# MIDS Applicant Digital Assistant 

Steve Dille, Kevin Kory, Nicole Yoon, Joanna Yu

UC Berkeley MIDS W210 Capstone Final Project, Spring 2021

## Introduction 
The MIDS Applicant Advisor Digital Assistant targets graduate school applicants and provides a conversational AI solution to bridge the information gap between applicants and university program admissions teams. Using unstructured data based on key admissions facts and insider advice from students, we are applying natural language processing powered by Amazon Lex for our MVP which offers applicants easier access to previously hard to gather data to make informed decisions on MIDS application. We have already launched the first chatbot on the midsdvisor.com website to UC Berkeley MIDS candidates as our initial target user group.

## Infrastructure
![pipeline_diagram](/Images/infrastructure.jpg)
* Our website, **midsadvisor.com**, is hosted on WordPress. Javascript is used to connect to the Lex web user interface. When the user clicks “Chat Now”, the chatbot pops up as an iframe on the website. 
* **CloudWatch** maintains collect monitoring and operational data. The logs from CloudWatch are used for debugging purposes as well as extracting metric information on the chatbot. 
* **Lambda** is used to create custom functions in Lex. Lambda is a very versatile serverless compute tool that allows us to execute code in response to triggers, such as changes in data or actions by users. 
* **Cloudformation** is used to provision desired resources and their dependencies so related resources can be launched and configured together as a stack. 
* **Cognito** is used to set up permission and credentials so that midsadvisor.com can connect to the Lex chatbot interface. Cognito does user identity management and sets the appropriate IAM credentials.
* **CloudFront**, a content delivery network service, is used to provision object storage so the web application and build artifacts could be stored in the S3 bucket.

## Data
The digital assistant is powered by a variety of sources:
* Official content from the School of Information such as the MIDS website, FAQ, etc.
* Unstructured data based on key admissions facts 
* Insider advice from students

## Our Model
### AI-as-a-Service Model
**Amazon Lex** - AI as a Service for building conversational interfaces into any application using voice and text.

Advantages:
* Cost-Effective
* Short Time to Market
* Scales Automatically
* Leverages Alexa NLP to Create Speech Language Understanding System

## Model Limitation
*Limitations*
* Inflexible model - proprietary NLP engine
* Rule-based framework - limited conversational breadth
* Less conversational - limited conversational depth
 
*Solutions*
* Increased utterance fine-tuning
* Word / sentence variation
* Most common questions
* Increased question breadth
* Multi-turn design
* Intent chaining with context

## User Testing
* Three rounds of user testing (phased based on use case development)
* User survey - 3 dimensions: 
1. Ability to understand
2. Relevancy of response
3. Overall conversational capability

## Metrics & Evaluation
* Percentage of missed questions (utterances)
* Length of conversation
* Qualitative review of missed questions

## Other Work
### Excel Template Digital Assistant
Maintaining up-to-date information is an important issue for an applicant digital assistant. During the early stage of the project, we were successful in automating the creation of a Lex bot from an Excel template using CloudFormation. However, the dialogue complexity of our Lex digital assistant soon exceeded what could be supported by the Excel template. Therefore, we stopped the work in this area. The files are In the  "Excel" folder. 

Setup requirement:

AWS CLI 

Create an S3 bucket and update `sourcebucket` in `*deployment.sh` with the bucket name

Run `./deployment.sh` 

This template runs CloudFormation in the `us_east1` region. 

Acknowledgement: this work is based on the work of Cyrus Wong (https://github.com/wongcyrus/ExcelLexBot)

## Directory of Files
* `Code and Export/Chatbot JSON export` folder contains the json file to load the chatbot in Amazon Lex.
* `Code and Export/Lambda samples` folder contains sample lambda functions used in the chatbot. Each intent comes with a yaml and a python file. 
* `Code and Export/Metrics` folder contains the survey from the user testing and the jupyter notebook used to analyze the chat log. 
* `Code and Export/User Research` folder contains the results of the user research.
* `Code and Export/Web Deliverable` folder contains the Javascript used to create the Lex web UI iframe.
* `Excel` folder contains the files for the Excel Template Digital Assistant described above.
* `Images` folder contains images used in the repo.
* `Presentations` folder contains presentation slides for this project.

