import os
import pickle
import tempfile
import pandas as pd
from io import BytesIO
from langchain.document_loaders import PyPDFLoader
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
        self.qa_chain = None

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

    def load_documents(self, file_path, file_extension):
        ext = file_extension.lower()
        documents = []

        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
            documents = loader.load()
        elif ext == ".xlsx":
            xlsx_file = pd.ExcelFile(file_path)
            for sheet in xlsx_file.sheet_names:
                df = pd.read_excel(xlsx_file, sheet_name=sheet)
                text = df.to_string()
                documents.append(Document(page_content=text))
        elif ext == ".csv":
            csv_data = pd.read_csv(file_path)
            text = csv_data.to_string()
            documents.append(Document(page_content=text))
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        return documents

    def update_faiss_index(self, file_path, file_extension):
        user_folder = f"faiss_index_{self.user_id}"
        embeddings = OpenAIEmbeddings(api_key=self.api_key)

        if os.path.exists(user_folder):
            vectorstore = FAISS.load_local(user_folder, embeddings, allow_dangerous_deserialization=True)
        else:
            vectorstore = None

        docs = self.load_documents(file_path, file_extension)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        if vectorstore is None:
            vectorstore = FAISS.from_documents(splits, embeddings)
        else:
            vectorstore.add_documents(splits)

        os.makedirs(user_folder, exist_ok=True)
        vectorstore.save_local(user_folder)

        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=self.api_key),
            retriever=retriever,
            memory=self.memory
        )

    def query_documents(self, query: str) -> str:
        if not self.qa_chain:
            raise ValueError("QA chain not initialized. Please load documents first.")

        result = self.qa_chain({"question": query})
        self.save_memory()
        return result['answer']

def loaddoc(file_bytes: bytes, file_extension: str, api_key: str, user_id: str) -> None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file.write(file_bytes)
        temp_file_path = temp_file.name

    chat_doc = ChatWithDoc(api_key, user_id)
    chat_doc.update_faiss_index(temp_file_path, file_extension)

def chatwithdoc(query: str, api_key: str, user_id: str) -> str:
    chat_doc = ChatWithDoc(api_key, user_id)
    return chat_doc.query_documents(query)
