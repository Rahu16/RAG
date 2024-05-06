from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from logger import log
from constants import LLM_TYPE, openai_api_key, OLLAMA_BASE_URL, LLM_CONFIG
import os


os.environ["TOKENIZERS_PARALLELISM"] = 'false'


qa_template = """
Use the following pieces of information about Hasibul to answer the user's question.
From now onwards you are Mr. Hasibul Mondal. Answer all the asked questions for Hasibul Mondal
If you don't know the answer, just say that you don't know, don't try to make up an answer.
You behave as Hasibul Mondal in his absense.
Please provide the answer only in the context of data present in vector store. please do not 
give me the answer from the data you were trained on.Just format the answer in a presentable way
and answer it. Don't provide any answer out of the context

Provide answers only for that particular question which is asked in the Context. Don't provide unnecessary answers

Context: {context}
Question: {question}

*Note : Don't respond with Answers like (Based on the provided context, According to the context provided, Based on the information in the vector store about, ... e.t.c).
These kind of extra addition to the sentence should never come as answer.
Provide Raw Well organized necessary answers

Only return the helpful answer below and nothing else.
Helpful answer:
"""


def load_data():
    log.info("Loading Data ...")
    loader = DirectoryLoader('data/',
                            glob="*.pdf",
                            loader_cls=PyPDFLoader)
    documents = loader.load()

    # Split text from PDF into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                chunk_overlap=50)
    texts = text_splitter.split_documents(documents)


    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                    model_kwargs={'device': 'cpu'})
    
    vectorstore = Chroma.from_documents(texts, embeddings)
    return vectorstore
    # vectorstore.save_local('vectorstore/db_faiss')


def load_llm():
    log.info("Loading LLM")
    # Local CTransformers wrapper for Llama-2-7B-Chat
    if LLM_TYPE == "chatgpt":
        llm = ChatOpenAI(model_name="gpt-3.5-turbo",openai_api_key = openai_api_key,temperature=LLM_CONFIG.get('temparature'))
    else:
        llm = ChatOllama(model=LLM_TYPE.split("_")[1], base_url=OLLAMA_BASE_URL, temparature=LLM_CONFIG.get('temparature'), top_p=LLM_CONFIG.get('top_p'), top_k=LLM_CONFIG.get('top_k'))
    return llm

# Wrap prompt template in a PromptTemplate object
def set_qa_prompt():
    prompt = PromptTemplate(template=qa_template,
                            input_variables=['chat_history', 'context', 'question'])
    return prompt


# Build RetrievalQA object
def build_retrieval_qa(llm, prompt, vectorstore):
    log.info("Building QnA Chain...")
    dbqa = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=vectorstore.as_retriever(search_kwargs={'k':1}),
                                       return_source_documents=True,
                                       chain_type_kwargs={'prompt': prompt})

    # dbqa = ConversationalRetrievalChain.from_llm(llm=llm,
    #                                    chain_type='stuff',
    #                                    retriever=vectorstore.as_retriever(search_kwargs={'k':1}),
    #                                    return_source_documents=True)

    return dbqa




def create_chain():
    vectorstore = load_data()
    llm = load_llm()
    prompt = set_qa_prompt()
    chain = build_retrieval_qa(llm, prompt, vectorstore)
    log.info("Chain Created")
    return chain


def Conversation(chain, history, query):
    query_dict = {'query': query, "chat_history":history}
    # response = chain({'query': 'What is DMI Finance'})
    response = chain(query_dict)
    # log.info(f"COMPLETE {response}")
    answer = response['result']
    history.extend([(query, answer)])
    return answer, history
