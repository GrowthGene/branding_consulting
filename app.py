import streamlit as st
import random

# --- 페이지 설정 ---
st.set_page_config(page_title="프리미엄 브랜딩 컨설팅", page_icon="👑")

# --- 전문가 데이터베이스 ---
# 칼 융의 12가지 브랜드 원형(Archetype)
archetypes = {
    "The Innocent": ("순수", "낙관, 정직, 순수함. 고객에게 안정감과 행복을 약속합니다.", ["🌈", "😊", "✨"]),
    "The Explorer": ("탐험가", "자유, 모험, 발견. 고객이 스스로를 발견하고 세상의 새로움을 경험하도록 이끕니다.", ["🚀", "🌍", "🧭"]),
    "The Sage": ("현자", "지혜, 진실, 지식. 깊이 있는 정보와 분석으로 고객이 현명한 결정을 내리도록 돕습니다.", ["📚", "💡", "🧠"]),
    "The Hero": ("영웅", "용기, 극복, 역경. 어려운 과제를 해결하고 세상에 족적을 남기도록 고객을 고무합니다.", ["💪", "🏆", "🔥"]),
    "The Outlaw": ("무법자", "혁명, 파괴, 자유. 기존의 틀을 깨고 새로운 길을 제시하며 변화를 주도합니다.", ["💥", "🏴‍☠️", "🤘"]),
    "The Magician": ("마법사", "비전, 변혁, 꿈의 실현. 불가능해 보이는 것을 가능하게 만드는 놀라운 경험을 선사합니다.", ["🔮", "✨", "🌌"]),
    "The Jester": ("광대", "재미, 유머, 긍정. 삶을 즐기고 현재를 만끽하도록 유쾌한 에너지를 전달합니다.", ["😂", "🎉", "🎈"]),
    "The Lover": ("연인", "친밀감, 열정, 관계. 고객이 사랑받고 소중히 여겨지는 특별한 감정을 느끼게 합니다.", ["❤️", "🌹", "💋"]),
    "The Caregiver": ("조력자", "돌봄, 공감, 보호. 고객을 보호하고 돕는 데 헌신하며 이타적인 모습을 보입니다.", ["🤗", "💖", "🤝"]),
    "The Ruler": ("지배자", "통제, 리더십, 권위. 혼돈 속에서 질서를 잡고 성공과 번영을 이끄는 리더의 모습을 보입니다.", ["👑", "🏛️", "💎"]),
    "The Creator": ("창조자", "혁신, 창의성, 자기표현. 상상력을 발휘하여 새롭고 가치 있는 것을 만들어냅니다.", ["🎨", "💡", "✍️"]),
    "The Everyman": ("보통사람", "소속감, 현실성, 공감. 누구나 쉽게 공감하고 어울릴 수 있는 친근한 브랜드입니다.", ["🙂", "🍻", "👍"])
}
# 스토리브랜드 7가지 요소
storybrand_elements = ["캐릭터(고객)", "난관에 직면하다", "가이드(당신)를 만나다", "계획을 제시하다", "행동을 촉구하다", "실패를 피하도록 돕다", "성공으로 끝나다"]

# --- UI ---
st.title("👑 프리미엄 SNS 브랜딩 컨설팅 (v2.0)")
st.info("100만 원 가치의 코칭 방법론을 담았습니다. 심층 질문에 답변하여 '대체 불가능한 브랜드'를 구축하세요.")

with st.form("premium_branding_form"):
    st.header("Step 1: 당신의 'WHY' 발견하기 (Golden Circle)")
    why = st.text_area("1-1. 모든 돈과 시간의 제약이 없다면, 당신이 세상에 어떤 긍정적 영향을 미치고 싶나요? (당신의 존재 이유, WHY)", placeholder="예: 사람들이 타인의 시선에서 벗어나 온전한 자신만의 삶을 사는 세상을 만들고 싶다.")
    how = st.text_area("1-2. 그 영향을 어떤 독창적인 방식으로 만들어낼 건가요? (차별화된 방식, HOW)", placeholder="예: 글쓰기와 심리학을 결합한 '내면 탐색 글쓰기' 프로그램을 통해서")
    what = st.text_input("1-3. 그래서 구체적으로 무엇을 제공하나요? (제품/서비스, WHAT)", placeholder="예: 온라인 글쓰기 코칭, 전자책, 워크숍")

    st.header("Step 2: 고객의 욕망 파헤치기 (StoryBrand)")
    customer = st.text_input("2-1. 당신의 고객은 누구인가요?", placeholder="예: 일과 삶 사이에서 정체성을 잃어버린 30대 직장인 여성")
    problem_external = st.text_input("2-2. 고객이 겪는 외부적 문제는 무엇인가요?", placeholder="예: 매일 반복되는 업무에 번아웃이 왔고, 무엇을 좋아하는지 모르겠다.")
    problem_internal = st.text_area("2-3. 그 문제 때문에 고객이 느끼는 내면의 감정(좌절감)은 무엇인가요?", placeholder="예: '이대로 내 인생이 끝나는 걸까?' 하는 불안감과 무기력함")
    problem_philosophical = st.text_input("2-4. 이것이 '왜' 잘못되었다고 생각하나요? (세상에 대한 신념)", placeholder="예: 누구나 자신만의 고유한 가치를 실현하며 살 권리가 있기 때문에")

    submit_button = st.form_submit_button("최고급 브랜딩 전략 분석")

if submit_button:
    if not all([why, how, what, customer, problem_external, problem_internal, problem_philosophical]):
        st.error("🚨 모든 심층 질문에 답변해야 정확한 분석이 가능합니다.")
    else:
        st.success("✨ 분석이 완료되었습니다. 당신의 브랜드는 새로운 차원으로 진화합니다.")
        st.divider()

        # 1. 브랜드 원형 분석
        # (실제로는 복잡한 로직 필요, 여기서는 WHY와 HOW 기반으로 단순 추론)
        primary_archetype_key = "The Sage" if "지식" in how or "분석" in how else "The Creator" if "만들" in why else "The Caregiver"
        secondary_archetype_key = "The Explorer" if "자유" in why else "The Hero" if "극복" in why else "The Jester"
        
        primary_name, primary_desc, primary_emoji = archetypes[primary_archetype_key]
        secondary_name, secondary_desc, _ = archetypes[secondary_archetype_key]

        st.header("📊 100만 원 가치의 컨설팅 결과")
        with st.expander("**[1] 브랜드 원형(Archetype) 분석: 당신의 영혼은 무엇을 말하는가?**", expanded=True):
            st.subheader(f"당신의 조합은 **'{primary_name} X {secondary_name}'** 입니다.")
            st.write(f"**- 주요 원형: {primary_name}** {primary_desc}")
            st.write(f"**- 보조 원형: {secondary_name}** {secondary_desc}")
            st.info("💡 **전략:** '현자'의 깊이 있는 지혜를 '탐험가'의 자유로운 방식으로 전달하세요. 고객은 당신을 통해 '안전하게 새로운 세상으로 나아가는 길'을 발견할 것입니다.")

        # 2. 골든 서클(WHY-HOW-WHAT) 기반 브랜드 에센스
        brand_essence = f"우리는 {why.split(' ')[0]}(WHY)라는 신념을 가지고, {how.split(' ')[0]}(HOW)을 통해, {what}(WHAT)을 제공합니다."

        # 3. 스토리브랜드(StoryBrand) 플롯 설계
        story_plot = f"""
        - **주인공(Hero):** {customer}
        - **고난(Problem):** {problem_external} 때문에 {problem_internal}을 느끼고 있습니다.
        - **가이드(Guide):** 바로 당신입니다. 당신은 그들의 고통을 이해하고 성공으로 이끌어줄 수 있습니다.
        - **계획(Plan):** 당신의 '{what}'은(는) 고객이 3단계(예: 1.자각 2.실행 3.변화)를 통해 문제를 해결하도록 돕는 명확한 계획입니다.
        - **성공(Success):** 당신의 도움으로 고객은 더 이상 무기력하지 않고, 자신만의 가치를 실현하는 삶을 살게 됩니다.
        """
        
        with st.expander("**[2] 스토리텔링 전략: 고객을 주인공으로 만들어라**"):
            st.subheader("- 골든 서클 기반 브랜드 에센스")
            st.write(brand_essence)
            st.subheader("- 스토리브랜드 플롯")
            st.text(story_plot)
            st.info("💡 **전략:** 모든 콘텐츠에서 당신이 주인공이 되지 마세요. 고객을 '주인공'으로, 당신을 '가이드'로 포지셔닝하여 신뢰를 얻으세요.")

        # 4. 실행 계획
        with st.expander("**[3] 실행 가이드: 브랜드를 살아 숨쉬게 하라**"):
            st.subheader("- 인스타그램 BIO (원형 + 스토리브랜드 적용)")
            bio_text = f"{primary_name} {random.choice(primary_emoji)} | {customer}를 위한 {what} | {problem_internal.split(' ')[0]} 해결사 | ⬇️ 무료 진단으로 변화 시작하기"
            st.code(bio_text, language=None)
            
            st.subheader("- 보이스 & 톤 가이드")
            st.write(f"**- 목소리:** {primary_name}처럼 차분하고 신뢰감 있게, 하지만 {secondary_name}처럼 가끔은 위트있게.")
            st.write("**- 금지어:** '절대', '무조건' 같은 단정적인 표현 대신 '...하는 경향이 있어요', '...라고 생각해볼 수 있어요' 사용.")
            
            st.subheader("- 핵심 콘텐츠 주제 (Pillar)")
            st.write(f"1. **WHY Pillar:** {why.split(' ')[0]} (우리가 이 일을 하는 이유)")
            st.write(f"2. **HOW Pillar:** {how.split(' ')[0]} (우리의 독창적인 해결 방식)")
            st.write(f"3. **WHAT Pillar:** {what} 고객 성공 사례 (우리 제품/서비스의 결과)")
