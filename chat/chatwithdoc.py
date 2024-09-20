import os
import pickle
from io import BytesIO
import pandas as pd
from langchain.document_loaders import (
    PyPDFLoader, UnstructuredWordDocumentLoader, UnstructuredFileLoader,
    UnstructuredExcelLoader, UnstructuredCSVLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from .gpt4omini import gpt4omini
from typing import Optional

class DocumentManager:
    def _save_memory(self, memory, user_id: str):
        memory_path = f"{user_id}_memory.pkl"
        with open(memory_path, "wb") as f:
            pickle.dump(memory, f)

    def _load_memory(self, user_id: str) -> ConversationBufferMemory:
        memory_path = f"{user_id}_memory.pkl"
        if os.path.exists(memory_path):
            with open(memory_path, "rb") as f:
                memory = pickle.load(f)
        else:
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        return memory

    def _load_documents(self, file_bytes: bytes, file_extension: str) -> list[Document]:
        file_stream = BytesIO(file_bytes)
        ext = file_extension.lower()

        documents = []

        if ext == ".pdf":
            loader = PyPDFLoader(file_stream)
            documents = loader.load()
        elif ext == ".docx":
            loader = UnstructuredWordDocumentLoader(file_stream)
            documents = loader.load()
        elif ext in [".txt", ".md"]:
            loader = UnstructuredFileLoader(file_stream)
            documents = loader.load()
        elif ext == ".xlsx":
            xlsx_file = pd.ExcelFile(file_stream)
            for sheet in xlsx_file.sheet_names:
                df = pd.read_excel(xlsx_file, sheet_name=sheet)
                text = df.to_string()
                documents.append(Document(page_content=text))
        elif ext == ".csv":
            csv_data = pd.read_csv(file_stream)
            text = csv_data.to_string()
            documents.append(Document(page_content=text))
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        return documents

    def _get_vectorstore(self, user_id: str, embeddings: OpenAIEmbeddings) -> Optional[FAISS]:
        user_folder = f"faiss_index_{user_id}"
        if os.path.exists(user_folder):
            vectorstore = FAISS.load_local(
                user_folder,
                embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            vectorstore = None
        return vectorstore

    def _save_vectorstore(self, vectorstore: FAISS, user_id: str):
        user_folder = f"faiss_index_{user_id}"
        os.makedirs(user_folder, exist_ok=True)
        vectorstore.save_local(user_folder)

    def _split_documents(self, documents: list[Document]) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return text_splitter.split_documents(documents)

    def load_documents_to_faiss(self, file_bytes: bytes, file_extension: str, user_id: str, api_key: str) -> FAISS:
        embeddings = OpenAIEmbeddings(api_key=api_key)
        vectorstore = self._get_vectorstore(user_id, embeddings)
        
        documents = self._load_documents(file_bytes, file_extension)
        splits = self._split_documents(documents)

        if vectorstore is None:
            vectorstore = FAISS.from_documents(splits, embeddings)
        else:
            vectorstore.add_documents(splits)

        self._save_vectorstore(vectorstore, user_id)
        return vectorstore

    def query_documents(self, query: str, user_id: str, api_key: str) -> str:
        embeddings = OpenAIEmbeddings(api_key=api_key)
        vectorstore = self._get_vectorstore(user_id, embeddings)
        if vectorstore is None:
            raise ValueError(f"No FAISS index found for user ID: {user_id}")

        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        memory = self._load_memory(user_id)


        result = gpt4omini(prompt=f"Answer the following question based on the document: {query}", api_key=api_key)
        self._save_memory(memory, user_id)

        return result




def loaddoc(file_bytes: bytes, file_extension: str, api_key: str, user_id: str = "user_temp") -> FAISS:
    """
    Public function to load documents and update FAISS index.
    """
    doc_manager = DocumentManager()
    return doc_manager.load_documents_to_faiss(file_bytes, file_extension, user_id, api_key)


def chatwithdoc(query: str, user_id: str, api_key: str) -> str:
    """
    Public function to query a FAISS index and generate a response.
    """
    doc_manager = DocumentManager()
    return doc_manager.query_documents(query, user_id, api_key)
