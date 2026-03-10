import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="KIT 전략 벤치마킹", layout="wide")
st.title("🏛️ KIT 기획처 글로벌 12개 대학 '더블 트랙' 통합 분석")

# 1. 대상 대학 및 도메인 정보 (정확한 검색을 위해 도메인 추가)
colleges = {
    "샌하신토": ["San Jacinto College", "sanjac.edu"],
    "센테니얼": ["Centennial College", "centennialcollege.ca"],
    "발렌시아": ["Valencia College", "valenciacollege.edu"],
    "파사데나": ["Pasadena City College", "pasadena.edu"],
    "싱클레어": ["Sinclair Community College", "sinclair.edu"],
    "피트 CC": ["Pitt Community College", "pittcc.edu"],
    "조지 브라운": ["George Brown College", "georgebrown.ca"],
    "서남 위스콘신": ["Southwest Wisconsin Technical College", "swtc.edu"],
    "마이애미 데이드": ["Miami Dade College", "mdc.edu"],
    "TAFE NSW": ["TAFE NSW Australia", "tafensw.edu.au"],
    "CSN": ["College of Southern Nevada", "csn.edu"],
    "시애틀 C.": ["Seattle Colleges", "seattlecolleges.edu"]
}

# 2. 분석 주제 선택
themes = ["AI 행정 및 자동화", "유학생 유치 및 지원 정책", "지역 산업체 산학협력", "최신 캠퍼스 시설 및 보건"]
selected_theme = st.selectbox("🎯 실시간 조사할 전략 주제를 선택하세요", themes)

if st.button("🚀 12개 대학 공식/뉴스 일괄 조사 시작"):
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    headers = {'User-Agent': 'Mozilla/5.0'}

    for i, (kor_name, info) in enumerate(colleges.items()):
        eng_name, domain = info[0], info[1]
        status_text.text(f"🔍 {kor_name} 대학 분석 중... ({i+1}/12)")
        
        # 트랙 A: 공식 홈페이지(.edu) 타겟 검색
        try:
            official_query = f"site:{domain} {selected_theme}"
            off_res = requests.get(f"https://www.google.com/search?q={official_query}", headers=headers, timeout=5)
            off_soup = BeautifulSoup(off_res.text, 'html.parser')
            off_snippet = off_soup.select_one('.VwiC3b').get_text()[:60] + "..." if off_soup.select_one('.VwiC3b') else "공식 공지 없음"
        except: off_snippet = "연결 지연"

        # 트랙 B: 구글 뉴스 채널 검색
        try:
            news_query = f"{eng_name} {selected_theme} latest news"
            news_res = requests.get(f"https://www.google.com/search?q={news_query}", headers=headers, timeout=5)
            news_soup = BeautifulSoup(news_res.text, 'html.parser')
            news_snippet = news_soup.select_one('.VwiC3b').get_text()[:60] + "..." if news_soup.select_one('.VwiC3b') else "보도 자료 없음"
        except: news_snippet = "연결 지연"

        results.append({
            "대학명": kor_name,
            "🏫 공식 채널 현황": off_snippet,
            "🌐 대외 뉴스/평판": news_snippet
        })
        
        progress_bar.progress((i + 1) / 12)
        time.sleep(0.5) # 구글 차단 방지용

    status_text.success("✅ 12개 대학 조사가 모두 완료되었습니다!")
    
    # 3. 결과 표 출력 및 엑셀 다운로드
    final_df = pd.DataFrame(results)
    st.subheader(f"📊 {selected_theme} - 입체 분석 리포트")
    st.table(final_df)
    
    csv = final_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 조사 결과 엑셀(CSV) 저장", csv, f"KIT_Global_Trend.csv", "text/csv")
