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
import review_agent
import openai

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

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {'role': 'assistant', "content": 'Hello! Upload a PDF and ask me anything about its content.'}]

if 'all_QA' not in st.session_state:
    st.session_state.all_QA = []

if 'qa_id' not in st.session_state:
    st.session_state.qa_id = 0

# 随机选择一个QA文件，然后从该文件中随机选择一个QA对话
def get_random_qa_pair(name):
    chat_files = [f for f in os.listdir(CHAT_HISTORY_DIR) if f ==(f"{name}.json")]

    if not chat_files:
        return None, None  # 如果没有文件，返回None

    # 从目录中随机选择一个文件
    selected_file = random.choice(chat_files)

    # 读取文件并提取所有聊天记录
    with open(f"{CHAT_HISTORY_DIR}/{selected_file}", 'r') as file:
        chat_data = json.load(file)

    # 确保文件中有内容
    if len(chat_data) > 0:
        # 从聊天记录中随机选择一个QA对
        random_index = random.randint(0, len(chat_data) - 1)
        selected_qa = chat_data[random_index]
        return selected_qa['user'], selected_qa['answer']

    return None, None  # 如果文件中没有聊天记录



# New code from here
    # 获取随机QA对

# 侧边栏
st.title("Settings")
# New code from here

import os

folder_path = 'chat_history'
file_names = []

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.json'):  # 只处理JSON文件
            file_name, _ = os.path.splitext(file)  # 分割文件名和扩展名
            file_names.append(file_name)  # 只添加文件名到列表中

# 打印文件名列表
for name in file_names:
    print(name)

print(file_names)




topic = st.selectbox('Select a topic to review', file_names)
user, answer = get_random_qa_pair(topic)
print(user, answer)

if user is not None and answer is not None:
    # 存储到会话状态中
    openai.api_type = "openai" 
    # 使用新版 OpenAI 客户端创建 Completion
    prompt = f"Follow the 2 steps:    1. Generate 3 questions similar to this: {user}.    2. Then expand knowledge points from {answer}."
    response =  openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
            "role": "user",
            "content": prompt,
            },
        ],
    )

    similar_question = response.choices[0].message.content
    # print("qa:",similar_question)

    st.session_state['current_qa_pair'] = {'user': user, 'answer': answer, 'similar_question': similar_question}
    # st.rerun()  # 触发刷新以更新显示
else:
    st.write("No QA pairs found.")

# If Review Mode is activated and we have a QA pair
if 'current_qa_pair' in st.session_state:
    # 刷新按钮
    if st.button("Refresh QA"):
        user, answer = get_random_qa_pair(name=topic)

        if user is not None and answer is not None:
            # 尝试生成类似问题
            try:
                openai.api_type = "openai" 
                # 使用新版 OpenAI 客户端创建 Completion
                prompt = f"Follow the 2 steps:    1. Generate 3 questions similar to this: {user}.    2. Then expand knowledge points from {answer}."
                response =  openai.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    messages=[
                        {
                        "role": "user",
                        "content": prompt,
                        },
                    ],
                )

                similar_question = response.choices[0].message.content
                # print("qa:",similar_question)

                st.session_state['current_qa_pair'] = {'user': user, 'answer': answer, 'similar_question': similar_question}
                st.experimental_rerun()  # 触发刷新

            except Exception as e:
                st.error(f"Error generating similar question: {e}")

        else:
            st.write("No QA pairs found.")

    st.write("Random QA Pair:")
    qa_pair = st.session_state['current_qa_pair']
    # print("qapair:",qa_pair)
    user = qa_pair.get("user", "Unknown")
    answer = qa_pair.get("answer", "No answer")
    similar_question = qa_pair.get("similar_question", "Not available")

    st.write(f"User: {user}")
    st.write(f"Answer: {answer}")

    st.write("Question Prompting and Knowledge Point Expansion:")
    st.write(similar_question)


# New code ends here
