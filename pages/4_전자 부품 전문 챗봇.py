import openai
import streamlit as st
from streamlit_chat import message
import os
import base64
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(
    page_title="3_an_electronic_component_helper",
    page_icon="🧷"
)
def create_prompt(
    query,
    system_role=f"""You're a professional expert who knows electronic devices well, and what the electronic components do.In particular, it's a kind expert who is very good at solving mobile phones.The man who developed this system is a technology teacher of Yeom Chang Middle School.
    """,
    model='gpt-4o-mini',
    stream=True
):
    user_content = f"""User question: "{str(query)}". """

    messages = [
        {"role": "system", "content": system_role},
        {"role": "user", "content": user_content}
    ]
    return messages

def generate_response(messages):
    with st.spinner("작성 중..."):
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.4,
            max_tokens=500)
    return result['choices'][0]['message']['content']

st.image('images/ask_me_chatbot3.png')

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if st.button('기존 체팅 삭제'):
    st.session_state['generated'] = []
    st.session_state['past'] = []
autocomplete = st.toggle("예시로 채우기를 통해 프롬프트 잘 활용해볼까?")
example={
    "prompt": "핸드폰에서 메인보드가 하는 역할을 100자 내외로 말해줘!"
}

with st.form('form', clear_on_submit=True):
    user_input = st.text_input('😎전자 부품이 해당 기기에서의 역할은?',
                               value= example["prompt"] if autocomplete else "",
                                 key='input')
    submitted = st.form_submit_button('Send')

if submitted and user_input:
    # 프롬프트 생성 후 프롬프트를 기반으로 챗봇의 답변을 반환
    prompt = create_prompt(user_input)
    chatbot_response = generate_response(prompt)
    st.balloons()
    
    
    st.session_state['past'].append(user_input)
    st.session_state["generated"].append(chatbot_response)
        
if st.session_state['generated']:
    for i in reversed(range(len(st.session_state['generated']))):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))





# 챗봇의 대화 내용을 저장하고 다운로드 링크를 생성하는 함수
def save_and_download_chat(past, generated):
    chat_content = ""

    for user_msg, chatbot_msg in zip(past, generated):
        chat_content += "사용자: " + user_msg + "\n"
        chat_content += "챗봇: " + chatbot_msg + "\n"
        chat_content += "---" + "\n"

    # 대화 내용을 텍스트 파일로 저장하고 다운로드 링크 생성
    b64 = base64.b64encode(chat_content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="chat_history.txt">대화 내용 다운로드</a>'
    st.markdown(href, unsafe_allow_html=True)

# 사용자가 '챗봇 내용을 저장' 버튼을 누르면 대화 내용을 저장하고 다운로드 링크를 생성
if st.button('챗봇 내용을 저장'):
    save_and_download_chat(st.session_state['past'], st.session_state['generated'])
