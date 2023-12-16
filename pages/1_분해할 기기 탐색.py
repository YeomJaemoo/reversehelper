from googleapiclient.discovery import build
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="분해할 기기 탐색🔭", 
    page_icon="🛠️"
)
st.title("🔭분해할 기기: :red[유튜브]로 :red[탐색]하기")
st.divider()
st.subheader("🔎아래의 검색창에 분해할 기기의 명칭을 넣어 보자")
st.divider()

# API 키 입력
api_key = 'AIzaSyDMXxkKZ4vL0vOW8LbA92tz6s15hhrRn5g'

youtube = build('youtube', 'v3', developerKey=api_key)

def get_data_from_youtube(word):
    search_response = youtube.search().list(
        q=word,
        part='snippet',
        maxResults=10
    ).execute()

    titles = []
    urls = []
    thumbnails = []

    for search_result in search_response.get('items', []):
        titles.append(search_result['snippet']['title'])
        urls.append(f"https://www.youtube.com/watch?v={search_result['id']['videoId']}")
        thumbnails.append(search_result['snippet']['thumbnails']['default']['url'])

    df = pd.DataFrame({
        '제목': titles,
        '링크': urls,
        '이미지 URL': thumbnails
    })

    return df

user_input = st.text_input("모델명을 입력하세요(예: note5, 노트5):")

if user_input:
    search_word = user_input + " disassembly"
    df = get_data_from_youtube(search_word)
    st.dataframe(df)

    for i in range(len(df)):
        st.subheader(df.loc[i, '제목'])
        st.image(df.loc[i, '이미지 URL'])
        st.markdown(f"[동영상 바로가기]({df.loc[i, '링크']})")
        st.write("---")
