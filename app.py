#使用streamlit作为图形界面
import streamlit as st
#load_dotenv 是一个函数需要在main内部运行，以便应用程序可以使用.env中的变量
from dotenv import load_dotenv
# 实现获取pdf中的文字内容的库
from PyPDF2 import PdfReader
# 获取实现字符分割的模块
from langchain.text_splitter import CharacterTextSplitter
# 获取embedding 的 api
from langchain.embeddings import HuggingFaceInstructEmbeddings
# 导入本地向量数据库 FAISS 
from langchain.vectorstores import FAISS
# 会话缓存内存，保存对话
from langchain.memory import ConversationBufferMemory
# 导入会话检索链，允许与向量数据库对话
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub

# 获取PDF中的文字内容的函数,返回一个包含PDF文本内容的字符串
def get_pdfs_text(pdf_docs):
    #先初始化变量，然后遍历整个文本，储存在变量中
    text = ""
    for pdf in pdf_docs:
        #初始化pdf阅读器对象。创建一个包含所有页面的PDF对象。
        pdf_reader = PdfReader(pdf)
        #提取每个页面的内容，储存在text变量中
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# 将获取到的文本分割成块
def get_text_chunks(text):
    # text_spliter需要一些参数定义，第一是分隔符，此处为换行符；第二是块的大小，此处为500字符；第三为块的重叠度，
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 500,
        chunk_overlap = 100,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    # 这里是向量化使用的 api 接口，可以不是openai
    embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")
    # 这里是将向量化的数据储存在数据库中
    vectorstore = FAISS.from_text(texts = text_chunks, embeddings = embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    #Temperature 不要是0就可以
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512}) 
    # 初始化内存
    memory = ConversationBufferMemory(memory_key = "chat_history", return_messages = True)
    # 初始化对话
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vectorstore.as_retriever(),
        memory = memory
    )
    return conversation_chain
        
def handle_userinput(user_question):
    # 用 st.session_state 是为了保证能记住上下文
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    # 允许使用索引以及索引内容循环遍历整个聊天历史记录
    for i, message in enumerate(st.session_state.chat_history):
        # 取偶数部分作为用户的内容，奇数部分作为机器人回答内容
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
def main():
    load_dotenv()

    #页面标题以及标题旁的表情符号
    st.set_page_config(page_title="chat with multiple PDFs",page_icon=":books:")

    st.write(css, unsafe_allow_html=True)

    # 当应用程序重新运行时（不是刷新），它将检查对话是否已经被初始化，如果已经初始化，则不会对其执行任何操作
    if "conversation" not in st.session_state:
        st.session_state.convesation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    #这是应用程序的主标题
    st.header("chat with multiple PDFs :books:")

    #在标题下方，有一个文本输入，这是文本输入的标签
    user_question = st.text_input("ask a question about your documents:")
    
    if user_question:
        handle_userinput(user_question)

    #增加一个侧边栏，使用户可以在这里上传文档
    with st.sidebar:
        st.subheader("Your docuemnt")
        #实现加载功能，upload
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'",accept_multiple_files=True)
        
        if st.button("Process"):

            #添加一个微调器,使得以下操作在进行时用户可以看到反应
            with st.spinner("Processing"):
                # get PDFs text
                raw_text = get_pdfs_text(pdf_docs)

                # 获取文字，然后将其分为文本块
                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain 
                # st,session_state 帮助避免重复初始化这个变量
                st.session_state.conversation = get_conversation_chain(vectorstore)


if __name__ == '__main__':
    main()


