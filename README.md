# MIDS Applicant Digital Assistant 

Steve Dille, Kevin Kory, Nicole Yoon, Joanna Yu

MIDS W210 Capstone Final Project, Spring 2021

## Introduction 
to be added

## 
### Excel Template Digital Assistant
Maintaining up-to-date information is an important issue for an applicant digital assistant. During the early stage of the project, we were successful in automating the creation of a Lex bot from an Excel template using CloudFormation. However, the dialogue complexity of our Lex digital assistant soon exceeded what could be supported by the Excel template. Therefore, we stopped the work in this area. The files are In the  "Excel" folder. 

Setup requirement:

AWS CLI 

Create an S3 bucket and update *sourcebucket* in *deployment.sh* with the bucket name

Run ./deployment.sh 

This template runs CloudFormation in the us_east1 region. 

Acknowledgement: this work is based on the work of Cyrus Wong (https://github.com/wongcyrus/ExcelLexBot)