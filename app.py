import streamlit as st
import pandas as pd

st.set_page_config(page_title="KIT 글로벌 전략 대시보드", layout="wide")
st.title("🏛️ KIT 기획처 글로벌 대학 '더블 트랙' 분석 센터")

# 대학 정보 데이터베이스 (기획처 자산)
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

# 분석 주제 설정
themes = ["AI 행정 및 자동화", "유학생 유치 및 지원 정책", "지역 산업체 산학협력", "최신 캠퍼스 혁신"]
selected_theme = st.selectbox("🎯 분석할 전략 주제를 선택하세요", themes)

st.divider()

# 12개 대학 일괄 리스트 출력 (차단 없는 링크 방식)
st.subheader(f"📊 {selected_theme} - 글로벌 대학별 원터치 분석 리포트")

results = []
for kor_name, info in colleges.items():
    eng_name, domain = info[0], info[1]
    
    # 구글 검색용 URL 생성 (공식 vs 뉴스)
    off_link = f"https://www.google.com/search?q=site:{domain}+{selected_theme.replace(' ', '+')}"
    news_link = f"https://www.google.com/search?q={eng_name.replace(' ', '+')}+{selected_theme.replace(' ', '+')}+latest+news"
    
    results.append({
        "대학명": kor_name,
        "🏫 공식 채널 (edu)": f"[공식자료 확인]({off_link})",
        "🌐 대외 뉴스 (News)": f"[최신뉴스 확인]({news_link})"
    })

# 예쁜 표로 출력
df = pd.DataFrame(results)
st.write("💡 대학별 '확인' 링크를 클릭하면 실시간 데이터로 즉시 이동합니다.")
st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

st.divider()
st.info("💡 **기획처 팁**: 구글 크롤링 차단을 피하면서도 가장 빠르고 정확하게 12개 대학의 원문을 대조할 수 있는 방식입니다.")
