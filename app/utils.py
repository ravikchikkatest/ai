import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings  
from langchain_community.vectorstores import Chroma

from langchain_text_splitters import RecursiveCharacterTextSplitter

class Utils:
    
    @staticmethod
    def extract_text_from_resume(file):
        # Extract text from uploaded files
        temp_file_path = f"temp_{file.name}"
        with open(temp_file_path, "wb") as f:
            f.write(file.getbuffer())

        file_extension = os.path.splitext(file.name)[1].lower()
        try:
            if file_extension == '.pdf':
                loader = PyPDFLoader(temp_file_path)
            elif file_extension == '.docx':
                loader = Docx2txtLoader(temp_file_path)
            elif file_extension == '.txt':
                loader = TextLoader(temp_file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")

            documents = loader.load()
            text = " ".join([doc.page_content for doc in documents])
            return text
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    @staticmethod
    def get_google_llm(GOOGLE_API_KEY):
        # genai API key setup
        genai.configure(api_key=GOOGLE_API_KEY)
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.2
        )
        return llm
    
    @staticmethod
    def get_vector_store(GOOGLE_API_KEY):
        # genai API key setup
        genai.configure(api_key=GOOGLE_API_KEY)
        # Setup embedding model
        embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        # Create or load Chroma vector store
        VECTOR_STORE_DIR = "C:\\Agentic\\chroma_store"
        if os.path.exists(VECTOR_STORE_DIR):
            vectorstore = Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embedding_model)
        else:
            os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
            vectorstore = Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embedding_model)
        return vectorstore
    

class VectorStoreUtils:

    def __init__(self, app_name):
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.app_name = app_name
    
    def get_vector_store(self):
        # genai API key setup
        genai.configure(api_key=self.GOOGLE_API_KEY)
        # Setup embedding model
        embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        # Create or load Chroma vector store
        VECTOR_STORE_DIR = f"C:\\Agentic\\chroma_store\\{self.app_name}"
        if os.path.exists(VECTOR_STORE_DIR):
            vectorstore = Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embedding_model)
        else:
            os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
            vectorstore = Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embedding_model)
        return vectorstore
    
    # Text splitting
    def __split_text(self,text):
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return splitter.create_documents([text])


    def store_resume_analysis(self, analysis,  doc_metadata):
        documents = self.__split_text(analysis)
        vectorstore = self.get_vector_store()
        docs_with_metadata = []
        for doc in documents:
            doc.metadata = doc_metadata.copy()
            docs_with_metadata.append(doc)

        vectorstore.add_documents(docs_with_metadata)
        vectorstore.persist()