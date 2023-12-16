import streamlit as st
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup 
import pandas as pd
import time
st.set_page_config(
    page_title="분해할 기기 탐색🔭", 
    page_icon="🛠️"
)
st.title("분해할 기기 유튜브로 탐색하기")
st.divider()
st.subheader("아래의 검색창에 분해할 기기의 명칭을 넣어 보자")

st.divider()
def get_data_from_youtube(word, scroll=False):
    with st.spinner("분해 영상을 찾고 있습니다. 잠시만 기다려 주세요⏱"):
        options = Options() 
        options.add_argument("--headless=new")
        options.add_argument('--disable-gpu')
        driver = Chrome(options=options)

        base_url = "https://www.youtube.com"
        search_word = '/results?search_query=' + word
        search_option = "&sp=CAMSAhAB" # 조회수로 정렬

        url = base_url +  search_word + search_option # 접속하고자 하는 웹 사이트
        driver.get(url) # URL에 접속
        time.sleep(3) # 웹 브라우저를 실행하고 URL에 접속할 때까지 기다림  
        
        if(scroll==True):
            # 수직(Y축 방향)으로 스크롤 동작하기 
            y = 0 # Y축 방향으로 스크롤 이동할 거리 초기화
            y_step = 1000
            for k in range(1, 5): # 반복 횟수 지정
                y = y + y_step  # 반복할 때마다 Y축 방향으로 더해지는 거리를 지정
                script = "window.scrollTo({0},{1})".format(0, y)
                driver.execute_script(script) # Y축 방향으로 스크롤
                time.sleep(3) # 결과를 받아올 때까지 잠시 기다림

        html = driver.page_source # 접속 후에 해당 page의 HTML 코드를 가져옴
        
        soup = BeautifulSoup(html, 'lxml')
        
        # 동영상 제목과 URL 추출하기
        title_hrefs = soup.select('a#video-title')
        
        titles = []
        urls = []    
        for title_href in title_hrefs:
            title = title_href['title']         # 태그 안에서 title 속성의 값을 가져오기
            url = base_url + title_href['href'] # href 속성의 값 가져와 기본 url과 합치기        
            titles.append(title)
            urls.append(url)

        # 조회수와 업로드 시기 추출하기
        view_uploads = soup.select('span.style-scope.ytd-video-meta-block')
        
        view_numbers = view_uploads[0::2] # 인덱스가 짝수인 요소 선택
        upload_times = view_uploads[1::2] # 인덱스가 홀수인 요소 선택

        views = []
        uploads = [] 
        for view_number, upload_time in zip(view_numbers, upload_times):
            view = view_number.get_text().split(" ")[-1] # 조회수 추출
            upload = upload_time.get_text()              # 업로드 시기 추출
            views.append(view)
            uploads.append(upload)

        # 썸네일 이미지 URL 추출하기
        image_elements = soup.select('a#thumbnail img')
        image_urls = [image['src'] for image in image_elements if 'src' in image.attrs]

        # 추출된 정보를 모으기
        search_results = []
        for title, url, view, upload, image_url in zip(titles, urls, views, uploads, image_urls):
            search_result = [title, url, view, upload, image_url]
            search_results.append(search_result)
        
        # 추출 결과를 판다스 DataFrame 데이터 형식으로 변환
        df = pd.DataFrame(search_results, columns=["제목", "링크", "조회수", "업로드", "이미지 URL"])
        
        return df

# 스트림릿에서 사용자 입력 받기
user_input = st.text_input("모델명을 입력하세요(예: note5, 노트5):")

# 입력값이 비어있지 않을 때만 검색 수행
if user_input:
    # 입력받은 검색어에 "disassembly" 추가
    search_word = user_input + " disassembly"

    # 검색 결과 얻기
    df = get_data_from_youtube(search_word, scroll=True)
    st.dataframe(df)
    # 링크를 클릭 가능하게 만들기
    for i in range(len(df)):
        st.subheader(df.loc[i, '제목'])
        st.image(df.loc[i, '이미지 URL'])
        st.markdown(f"[동영상 바로가기]({df.loc[i, '링크']})")
        st.text(f"조회수: {df.loc[i, '조회수']}, 업로드: {df.loc[i, '업로드']}")
        st.write("---")
