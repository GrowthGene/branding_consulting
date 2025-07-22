import streamlit as st

st.title("SNS 브랜딩 컨설팅 프로그램")
st.write("시중 코치 방법 기반: 사전 설문으로 강점 발굴 → 페르소나 재정의 → BIO 최적화 (e.g., Ryan Zofay 스타일)")

# 사전 설문 (사용자 입력)
mission = st.text_input("브랜드 미션 (e.g., '선배로서 코칭'):", "")
passion = st.text_input("열정 분야 (e.g., '뉴스킨 제품'):", "")
expertise = st.text_input("전문성 (e.g., '출산 후 자기관리'):", "")
values = st.text_input("핵심 가치 (e.g., '신뢰, 성실'):", "")
target = st.text_input("타겟 고객 (e.g., '30-40대 여성'):", "")
pain = st.text_input("타겟 고민 (e.g., '뱃살'):", "")
gain = st.text_input("타겟 욕망 (e.g., '자신감 회복'):", "")

if st.button("브랜드 재창조 실행"):
    if all([mission, passion, expertise, values, target, pain, gain]):
        # 분석 및 재창조
        redefined_mission = f"재정의된 미션: {mission}을 넘어, {passion}으로 {gain}을 실현하는 {values}한 멘토."
        persona = f"페르소나: Empowering Sage - {expertise} 전문, 취약점 공유로 공감 유도 (e.g., '나도 {pain} 겪었어')."
        bio = f"인스타 BIO: {redefined_mission[:50]}✨ | {target}을 위한 {passion} 코치 | DM으로 상담!"
        hashtags = ["#브랜드변신", "#개인브랜딩", f"#{pain}극복", "#자기관리", "#여성성공"]
        
        # 출력
        st.subheader("[브랜드 재창조 결과]")
        st.write(redefined_mission)
        st.write(persona)
        st.write(bio)
        st.write("핵심 해시태그: " + ", ".join(hashtags))
        
        st.subheader("[장기 플랜: 초창기(강점 발굴), 중간(콘텐츠 빌드), 수익화(파트너십)]")
        st.write("1. 초창기: 주 3회 스토리 공유로 공감 쌓기.")
        st.write("2. 중간: 취약점 에피소드 포스트로 충성도 높이기.")
        st.write("3. 연결: 관계 마케팅으로 콜라보 유도 (e.g., Daria Astanaeva 방법).")
    else:
        st.error("모든 필드를 입력해주세요.")