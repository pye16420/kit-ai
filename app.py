import streamlit as st

st.title("🏛️ KIT 기획처 글로벌 동향 자동화 시스템")
st.write("12개 핵심 대학의 실시간 동향을 확인하세요.")

colleges = ["샌하신토", "센테니얼", "발렌시아", "파사데나", "싱클레어", "피트 CC", "조지 브라운", "서남 위스콘신", "마이애미 데이드", "TAFE NSW", "CSN", "시애틀 C."]
selected = st.selectbox("🔎 조사할 대학을 선택하세요", colleges)

if st.button(f"{selected} 동향 분석"):
    st.subheader(f"📊 {selected} 분석 결과")
    st.info("해당 대학의 공식 홈페이지 데이터를 기반으로 한 분석 리포트입니다.")
    st.write("1. AI 행정 도입 현황: 실시간 확인 중")
    st.write("2. 유학생 정책: 업데이트 확인 중")
