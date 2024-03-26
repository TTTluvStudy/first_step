#s使用streamlit作为图形界面
import streamlit as st



def main():

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
        st.file_uploader("Upload your PDFs here and click on 'Process'")
        st.button("Process")




if __name__ == '__main__':
    main()


