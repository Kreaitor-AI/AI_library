import os
import pickle
import tempfile
from io import BytesIO
import pandas as pd
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
        self.embeddings = OpenAIEmbeddings(api_key=self.api_key)

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

    def load_documents(self, file_bytes: bytes, file_extension: str) -> list[Document]:
        ext = file_extension.lower()
        documents = []

        if ext == ".pdf":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(file_bytes)
                temp_pdf_path = temp_pdf.name
            loader = PyPDFLoader(temp_pdf_path)
            documents = loader.load()
            os.remove(temp_pdf_path)
        elif ext == ".xlsx":
            xlsx_file = pd.ExcelFile(BytesIO(file_bytes))
            for sheet in xlsx_file.sheet_names:
                df = pd.read_excel(xlsx_file, sheet_name=sheet)
                text = df.to_string()
                documents.append(Document(page_content=text))
        elif ext == ".csv":
            csv_data = pd.read_csv(BytesIO(file_bytes))
            text = csv_data.to_string()
            documents.append(Document(page_content=text))
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        return documents

    def update_faiss_index(self, file_bytes: bytes, file_extension: str):
        user_folder = f"faiss_index_{self.user_id}"

        if os.path.exists(user_folder):
            vectorstore = FAISS.load_local(user_folder, self.embeddings)
        else:
            vectorstore = FAISS(embedding_function=self.embeddings)

        documents = self.load_documents(file_bytes, file_extension)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(documents)

        vectorstore.add_documents(splits)
        os.makedirs(user_folder, exist_ok=True)
        vectorstore.save_local(user_folder)

        return vectorstore

    def query_documents(self, query: str) -> str:
        user_folder = f"faiss_index_{self.user_id}"

        if not os.path.exists(user_folder):
            raise ValueError(f"No FAISS index found for user ID: {self.user_id}")

        vectorstore = FAISS.load_local(user_folder, self.embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        relevant_docs = retriever.retrieve(query)
        if not relevant_docs:
            return "No relevant documents found for the query."

        prompt = f"Answer the following question based on the documents: {query}\nDocuments: {relevant_docs}"
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        result = llm({"question": prompt})

        # Save updated memory after the query
        self.save_memory()

        return result['answer']

def loaddoc(file_bytes: bytes, file_extension: str, api_key: str, user_id: str = "user_temp") -> FAISS:
    """
    Public function to load documents and update FAISS index.
    """
    doc_manager = ChatWithDoc(api_key=api_key, user_id=user_id)
    return doc_manager.update_faiss_index(file_bytes, file_extension)

def chatwithdoc(query: str, user_id: str, api_key: str) -> str:
    """
    Public function to query a FAISS index and generate a response.
    """
    doc_manager = ChatWithDoc(api_key=api_key, user_id=user_id)
    return doc_manager.query_documents(query)
