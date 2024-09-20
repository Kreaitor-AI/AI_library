import os
import pickle
from io import BytesIO
import pandas as pd
import boto3
from langchain.document_loaders import (
    PyPDFLoader, UnstructuredWordDocumentLoader, UnstructuredFileLoader,
    UnstructuredExcelLoader, UnstructuredCSVLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document

class ChatWithDoc:
    def __init__(self, api_key: str, user_id: str):
        self.api_key = api_key
        self.user_id = user_id
        self.memory = self.load_memory()

    def save_memory(self):
        memory_path = f"{self.user_id}_memory.pkl"
        with open(memory_path, "wb") as f:
            pickle.dump(self.memory, f)

    def load_memory(self):
        memory_path = f"{self.user_id}_memory.pkl"
        if os.path.exists(memory_path):
            with open(memory_path, "rb") as f:
                memory = pickle.load(f)
        else:
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        return memory

    def load_documents(self, file_stream):
        documents = []

        if file_stream.name.endswith(".pdf"):
            loader = PyPDFLoader(file_stream)
            documents = loader.load()
        elif file_stream.name.endswith(".docx"):
            loader = UnstructuredWordDocumentLoader(file_stream)
            documents = loader.load()
        elif file_stream.name.endswith((".txt", ".md")):
            loader = UnstructuredFileLoader(file_stream)
            documents = loader.load()
        elif file_stream.name.endswith(".xlsx"):
            xlsx_file = pd.ExcelFile(file_stream)
            for sheet in xlsx_file.sheet_names:
                df = pd.read_excel(xlsx_file, sheet_name=sheet)
                text = df.to_string()
                documents.append(Document(page_content=text))
        elif file_stream.name.endswith(".csv"):
            csv_data = pd.read_csv(file_stream)
            text = csv_data.to_string()
            documents.append(Document(page_content=text))
        else:
            raise ValueError("Unsupported file type.")

        return documents

    def update_faiss_index(self, file_stream):
        user_folder = f"faiss_index_{self.user_id}"
        embeddings = OpenAIEmbeddings(api_key=self.api_key)

        if os.path.exists(user_folder):
            vectorstore = FAISS.load_local(user_folder, embeddings, allow_dangerous_deserialization=True)
        else:
            vectorstore = None

        docs = self.load_documents(file_stream)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        if vectorstore is None:
            vectorstore = FAISS.from_documents(splits, embeddings)
        else:
            vectorstore.add_documents(splits)

        os.makedirs(user_folder, exist_ok=True)
        vectorstore.save_local(user_folder)

        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=self.api_key),
            retriever=retriever,
            memory=self.memory
        )

        return qa_chain

def loaddoc(file_url: str, aws_access_key: str, aws_secret_key: str, bucket_name: str, api_key: str, user_id: str) -> ConversationalRetrievalChain:
    """
    Load documents from S3 and update the FAISS index.
    
    Args:
        file_url (str): The URL of the file in the S3 bucket.
        aws_access_key (str): AWS access key.
        aws_secret_key (str): AWS secret key.
        bucket_name (str): S3 bucket name.
        api_key (str): API key for the OpenAI model.
        user_id (str): Unique user identifier.
        
    Returns:
        ConversationalRetrievalChain: The QA chain for the loaded documents.
    """
    # Create S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    
    # Download the file
    file_stream = BytesIO()
    s3.download_fileobj(bucket_name, file_url, file_stream)
    file_stream.seek(0)  # Reset stream position to the beginning
    
    chat_doc = ChatWithDoc(api_key, user_id)
    return chat_doc.update_faiss_index(file_stream)

def chatwithdoc(query: str, qa_chain: ConversationalRetrievalChain, api_key: str, user_id: str) -> str:
    """
    Query the loaded documents using the QA chain.
    
    Args:
        query (str): The question to ask.
        qa_chain (ConversationalRetrievalChain): The QA chain to use for the query.
        api_key (str): API key for the OpenAI model.
        user_id (str): Unique user identifier.
        
    Returns:
        str: The answer to the query.
    """
    chat_doc = ChatWithDoc(api_key, user_id)
    result = qa_chain({"question": query})
    chat_doc.save_memory()
    return result['answer']
