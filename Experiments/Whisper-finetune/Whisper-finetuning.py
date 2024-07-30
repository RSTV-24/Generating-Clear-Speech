import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor, WhisperFeatureExtractor, WhisperTokenizer
from datasets import load_dataset, DatasetDict
import evaluate
from dataclasses import dataclass
from typing import Any, Dict, List, Union

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

checkpoint = "openai/whisper-base.en"
tokenizer = WhisperTokenizer.from_pretrained(checkpoint, task="transcribe")
model = WhisperForConditionalGeneration.from_pretrained(checkpoint)
model.to(device)
processor = WhisperProcessor.from_pretrained(checkpoint, task="transcribe")
feature_extractor = WhisperFeatureExtractor.from_pretrained(checkpoint, task="transcribe")

torgo = DatasetDict()
torgo["train"] = load_dataset("tanmay-udupa/torgo_audio_dataset", split="train")
torgo["train"] = torgo["train"].shuffle(seed=42)
split_datasets = torgo["train"].train_test_split(test_size=0.2, seed=42)
torgo["train"] = split_datasets["train"]
torgo["eval"] = split_datasets["test"]

def prepare_dataset(batch):
    batch_audio = batch["audio"]["array"]
    input_features = feature_extractor(
        batch_audio,
        sampling_rate=batch["audio"]["sampling_rate"]
    ).input_features[0]
    labels = tokenizer(batch["transcription"]).input_ids
    return {"input_features": input_features, "labels": labels}

torgo["train"] = torgo["train"].map(prepare_dataset, remove_columns=torgo["train"].column_names)
torgo["eval"] = torgo["eval"].map(prepare_dataset, remove_columns=torgo["eval"].column_names)

print("Train dataset:", torgo["train"])
print("Eval dataset:", torgo["eval"])

@dataclass
class DataCollator:
    processor: Any
    decoder_start_token_id: int

    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        input_features = [{"input_features": feature["input_features"]} for feature in features]
        batch = self.processor.feature_extractor.pad(input_features, return_tensors="pt")

        label_features = [{"input_ids": feature["labels"]} for feature in features]
        labels_batch = self.processor.tokenizer.pad(label_features, return_tensors="pt")

        labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)
        if (labels[:, 0] == self.decoder_start_token_id).all().cpu().item():
            labels = labels[:, 1:]
        batch["labels"] = labels

        return batch

data_collator = DataCollator(processor=processor, decoder_start_token_id=model.config.decoder_start_token_id)
metric = evaluate.load("wer")

def compute_metrics(pred):
    pred_ids = pred.predictions
    label_ids = pred.label_ids

    label_ids[label_ids == -100] = tokenizer.pad_token_id

    pred_str = tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    label_str = tokenizer.batch_decode(label_ids, skip_special_tokens=True)

    wer = 100 * metric.compute(predictions=pred_str, references=label_str)

    return {"wer": wer}

from transformers import Seq2SeqTrainingArguments, Seq2SeqTrainer

training_args = Seq2SeqTrainingArguments(
    output_dir="./whisper-torgo",
    per_device_train_batch_size=32,
    gradient_accumulation_steps=4,
    learning_rate=1e-5,
    remove_unused_columns=False,
    warmup_steps=5,
    max_steps=200,
    gradient_checkpointing=True,
    fp16=True,
    evaluation_strategy="steps",
    per_device_eval_batch_size=8,
    predict_with_generate=True,
    generation_max_length=225,
    save_steps=100,
    eval_steps=20,
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="wer",
    greater_is_better=False,
    push_to_hub=False,
)


trainer = Seq2SeqTrainer(
    args=training_args,
    model=model,
    train_dataset=torgo["train"],
    eval_dataset=torgo["eval"],
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    tokenizer=processor.feature_extractor,
)

trainer.train()
