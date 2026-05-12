from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

loader = TextLoader("papers/document.txt")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=500,chunk_overlap=50)
splits = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

vectorstore = Chroma.from_documents(splits, embeddings)

llm = Ollama(model = "llama3")
qa_chain = RetrievalQA.from_chain_type(llm,retriever = vectorstore.as_retriever())

query="这篇文章的创新点是什么？"
result = qa_chain.invoke({"query":query})
print(result)