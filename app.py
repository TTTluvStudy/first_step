#使用streamlit作为图形界面
import streamlit as st
#load_dotenv 是一个函数需要在main内部运行，以便应用程序可以使用.env中的变量
from dotenv import load_dotenv
# 实现获取pdf中的文字内容的库
from PyPDF2 import PdfReader

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

def main():
    load_dotenv()

    #页面标题以及标题旁的表情符号
    st.set_page_config(page_title="chat with multiple PDFs",page_icon=":books:")

    #这是应用程序的主标题
    st.header("chat with multiple PDFs :books:")

    #在标题下方，有一个文本输入，这是文本输入的标签
    st.text_input("ask a question about your documents:")

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
                st.write(raw_text)


                # get the text chunks


                # create vector store




if __name__ == '__main__':
    main()


