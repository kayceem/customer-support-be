import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader, UnstructuredExcelLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")


def RagService(question):
    """Rag Services for  hrgpt"""
    model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY, temperature=0.2, convert_system_message_to_human=True,)
    pdf_loaders = []
    excel_loaders = []
    folder_path = 'files'
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.lower().endswith('.pdf'):
            pdf_loaders.append(PyPDFLoader(file_path))
        elif file_name.lower().endswith(('.xls', '.xlsx')):
            excel_loaders.append(UnstructuredExcelLoader(file_path))
    pages = []
    for pdf_loader in pdf_loaders:
        pages += pdf_loader.load_and_split()
    for excel_loader in excel_loaders:
        pages += excel_loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    context = "\n\n".join(str(p.page_content) for p in pages)
    texts = text_splitter.split_text(context)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k": 5})
    # template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say "Sorry, this information is not available.", don't try to make up an answer. But if the question is a part of conversation like "hi", "hello" etc. keep carrying on the conversation. Keep the answer as concise as possible.
    # {context}
    # Question: {question}
    # Helpful Answer:"""
    template = """ You are a friendly customer support agent. You help people with their problem. Answer in full and professional sentences. Use the following pieces of context to answer the question at the end. If the answer is not available in the context, just say the information is not available in a professional manner , don't try to make up an answer. But if the question is a part of conversation like "hi", "hello" etc. keep carrying on the conversation. Keep the answer as concise as possible.
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
    qa_chain = RetrievalQA.from_chain_type(
        model,
        retriever=vector_index,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    result = qa_chain({"query": question})
    return result["result"]
