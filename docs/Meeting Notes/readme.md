### 25 August 2023
>Meeting 7:30 PM
>Discussing domains, ideas, and potential guides 
>https://arxiv.org/archive/

### 27 August 2023
> Ambhikesh: idea for the project: partly inspired by [this article](https://medium.com/@shwpatki/why-bother-with-inclusive-tech-edc4184ea264) 

### 29 August 2023
>Mailed Prof. Srinath and set up a meeting for 10:15 a.m. on 30 Aug
>[Capstone idea pitch- presentation](https://docs.google.com/presentation/d/1MtmYfKMdkwk1Fii-owboDo6b3eOS0agALosNrAi16eU/edit?usp=sharing): made slides to pitch to Prof. Ramamoorthy Srinath

### 04 October 2023
>Had a brainstorming session
> Ideas:
> 	Consumer laws 
> 	Signature Forgery
> 	Early prediction of stocks
> 	 The speech problem using Error Correcting Codes(?)
### 19 December 2023
> Mailed Prof. Srinath regarding his decision.
> Extra Ideas:
> 	Determining the parallelism in an algorithm using DL.
> 	A ML model which determines the period in which a painting was created.
> 	Physical threat analysis using surveillance videos using DL.

### 25 December 2023
> Prof. Srinath Confirmed his decision.
- [ ] try and get some data sets on the for the problems (I will share some for starters tomorrow)
- [ ] try and assemble 5-10  papers ( yr2020-2023).
- [ ] Try and formulate a rough set of Demo requirements ( futuristic), that will give a 10,000ft view of Reqts.
### 12 January 2024
Prof. Srinath and team discussed about few possible projects ideas
>Have to settle with a final project idea
>Gave a brief outline on all the ideas
```md
painting
how many paintings arent dated yet 
how to verify the answer
how to verify originality or deepfake detection
what is use case
treding
dataset
utility rating
Conferences

perplexity ai

need an app on mobile or laptop 
sending an impaired speech, associate with text 
auto encoder, 
latent data, train the net to produce the right things
frequencies of frequencies
Generative AI
deep learnig to map correct data from the dataset
real time translator
test it
impaired speech
mix of impaired and normal speech
```
### 19 January 2024

Team meeting 
>find benchmarks: google project relate
>what model are you going to use
>feasibility:
>scope and major tasks
>use case:
>planning and deliverables timeline
>requirements specification 
>hldd
>potential questions that will be asked
>and answered
>ai and software tools we are using for the project
>weekly reviews, meeting documentation


A discussion with Srinath Sir, about the possible approaches and demonstration of the project
—
Roseline:
>Meeting with sir
>Block diagram
>Recorded conversation
>4 scenarios: 2 people scenario extend bidirectionally
>Multiagent scenario multiple each and dynamic
>Source: impaired speech output
>Destination: non impaired
>Model in real time like a firewall sitting there doing the transfer, time lags
>Recorded convo: Simplest model for the first time demo 
>Impaired speech Like foreign language translation 
>Dialog for a while
>Based on the response of the receiver we evaluate the performance 
>One test without model
>One test with model and compare the result
>Extend to star shaped model and bidirectional impairment
>Final demo: 4 way conversation with impairments in all ways DEMo PROMISE STATIC SOURCE IMPAIRMENT
>Source and destinations should be identified
>Look for machine learning models that take speech and map it to speech
>Driven by a dataset of live recordings
>Get some sample conversations 
>Speech to speech or speech to text and text to speech easier) upgradation of problem 
>Submit diagrams in sandbox soon 

—
Ambhikesh:
>Real time perspective either Mobile Application or PC Application.
>The model sits in between the source, destination and tries to map out the corrected speech. 
>Can be used as the start of a High Level Diagram.

>**2-speaker scenario**
>For demonstration, we could record a conversation between source and destination, where there can be 3 scenarios(normal-normal, normal-impaired, impaired-impaired).
>The model sits in between like a firewall. There'll be time lags involved. For real time , there is a strict time demand.

>**First level demo**: we can have one sender/receiver who is impaired and one sender/receiver who is non-impaired. 
>Recorded conversation of 20 minutes.
>If the destination user partially understands, then there's going to be a response of some nature and then you are going to produce for the same listener the transformed speech.
>If the destination user understood correctly, there's going to be a smooth response. (a positive response, the flow of conversation continues)
>If the destination user doesn't understand, they are going to say "can you repeat?" "I did not get that" (a negative response)
>Based on the response, we are going to evaluate the model efficiency.

>**Alternate View:** Instead of calling it as impaired >speech, we can call it as another language
>Suppose someone speaks perfect Chinese, but the other >person doesn't understand (similar to impaired >speech). It's not only translation, because we know >its a language and something about the conversation

>**Test**: Best way to test the model, tell the impaired speech user to read out a paragraph, or ask questions with a pre-defined answer. Because you know what is intended by the speaker with the impairment and what is not being understood by the receiver. And there should be  a different response(positive) when you put the model in between. If the response without the model and response with the model comes closer to each other, then its working perfectly

>**Extension**: multi-agent scenario (star based model with bi-directional impairment)
>multiple sources and multiple destinations
>for e.g. Conference Call

>**Final demo:** have your model working for a five-way conversation. (bidirectional and dynamic source) The model has to also identify where the impaired speech is coming from(?).
>five cornered with an autoencoder sitting in between with static source impairment(The model knows where the impaired speech is coming from).

>*"promise less and deliver more"*

>Next Level: Put this in a software, like morphing the user's voice.

>Use project relate as benchmark

### 21 January 2024
>Review-1 template was filled

---
## February 2024

### 03 January 2024
**Meeting with Prof. Srinath 15:30 -15:40 pm**      
> Load all referenced papers in lit review folder and offline             
> Slide numbering              
> Any major changes you make should be version controlled (V1.0, V2.0 etc)            
> Add diagrams after Feasibility slide             
> Add references and datasets in the last slide              
> If you have some audio sample you keep them in the slides(last)              
> transformer and encoder approach               
> Should tell whether our model is real time or not              
> Showcase all the papers we have gone through           
> If we are asked what model we are planning to use, we can tell the models currently in use.           



