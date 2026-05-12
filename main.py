# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

rag_chain = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_chain
    DATA_PATH = "papers/"
    CHROMA_PATH = "chroma_db"

    print("初始化 RAG...")
    if not os.path.exists(CHROMA_PATH):
        print("构建向量库...")
        os.makedirs(DATA_PATH, exist_ok=True)
        docs = []
        for f in os.listdir(DATA_PATH):
            if f.endswith(".txt"):
                loader = TextLoader(os.path.join(DATA_PATH, f), encoding='utf-8')
                docs.extend(loader.load())
        if not docs:
            print("❌ 请将 .txt 文件放入 papers/ 文件夹")
            return
        splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = splitter.split_documents(docs)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        vectorstore = Chroma.from_documents(splits, embeddings, persist_directory=CHROMA_PATH)
        vectorstore.persist()
    else:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = Ollama(model="qwen2.5:7b", temperature=0.3)

    template = """Use the context to answer the question. If you don't know, say so.
Context: {context}
Question: {question}
Answer:"""
    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = (
        {
            "context": retriever | (lambda d: "\n\n".join(x.page_content for x in d)),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    print("✅ 就绪")
    yield
    print("关闭")

app = FastAPI(title="论文评估", lifespan=lifespan)

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    if rag_chain is None:
        raise HTTPException(503, "系统未就绪")
    try:
        ans = rag_chain.invoke(request.query)
        return QueryResponse(answer=ans)
    except Exception as e:
        raise HTTPException(500, str(e))