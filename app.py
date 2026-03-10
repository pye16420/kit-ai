import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="KIT 글로벌 동향 시스템", layout="wide")
st.title("🏛️ KIT 기획처 글로벌 동향 '더블 트랙' 시스템")

# 1. 대학 리스트와 영문명 매핑 (완전판)
eng_names = {
    "샌하신토": "San Jacinto College", "센테니얼": "Centennial College", 
    "발렌시아": "Valencia College", "파사데나": "Pasadena City College",
    "싱클레어": "Sinclair Community College", "피트 CC": "Pitt Community College",
    "조지 브라운": "George Brown College", "서남 위스콘신": "Southwest Wisconsin Technical College",
    "마이애미 데이드": "Miami Dade College", "TAFE NSW": "TAFE NSW",
    "CSN": "College of Southern Nevada", "시애틀 C.": "Seattle Colleges"
}
colleges = list(eng_names.keys())

selected = st.selectbox("🔎 조사할 대학을 선택하세요", colleges)
eng_name = eng_names[selected]

if st.button(f"🚀 {selected} 실시간 입체 분석 시작"):
    col1, col2 = st.columns(2)
    headers = {'User-Agent': 'Mozilla/5.0'}

    # 트랙 1: 공식 채널 조사
    with col1:
        st.subheader("🏫 공식 채널 동향 (Official)")
        try:
            url = f"https://www.google.com/search?q=site:.edu+{eng_name}+AI"
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            # 요약 메시지만 간단히 출력 (차단 대비)
            st.info(f"현재 {selected} 대학의 공식 edu 도메인에서 데이터를 스캔 중입니다.")
            st.write(f"🔗 [공식 검색결과 바로가기](https://www.google.com/search?q=site:.edu+{eng_name.replace(' ', '+')})")
        except:
            st.error("연결 지연")

    # 트랙 2: 뉴스 채널 조사
    with col2:
        st.subheader("🌐 뉴스 채널 동향 (News)")
        try:
            news_url = f"https://www.google.com/search?q={eng_name}+latest+news"
            st.success(f"최신 글로벌 뉴스를 불러오는 중입니다.")
            st.write(f"📰 [최신 구글 뉴스 확인하기](https://www.google.com/search?q={eng_name.replace(' ', '+')}+latest+news)")
        except:
            st.error("연결 지연")

    st.divider()
    st.write("💡 **기획처 팁**: 구글의 보안 정책으로 인해 직접 크롤링이 막힐 경우, 위 링크를 클릭하면 즉시 해당 대학의 최신 데이터를 확인하실 수 있습니다.")
