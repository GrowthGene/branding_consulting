import streamlit as st
import random

# --- 페이지 설정 ---
st.set_page_config(page_title="SNS 브랜딩 컨설팅", page_icon="✨")

st.title("✨ SNS 브랜딩 자동 컨설팅 프로그램")
st.write("7가지 질문에 답변하면 당신만의 강력한 SNS 브랜딩 전략을 제안해 드립니다.")

# 페르소나 및 키워드 데이터 (시장 분석 기반)
personas = {
    "전문가": "신뢰의 현자 (Sage)",
    "경험 공유": "공감의 개척자 (Explorer)",
    "동기부여": "열정의 영웅 (Hero)",
    "정보 제공": "지혜로운 창조자 (Creator)"
}
emotional_hooks = ["재탄생", "새로운 시작", "완벽한 변신", "자신감 회복", "성장의 여정"]
cta_options = ["지금 바로 DM 주세요!", "프로필 링크 확인!", "무료 상담 신청하기!"]

# --- 입력 폼 ---
with st.form("branding_form"):
    st.header("📝 사전 설문")
    
    mission = st.text_input("1. 당신의 브랜드가 존재하는 이유는 무엇인가요? (미션)", placeholder="예: 운동을 통해 사람들의 건강한 삶을 돕는다.")
    passion = st.text_input("2. 당신이 가장 열정적으로 이야기할 수 있는 주제는 무엇인가요?", placeholder="예: 홈 트레이닝")
    expertise = st.text_input("3. 당신이 전문성을 가지고 있는 분야는 무엇인가요?", placeholder="예: 재활 필라테스 자격증 보유")
    core_value = st.text_input("4. 당신이 가장 중요하게 생각하는 핵심 가치는 무엇인가요?", placeholder="예: 꾸준함, 진정성")
    target_audience = st.text_input("5. 당신의 핵심 타겟 고객은 누구인가요?", placeholder="예: 30대 출산 후 여성")
    target_pain_point = st.text_input("6. 타겟 고객이 가장 해결하고 싶어하는 고민은 무엇인가요?", placeholder="예: 출산 후 늘어진 뱃살과 약해진 코어")
    target_desire = st.text_input("7. 타겟 고객이 궁극적으로 원하는 욕망은 무엇인가요?", placeholder="예: 임신 전의 몸매와 자신감을 되찾고 싶다.")

    submit_button = st.form_submit_button("브랜딩 전략 분석 시작")

# --- 분석 로직 및 결과 출력 ---
if submit_button:
    # 에러 핸들링
    if not all([mission, passion, expertise, core_value, target_audience, target_pain_point, target_desire]):
        st.error("🚨 모든 필드를 입력해주세요!")
    else:
        st.success("🎉 분석이 완료되었습니다! 아래에서 결과를 확인하세요.")

        # 1. 재정의된 브랜드 미션 생성
        hook = random.choice(emotional_hooks)
        redefined_mission = f"단순히 '{passion}'을 넘어, '{target_audience}'가 '{target_pain_point}'을 극복하고 '{target_desire}'를 실현하도록 돕는 '{core_value}'의 멘토. 당신의 '{hook}'을 함께합니다."
        
        # 2. 페르소나 정의
        # 간단한 로직: 전문성과 열정의 교집합을 기반으로 페르소나 추천
        persona_key = "전문가" if "자격증" in expertise or "코치" in expertise else "경험 공유"
        persona = personas.get(persona_key, "공감의 개척자 (Explorer)")
        vulnerability_point = f"저 또한 과거에 '{target_pain_point}'으로 고생했지만 극복한 경험이 있습니다." # Ryan Zofay의 '취약점' 강조

        # 3. 인스타 BIO 생성 (Kait LeDonne 최적화)
        emoji_list = ["✨", "💪", "💡", "🚀", "❤️"]
        bio_emoji = random.choice(emoji_list)
        bio = f"{persona.split(' (')[0]} {bio_emoji} | {mission} | {target_audience} 전문 | {vulnerability_point.split(' ')[0]} 극복 스토리 | {random.choice(cta_options)}"
        
        # 4. 핵심 해시태그 생성
        hashtags = [
            f"#{passion.replace(' ', '')}",
            f"#{target_pain_point.split(' ')[0]}극복",
            f"#{target_audience.split(' ')[0]}",
            f"#{core_value.split(',')[0]}",
            f"#{hook}챌린지"
        ]

        # 5. 장기 플랜 (Daria Astanaeva의 관계 마케팅 기반)
        long_term_plan = {
            "초창기 (1-3개월)": "진정성 있는 소통과 '취약점' 공유를 통해 초기 팬들과 깊은 유대감 형성. 댓글과 DM에 100% 답장하며 관계 구축.",
            "중간 (4-9개월)": "타겟 고객의 고민 해결에 집중하는 정보성/참여형 콘텐츠(Q&A, 챌린지)로 전문성 입증 및 커뮤니티 활성화.",
            "수익화 (10개월 이후)": "구축된 신뢰를 바탕으로 소수 정예 그룹 코칭, 온라인 VOD 등 고부가가치 상품 제안. 커뮤니티 기반의 자연스러운 전환 유도."
        }

        # --- 결과 디스플레이 ---
        st.divider()
        st.header("📊 당신을 위한 맞춤 브랜딩 전략")

        st.subheader("1. 재정의된 브랜드 미션")
        st.info(redefined_mission)

        st.subheader("2. 브랜드 페르소나")
        st.info(f"**페르소나:** {persona}\n\n**스토리텔링 포인트:** '{vulnerability_point}'와 같이 당신의 취약점을 솔직하게 공유하며 타겟 고객과 강력한 공감대를 형성하세요.")

        st.subheader("3. 인스타그램 BIO (50자 내외 최적화)")
        st.info(f"**추천 BIO:**\n\n{bio}")
        st.caption("위 BIO를 기반으로 자유롭게 수정하여 사용하세요.")

        st.subheader("4. 핵심 해시태그 5가지")
        st.info('  |  '.join(hashtags))
        st.caption("콘텐츠 발행 시 위 해시태그를 기반으로 관련 해시태그를 추가하여 사용하세요.")
        
        st.subheader("5. 장기 성장 플랜 (관계 마케팅 기반)")
        for stage, plan in long_term_plan.items():
            st.write(f"**{stage}:** {plan}")
