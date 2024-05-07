# A RAG Based AI Application Answer Questions About myself


## Introduction
This is a Retrival Augmented Generation(RAG) based AI application which is built in top of FastAPI framework. It can be deployed with docker and also can run locally. The purpose of this application is to answer any question about my professional career through an AI on behalf of myself. The complete application is having two APIs. One QNA api is responsible for answering questions. Another terminate api is responsible for clearing the chat history for a particular conversation for a unique user so that cache memory becomes empty. The reason why second API was implemented because , we can easily integrate it with a frontend application. And at realtime many people can use it at scale. In one sentence, to make it a production ready application, I implemented it.

## Technology Used
1. FastAPI
2. Uvicorn
3. Docker
4. Docker-Compose
5. Langchain-Community
6. Langchain
7. Ollama
8. chatgpt

## Architecture And Flow
Now lets talk about the flow of the applcation. The flow of the application is given below

1. At the start of the application it will load the pdf full with questions and answers about me generated from my resume. I have generated these questions and answers from my resume with chatgpt, so that with RAG approach it works good with answering

2. Load the llm(large language model). Decide whether you want to use chatgpt or ollama

3. Set the prompt template

4. Build a retrival qa chain and return

5. Start the uvicorn server and application will start running

6. For each request : Trigger the QNA API with a query and session_id(unique customer session:can be a combination of customer_id + current datetime)

7. Getting the chat history for that particular session

8. Extract the relevant chunk of documents through from chroma vector database using the query

9. Format the entire prompt with the query, extracted chunk(context) and chat history

10. Call the llm with prompt and get llm response

11. Update it to the chat history in the cache

12. Return the response

13. Once a session is completed, release session cache data with terminate session api.

This is all about the flow of the applications. You can find the end to end architecture of this application below
![Architecture Diagram](https://github.com/Rahu16/RAG/blob/master/RAG_Architectire.drawio.png)


***Here you can find a video link demostration of the entire application***

![Video Document](https://github.com/Rahu16/RAG/blob/master/video_documentation)


## How To RUN the Application

There are two ways you can run the application.
a. You can run it manually in you local environment
b. You can run it with docker and docker-compose


### RUN LOCALLY

***Prerequisites:***
a. Need to install python from [here](https://www.python.org/downloads/)
b. Need to understand basis python
c. Need to run ollama in local : [docs](https://github.com/ollama/ollama)

***steps***

1. Clone the repository
2. Go to the root directory of the repository
3. Create a virtual env with comman `python3 -m venv env`
4. Execute the command `pip3 install -r requirements.txt`
5. Once requirements installations are done, open constants.py and choose your
   settings like what llm you want to use and what will be the temparature, top_p and top_k. Although for chatgpt and top_p and top_k is not configurable.
6. Put your api key from [here](https://platform.openai.com/api-keys) if you
   want to use chatgpt and provide the value of `LLM_TYPE` as `chatgpt`
7. If you want to use ollama, provide `LLM_TYPE`. For example if you want to use mistral:latest with ollama use the value of `LLM_TYPE` as `Ollama_mistral:latest`.
8. Choose the ollama base url if you are using ollama, if ollama is running on your local port 11434, then `base_url` would be `http://localhost:11434`
9. Remeber before using any llm using ollama, you have to first pull it with the command mentioned in the docs given above
10. Once all these settings are done. Run `python3 main.py` and it should serve the application on port 8500
11. Once it is done, you can open your browser and hit `http://localhost:8500/docs`, you can find swagger api docs and test the application there


### RUN with Docker and docker-compose

***Prerequisites:***
a. Need to install Docker from [here](https://docs.docker.com/engine/install/)
b. Install docker-compose from [here](https://docs.docker.com/compose/install/)
c. Need to be aware of basis linux commands to run it

***steps***

1. Clone the repository
2. Go to the root directory of the repository
3. Change the `LLM_TYPE` and `OPENAI_API_KEY` based on what LLM you want to use
4. If you want to change `LLM_CONFIG`, please check constants.py
5. Once all these setup is done, execute `docker-compose up -d --build`(if docker-compose is installed on root use sudo for linux)
6. Once both containers are running you can check with the command `docker ps`
7. Once it is running, if you want to use ollama, what llm you have chosen or 
  given in `docker-compose.yml`, you have load that in ollama container. For example if you have chosen to use mistral, the on your cmd or terminal execute `docker exec -it RAG-ollama-container-1 ollama run mistral`. It takes some time to load the entire model

8. Once it is done, you can open your browser and hit `http://localhost:8500/docs`



### API Documentation

***QNA API***
`Request Type` : `POST`
`url` : `http://localhost:8500/v1/rag/QnA`

`Request Body` : ```{
  "Query": "What you have worked in capgemini ?",
  "session_id": "string"
}```


`Response Body` :

Success Response :

```
{
    "Query": "What you have worked in capgemini ?",
    "Answer": " I have worked at Capgemini. One challenge I faced there was managing tight deadlines while ensuring the quality of deliverables. To overcome this, I prioritized tasks, communicated effectively with stakeholders, and utilized agile methodologies for iterative development and feedback."
  },
  200
```

Failed Response :

```
{"Query" : "What you have worked in capgemini ?" ,
 "Error" : Internal Server Error : (error)
 }
 ,
 500
```



***Terminate Session API***
`Request Type` : `GET`
`url` : `http://localhost:8500/v1/rag/terminate_session/<session_id>`


`Response Body` :

Success Response :

```
{
    "Terminated_SessionID": "string",
    "session_details": [
      [
        "What you have worked in capgemini ?",
        " I have worked at Capgemini. One challenge I faced there was managing tight deadlines while ensuring the quality of deliverables. To overcome this, I prioritized tasks, communicated effectively with stakeholders, and utilized agile methodologies for iterative development and feedback."
      ]
    ]
  },
  200
```

Failed Response :

```
{
"session":session_id,
"error_msg":msg
},
500
```

### Conclusion

So this is just a proof of concept made using RAG based approach where it will answer questions about myself. Initially I thought if making it a application where we can upload any resume we want and ask questions from it. But then I thought making it as an individual application where it can answer anything about one person like I can name it as `AskHasibul`.

However as it is an assignement to show case capabilities, I am not making much changes now. I believe there are many imporvements we can do it this application
For example

1. We can store the entire chat history in a database through terminate session_id api which will helpful for analytics
2. The answers where llm failed , we can add those answers data in our documents, so that next time it can answer properly
3. As thorough testing is not done, it may not answer professionally for some question. We may have to make little changes in prompt template after through testing

And many more improvments we can do with time. If anyone is here reading this document, Thank you for reading this document with patients. Will be waiting for some feedback about this application. Thank You
