import streamlit as st
import os

os.chdir(os.getcwd())
st.set_page_config(
    page_title="분해도구 안전 사용법❤️", 
    page_icon="🛠️"
)

st.image('images/1.png')
st.divider()
st.subheader("_🔩분해 도구의 명칭을 클릭 후 확인해보기!🧹_")

st.divider()

tool = [
    {
        "name": "🔑분해도구세트",
        "type": "사용법 보기",
        "image": r'images/2.png',
        "info": r'images/8.png'
    },
    {
        "name": "🔧드라이버세트",
        "type": "사용법 보기",
        "image": r"images/3.png",
        "info": r'images/10.png'
    },
    {
        "name": "🚏스크린흡입컵",
        "type": "사용법 보기",
        "image": r"images/4.png",
        "info": r'images/9.png'
    },
    {
        "name": "🐱‍🏍히팅기",
        "type": "사용법 보기",
        "image": r"images/5.png",
        "info": r'images/11.png'
    },
    {
        "name": "🥃라이터 오일",
        "type": "사용법 보기",
        "image": r"images/6.png",
        "info": r'images/12.png'
    },
    {
        "name": "✋제전 장갑",
        "type": "사용법 보기",
        "image": r"images/7.png",
        "info": r'images/13.png'
    }
]


for i in range(0,len(tool),3):
    row_tool = tool[i:i+3]
    cols = st.columns(3)
    
    for j in range(len(row_tool)):
        with cols[j%3]:
            current_pet = row_tool[j]
            st.subheader(current_pet["name"])
            st.image(current_pet["image"])
            with st.expander(label=current_pet["type"], expanded=False):
                st.image(current_pet["info"])
             
