# Generating-Clear-Speech

## Capstone Project UE21

#### Team: RSTV-24

> **Project Title**: Generating Clear Speech from Speech impaired Audio                
> **Project ID**: PW24_RS_03                 
> **Project Guide**: Dr. Ramamoorthy Srinath                    
> **Project Team**: Roseline Jerry A, T P Shriambhikesh, Tanmay Praveen Udupa, Vandana S   



##### Setting Up the Environment

## 1. Create a Conda Environment

To create a new Conda environment named `rstv` with Python 3.11:




```bash
conda create --name rstv python==3.11
```

## 2. Activate the Conda Environment

To activate the newly created environment:

```bash
conda activate rstv
```



## 3. Install PyTorch and CUDA Support

To install PyTorch, torchvision, torchaudio, and PyTorch-CUDA 12.1 packages from the official PyTorch and NVIDIA channels:

```bash
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

## 5. Install Additional Dependencies

To install additional dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## 6. Install the TTS Library

To install the TTS (Text-to-Speech) library:

```bash
pip install TTS
```



