from langchain_community.llms import Replicate
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.documents import Document

from .crawler import Crawler


llm = Replicate(
    model="meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d",
    model_kwargs={"temperature": .7}
)

def load_and_split_docs(link):
    loader = WebBaseLoader(link)
    doc = loader.load_and_split()
    splits = RecursiveCharacterTextSplitter().split_documents(doc)
    return splits

def get_retriever(splits):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2",model_kwargs={"device":"cpu"})
    vector = FAISS.from_documents(splits, embeddings)
    return vector.as_retriever()

def get_bot_posts():
    crawler = Crawler()
    trends = crawler.get_trends()
    web_links = crawler.get_web_links(trends) 
    documents = load_and_split_docs(web_links)
    retriever = get_retriever(documents)
    
    prompt = ChatPromptTemplate.from_template(
        """Answer the following question from the provided context:
        <context>
        {context}
        </context>
        Question: {input}""")
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    posts = []
    for trend in trends:
        response = retrieval_chain.invoke({"input":"Write a short sized blog post on the trending term {trend_term}."})
        posts.append(response['answer'])
     
    topics = []   
    for post in posts:
        response = document_chain.invoke({
            "input":"Write a suitable title for the blog post privided as context",
            "context": [Document(page_content=post)]
        })
        topics.append(response['answer'])
        
    contents = [{
        "topic": topic,
        "post": post} for topic, post in zip(topics,posts)]
    
    return contents