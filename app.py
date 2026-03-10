import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="KIT 실시간 벤치마킹", layout="wide")
st.title("🏛️ KIT 기획처 글로벌 12개 대학 실시간 주제 분석")

# 1. 대상 대학 영문명 매핑
colleges = {
    "샌하신토": "San Jacinto College", "센테니얼": "Centennial College", 
    "발렌시아": "Valencia College", "파사데나": "Pasadena City College",
    "싱클레어": "Sinclair Community College", "피트 CC": "Pitt Community College",
    "조지 브라운": "George Brown College", "서남 위스콘신": "Southwest Wisconsin Technical College",
    "마이애미 데이드": "Miami Dade College", "TAFE NSW": "TAFE NSW Australia",
    "CSN": "College of Southern Nevada", "시애틀 C.": "Seattle Colleges"
}

# 2. 분석 주제 설정
themes = ["AI 행정 및 자동화", "유학생 유치 및 지원 정책", "지역 산업체 산학협력", "최신 캠퍼스 시설 혁신"]
selected_theme = st.selectbox("🎯 실시간 조사할 전략 주제를 선택하세요", themes)

if st.button("🚀 12개 대학 일괄 크롤링 시작"):
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    headers = {'User-Agent': 'Mozilla/5.0'}

    # 12개 대학 순회 조사
    for i, (kor_name, eng_name) in enumerate(colleges.items()):
        status_text.text(f"🔍 {kor_name} 대학의 '{selected_theme}' 정보를 수집 중... ({i+1}/12)")
        
        try:
            # 주제와 대학명을 조합해 구글 검색 (가장 안정적인 방식)
            search_query = f"{eng_name} {selected_theme} latest news initiatives"
            url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
            
            res = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # 검색 결과의 첫 번째 스니펫 요약 가져오기
            snippet = soup.select_one('.VwiC3b') # 구글 검색 요약문 클래스
            summary = snippet.get_text()[:150] + "..." if snippet else "최신 관련 문서를 찾는 중입니다."
            
            results.append({"대학명": kor_name, "실시간 조사 결과(요약)": summary})
        except:
            results.append({"대학명": kor_name, "실시간 조사 결과(요약)": "연결 일시 지연 (직접 확인 필요)"})
        
        # 진행 바 업데이트
        progress_bar.progress((i + 1) / 12)
        time.sleep(0.5) # 구글 차단 방지를 위한 짧은 휴식

    status_text.success("✅ 12개 대학 조사가 완료되었습니다!")
    
    # 3. 결과 표 출력
    final_df = pd.DataFrame(results)
    st.subheader(f"📊 {selected_theme} - 글로벌 벤치마킹 리포트")
    st.table(final_df)
    
    # 엑셀 저장용 데이터 제공
    csv = final_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 조사 결과 엑셀(CSV) 다운로드", csv, f"KIT_Global_Trend_{selected_theme}.csv", "text/csv")
