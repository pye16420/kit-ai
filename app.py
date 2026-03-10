import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="KIT 글로벌 동향 시스템", layout="wide")
st.title("🏛️ KIT 기획처 글로벌 동향 '더블 트랙' 시스템")

eng_names = {
    "샌하신토": "San Jacinto College",
    "센테니얼": "Centennial College",
    "발렌시아": "Valencia College",
    "파사데나": "Pasadena City College",
    "싱클레어": "Sinclair Community College",
    "피트 CC": "Pitt Community College",
    "조지 브라운": "George Brown College",
    "서남 위스콘신": "Southwest Wisconsin Technical College",
    "마이애미 데이드": "Miami Dade College",
    "CSN": "College of Southern Nevada",
    "시애틀 C.": "Seattle Colleges"
}
colleges = list(eng_names.keys())

selected = st.selectbox("🔎 조사할 대학을 선택하세요", colleges)
eng_name = eng_names.get(selected, selected)

if st.button(f"🚀 {selected} 실시간 입체 분석 시작"):
    col1, col2 = st.columns(2)
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    # 트랙 1: 공식 홈페이지(edu 도메인) 내부 정보 우회 크롤링
    with col1:
        st.subheader("🏫 공식 채널 동향 (Official)")
        with st.spinner('공식 자료 수집 중...'):
            try:
                # site:.edu 연산자를 사용해 공식 홈페이지 내용만 검색
                official_url = f"https://www.google.com/search?q=site:.edu+{eng_name}+AI+administrative"
                res = requests.get(official_url, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                items = soup.select('.tF2Cxc') # 구글 검색 결과 클래스
                
                if items:
                    for i, item in enumerate(items[:3]):
                        title = item.select_one('.LC20lb').text
                        link = item.select_one('.yuRUbf a')['href']
                        st.write(f"🔹 **{title}**")
                        st.caption(f"[공식 문서 확인]({link})")
                else:
                    st.write("발견된 공식 문서가 없습니다.")
            except:
                st.error("공식 채널 연결에 실패했습니다.")

    # 트랙 2: 구글 뉴스 실시간 평판 크롤링
    with col2:
        st.subheader("🌐 뉴스 채널 동향 (News)")
        with st.spinner('최신 뉴스 수집 중...'):
            try:
                news_url = f"https://www.google.com/search?q={eng_name}+College+latest+news&tbm=nws"
                res = requests.get(news_url, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                news_items = soup.select('.SoSUEf') # 구글 뉴스 레이아웃 클래스
                
                if news_items:
                    for i, item in enumerate(news_items[:3]):
                        st.write(f"📰 {item.get_text()[:80]}...")
                else:
                    st.write("최근 보도된 뉴스가 없습니다.")
                    st.markdown(f"[구글 뉴스에서 직접보기](https://www.google.com/search?q={eng_name}+news)")
            except:
                st.error("뉴스 채널 연결에 실패했습니다.")
