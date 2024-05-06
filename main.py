import warnings
import time
import os
import uvicorn
from logger import log

from fastapi import FastAPI
from pydantic import BaseModel
from service import create_chain, Conversation

# Setting for no warning messages. 
warnings.filterwarnings("ignore")
app = FastAPI()

class Text(BaseModel):
    Query: str
    session_id: str


log.info("Creating Chain...")
chain = create_chain()
chat_manager = {}



@app.post('/v1/rag/QnA')
def Call_NLU(input_text: Text):
    global chat_manager
    start = time.time()
    text = input_text.Query
    session_id = input_text.session_id
    log.info(f"Received Payload Text : {text} :: Session ID : {session_id}")
    if session_id not in chat_manager.keys():
        chat_manager[session_id] = []
        log.info("Initiated new Session")
    log.info(f"Chat History For {session_id} ::: {chat_manager[session_id]} ")
    try:
        result, chat_history = Conversation(chain, chat_manager.get(session_id), text)
        chat_manager[session_id] = chat_history
    except Exception as e:
         log.info(f"Error Occured Query :: Query : {text} :: Error : {str(e)}")
         return {"Query" : {text}, "Error" : {str(e)}}, 500
    timeTaken = str(time.time()-start)
    log.info(f"Response : {result} :: Time Taken :: {timeTaken}")
    return {"Query": text, "Answer":result}, 200

@app.get('/v1/rag/terminate_session/{session_id}')
def TerminateSession(session_id: str):
    global chat_manager
    try:
        removed_session = chat_manager.pop(session_id)
        response = {"Terminated_SessionID":session_id, "session_details":removed_session}
        log.info(f"Removing Session {response}")
    except Exception as e:
         log.info(f"Error is Removing Session {session_id}:{str(e)}")
         return {"session":session_id, "error_msg":str(e)}, 500
    return response, 200

if __name__ == '__main__':
	# app.run(host='0.0.0.0', port=4601)
	uvicorn.run(app,host='0.0.0.0', port=8500)
