import streamlit as st
from llama_index.core import StorageContext, load_index_from_storage, VectorStoreIndex, SimpleDirectoryReader, \
    ChatPromptTemplate
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import os
import base64
import json
from datetime import datetime
import random
import learning_agent
# 现在我直接找了一个文件问答的模板，后期只需要把我们的pipeline 封装成函数，即可执行用户输入对应输出
# 目前可以做的UI设计：
# 继续完善课件回答chatbot
# 设计复习chatbot的产品展示形式  √
# 将两者放在一个网站 (侧边栏 or 其他方法)  √
# 网站配色 可参考这个网站：https://coolors.co/262322-63372c-c97d60-ffbcb5-f2e5d7
# 修改streamlit配色方法：https://blog.csdn.net/BigDataPlayer/article/details/128962594
# 本地调试，命令行进入相应路径执行： streamlit run app.py

# 更新：目前复习模块的展示已经完成，但还剩相关问题生成需对接，包括聊天记录存储也已经完成，等待接口完成最终调试



@st.cache_data()
def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def build_markup_for_logo(
    png_file,
    background_position="50% 10%",
    margin_top="5%",
    image_width="80%",
    image_height="",
):
    binary_string = get_base64_of_bin_file(png_file)
    return """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    background-position: %s;
                    margin-top: %s;
                    background-size: %s %s;
                }
            </style>
            """ % (
        binary_string,
        background_position,
        margin_top,
        image_width,
        image_height,
    )


def add_logo(png_file):
    logo_markup = build_markup_for_logo(png_file)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )

add_logo("image/icon.png")






# Define the directory for persistent storage and data
PERSIST_DIR = "./db"
DATA_DIR = "data"
CHAT_HISTORY_DIR = "chat_history"  # New directory for chat history

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PERSIST_DIR, exist_ok=True)
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)  # Ensure chat history directory exists


def displayPDF(file):
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


if 'messages' not in st.session_state:
    st.session_state.messages = [
        {'role': 'assistant', "content": 'Hello! Upload a PDF and ask me anything about its content.'}]

if 'all_QA' not in st.session_state:
    st.session_state.all_QA = []

if 'qa_id' not in st.session_state:
    st.session_state.qa_id = 0

if 'conversation' not in st.session_state:
    st.session_state.conversation = 'conversation'

#
# # 随机选择一个QA文件，然后从该文件中随机选择一个QA对话
# def get_random_qa_pair():
#     chat_files = [f for f in os.listdir(CHAT_HISTORY_DIR) if f.endswith(".json")]
#
#     if not chat_files:
#         return None, None  # 如果没有文件，返回None
#
#     # 从目录中随机选择一个文件
#     selected_file = random.choice(chat_files)
#
#     # 读取文件并提取所有聊天记录
#     with open(f"{CHAT_HISTORY_DIR}/{selected_file}", 'r') as file:
#         chat_data = json.load(file)
#
#     # 确保文件中有内容
#     if len(chat_data) > 0:
#         # 从聊天记录中随机选择一个QA对
#         random_index = random.randint(0, len(chat_data) - 1)
#         selected_qa = chat_data[random_index]
#         return selected_qa['user'], selected_qa['answer']
#
#     return None, None  # 如果文件中没有聊天记录


#image icon
icon_path = r"image\icon.png"
# Streamlit app initialization
st.title("Chat with your PDF📄")
# st.markdown("Built by [Qichen❤️]()")
st.markdown("chat here👇")

#
# # 侧边栏
# with st.sidebar:
#     st.image(icon_path, use_column_width=True)
#     st.title("Menu:")
#     uploaded_file = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button")
#     if st.button("Submit & Process"):
#         with st.spinner("Processing..."):
#             filepath = "data/saved_pdf.pdf"
#             with open(filepath, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
#             # displayPDF(filepath)  # Display the uploaded PDF
#
#             learning_agent.ingest_and_index_with_pdf_reader(filepath, PERSIST_DIR)
#             st.success("Upload file successfully!")
#
# # New code from here
#     if st.button("Review Mode"):
#         # 获取随机QA对
#         user, answer = get_random_qa_pair()
#         print(user, answer)
#
#         if user is not None and answer is not None:
#             # 存储到会话状态中
#             st.session_state['current_qa_pair'] = {'user': user, 'answer': answer}
#             st.rerun()  # 触发刷新以更新显示
#         else:
#             st.write("No QA pairs found.")
#
# # If Review Mode is activated and we have a QA pair
# if 'current_qa_pair' in st.session_state:
#     # Refresh button to get a new random QA pair
#     if st.sidebar.button("Refresh QA"):
#         # 获取新的随机QA对
#         user, answer = get_random_qa_pair()
#
#         if user is not None and answer is not None:
#             st.session_state['current_qa_pair'] = {'user': user, 'answer': answer}
#             st.rerun()  # 触发刷新
#         else:
#             st.sidebar.write("No QA pairs found.")
#
#     st.sidebar.write("Random QA Pair:")
#     qa_pair = st.session_state['current_qa_pair']
#     user = qa_pair.get("user", "Unknown")
#     answer = qa_pair.get("answer", "No answer")
#     st.sidebar.write(f"User: {user}")
#     st.sidebar.write(f"Answer: {answer}")
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

# 侧边栏
with st.sidebar:
    # 设置图片和标题
    st.title("Menu:")

    # 上传文件
    uploaded_file = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button")

    # 提交并处理文件
    if st.button("Submit & Process", use_container_width=True):
        with st.spinner("Processing..."):
            # 保存上传的文件
            filepath = "data/saved_pdf.pdf"
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # 处理文件
            learning_agent.ingest_and_index_with_pdf_reader(filepath, PERSIST_DIR)
            st.success("Upload file successfully!")

    conversation = st.sidebar.text_input("Enter your topic:")
    if conversation:
        st.sidebar.write("Your conversation will be saved as : ", conversation)
        st.session_state.conversation = conversation

# Save chat history
def auto_save_conversation(messages, name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_history/{name}.json"
    with open(filename, 'w') as file:
        json.dump(messages, file, indent=4)
    return filename

user_prompt = st.chat_input("Ask me anything about the content of the PDF:")
if user_prompt:
    retriver = learning_agent.retriever_rerank(PERSIST_DIR)
    st.session_state.messages.append({'role': 'user', "content": user_prompt})
    response, _ = learning_agent.query_normal(retriver, user_prompt)
    # st.session_state.messages.append({'role': 'assistant', "content": response.response})
    # streaming
    st.session_state.messages.append({'role': 'assistant', "content": response.response_txt})
    st.session_state.all_QA.append({
        "id": st.session_state.qa_id,
        "user": user_prompt,
        "answer": response.response_txt
    })
    st.session_state.qa_id += 1
    # Auto save conversation
    print(st.session_state.conversation)
    filename = auto_save_conversation(st.session_state.all_QA, st.session_state.conversation)
    st.success(f"Conversation auto-saved to {filename}")


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])


