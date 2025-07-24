import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import uuid

# 페이지 설정
st.set_page_config(
    page_title="Instagram Branding Expert",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #833AB4, #FD1D1D, #FCB045);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .section-header {
        background: linear-gradient(45deg, #833AB4, #FD1D1D);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #833AB4;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #833AB4, #FD1D1D);
        height: 10px;
        border-radius: 5px;
    }
    
    .survey-question {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #FCB045;
    }
</style>
""", unsafe_allow_html=True)

# 데이터 클래스 정의
@dataclass
class UserProfile:
    id: str
    business_stage: str
    business_type: str
    instagram_status: str
    target_age_group: str
    target_gender: str
    primary_goals: List[str]
    brand_archetype: str
    tone_scores: Dict[str, int]
    competitors: List[str]
    differentiation: List[str]
    time_available: str
    budget: str
    tools_available: List[str]
    created_at: str

@dataclass
class BrandStrategy:
    brand_type: str
    strategy_name: str
    content_pillars: List[str]
    posting_frequency: Dict[str, int]
    content_mix: Dict[str, int]
    recommended_tools: List[str]
    kpi_targets: Dict[str, float]
    weekly_plans: List[Dict]

# 설문 데이터 정의
SURVEY_DATA = {
    "business_stages": {
        "idea": "아이디어 단계 (아직 런칭 전)",
        "startup": "스타트업 (운영 1년 미만)", 
        "growth": "성장기 (운영 1-3년)",
        "mature": "안정기 (운영 3년 이상)"
    },
    
    "business_types": {
        "product": "제품 기반 비즈니스",
        "service": "서비스 기반 비즈니스",
        "digital": "디지털 제품/서비스",
        "creator": "크리에이터/인플루언서",
        "b2b": "B2B 비즈니스"
    },
    
    "instagram_statuses": {
        "none": "아직 계정이 없음",
        "personal": "개인 계정 보유",
        "business_small": "비즈니스 계정 (팔로워 100명 미만)",
        "business_medium": "비즈니스 계정 (팔로워 100-1000명)",
        "business_large": "비즈니스 계정 (팔로워 1000명 이상)"
    },
    
    "age_groups": {
        "18-24": "18-24세 (Gen Z)",
        "25-34": "25-34세 (젊은 밀레니얼)",
        "35-44": "35-44세 (기성 밀레니얼)",
        "45-54": "45-54세 (Gen X)",
        "55+": "55세 이상"
    },
    
    "primary_goals": {
        "awareness": "브랜드 인지도 향상",
        "traffic": "웹사이트 트래픽 증가",
        "leads": "리드 생성 및 잠재고객 확보",
        "sales": "직접 판매 증대",
        "community": "커뮤니티 구축 및 고객 충성도 향상",
        "expertise": "산업 내 전문성 인정",
        "partnerships": "인플루언서/파트너십 기회 창출"
    },
    
    "brand_archetypes": {
        "innocent": "The Innocent (순수함, 정직함)",
        "sage": "The Sage (지혜로움, 전문성)",
        "explorer": "The Explorer (모험적, 혁신적)",
        "outlaw": "The Outlaw (반항적, 혁명적)",
        "magician": "The Magician (변화 창조, 혁신)",
        "hero": "The Hero (용기있는, 결단력)",
        "lover": "The Lover (열정적, 로맨틱)",
        "jester": "The Jester (재미있는, 유머러스)",
        "everyman": "The Everyman (친근한, 접근 가능한)",
        "caregiver": "The Caregiver (보살피는, 돌보는)",
        "ruler": "The Ruler (권위적, 리더십)",
        "creator": "The Creator (창의적, 예술적)"
    }
}

# 전략 매칭 엔진
class StrategyEngine:
    def __init__(self):
        self.strategies = {
            "product_awareness": {
                "brand_type": "Product-First Visual Brand",
                "strategy_name": "인지도 우선 제품 브랜딩 전략",
                "content_pillars": ["제품 소개", "고객 사용 사례", "비하인드 스토리", "교육적 콘텐츠", "브랜드 스토리"],
                "posting_frequency": {"총_게시물": 12, "릴스": 8, "캐러셀": 3, "싱글포스트": 1},
                "content_mix": {"릴스": 70, "캐러셀": 25, "싱글포스트": 5},
                "recommended_tools": ["캔바 프로", "인스타그램 릴스", "해시태그 리서치 도구"],
                "kpi_targets": {"팔로워_증가율": 15.0, "참여율": 0.8, "도달률": 25.0}
            },
            "service_expertise": {
                "brand_type": "Expertise-Driven Authority Brand", 
                "strategy_name": "전문성 중심 권위 브랜딩 전략",
                "content_pillars": ["전문 지식 공유", "케이스 스터디", "업계 인사이트", "Q&A", "개인 스토리"],
                "posting_frequency": {"총_게시물": 10, "릴스": 4, "캐러셀": 5, "싱글포스트": 1},
                "content_mix": {"캐러셀": 50, "릴스": 40, "싱글포스트": 10},
                "recommended_tools": ["링크드인 연동", "캔바", "스토리 하이라이트"],
                "kpi_targets": {"팔로워_증가율": 10.0, "참여율": 1.2, "도달률": 20.0}
            },
            "creator_community": {
                "brand_type": "Personal Storytelling Brand",
                "strategy_name": "커뮤니티 중심 개인 브랜딩 전략", 
                "content_pillars": ["일상 공유", "팔로워 인터랙션", "라이브 콘텐츠", "협업", "개인 성장"],
                "posting_frequency": {"총_게시물": 14, "릴스": 6, "캐러셀": 4, "스토리": 20},
                "content_mix": {"릴스": 45, "캐러셀": 30, "스토리": 25},
                "recommended_tools": ["인스타그램 라이브", "스토리 인터랙션", "DM 자동화"],
                "kpi_targets": {"팔로워_증가율": 20.0, "참여율": 1.5, "커뮤니티_활동": 30.0}
            }
        }
    
    def match_strategy(self, profile: UserProfile) -> BrandStrategy:
        # 비즈니스 타입과 주요 목표를 기반으로 전략 매칭
        key = f"{profile.business_type}_{profile.primary_goals[0] if profile.primary_goals else 'awareness'}"
        
        if key in self.strategies:
            strategy_data = self.strategies[key]
        else:
            # 기본 전략
            strategy_data = self.strategies["product_awareness"]
        
        # 주간 계획 생성
        weekly_plans = self.generate_weekly_plans(profile, strategy_data)
        
        return BrandStrategy(
            brand_type=strategy_data["brand_type"],
            strategy_name=strategy_data["strategy_name"],
            content_pillars=strategy_data["content_pillars"],
            posting_frequency=strategy_data["posting_frequency"],
            content_mix=strategy_data["content_mix"],
            recommended_tools=strategy_data["recommended_tools"],
            kpi_targets=strategy_data["kpi_targets"],
            weekly_plans=weekly_plans
        )
    
    def generate_weekly_plans(self, profile: UserProfile, strategy_data: Dict) -> List[Dict]:
        plans = []
        for week in range(1, 13):  # 12주 계획
            if week <= 2:
                phase = "브랜드 파운데이션"
                tasks = [
                    "인스타그램 비즈니스 계정 설정 및 최적화",
                    "브랜드 아이덴티티 가이드 문서 작성",
                    "경쟁사 분석 및 벤치마킹",
                    "콘텐츠 필러 정의 및 스타일 가이드 작성"
                ]
            elif week <= 8:
                phase = "콘텐츠 전략 실행"
                tasks = [
                    f"{strategy_data['posting_frequency']['총_게시물']}개 포스트 제작 및 게시",
                    "스토리 인터랙티브 콘텐츠 일일 게시",
                    "댓글 및 DM 응답 (24시간 내)",
                    "주간 성과 분석 및 최적화"
                ]
            else:
                phase = "성장 가속화"
                tasks = [
                    "유료 광고 캠페인 테스트 런칭",
                    "인플루언서 협업 기획",
                    "UGC 캠페인 실행",
                    "크로스 플랫폼 콘텐츠 전략 구현"
                ]
            
            plans.append({
                "week": week,
                "phase": phase,
                "tasks": tasks,
                "kpi_focus": list(strategy_data["kpi_targets"].keys())[0] if strategy_data["kpi_targets"] else "팔로워 증가"
            })
        
        return plans

# 세션 상태 초기화
if 'survey_completed' not in st.session_state:
    st.session_state.survey_completed = False
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None
if 'strategy' not in st.session_state:
    st.session_state.strategy = None

# 메인 앱
def main():
    st.markdown('<h1 class="main-header">📸 Instagram Branding Expert</h1>', unsafe_allow_html=True)
    st.markdown("### 🚀 세계 최고의 SNS 브랜딩 전문가가 당신의 인스타그램 브랜딩을 도와드립니다")
    
    # 사이드바 네비게이션
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.selectbox(
        "페이지 선택",
        ["🏠 홈", "📝 브랜딩 설문조사", "📊 결과 및 전략", "📈 성과 대시보드", "📚 리소스"]
    )
    
    if page == "🏠 홈":
        show_home()
    elif page == "📝 브랜딩 설문조사":
        show_survey()
    elif page == "📊 결과 및 전략":
        show_results()
    elif page == "📈 성과 대시보드":
        show_dashboard()
    elif page == "📚 리소스":
        show_resources()

def show_home():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 🎯 2024-2025년 인스타그램 브랜딩의 새로운 표준
        
        **최신 트렌드 기반 전략적 접근**
        - 📹 **비디오 중심 전략**: 릴스 콘텐츠 최적화로 70% 높은 도달률
        - 🤝 **진정성 있는 커뮤니티**: DM 공유 중심의 알고리즘 최적화
        - 📊 **데이터 기반 의사결정**: 실시간 성과 분석과 전략 조정
        
        **체계적인 3단계 프로세스**
        1. **📋 정밀 진단**: 25개 핵심 질문으로 브랜드 DNA 분석
        2. **🎨 맞춤 전략**: AI 기반 개인화된 브랜딩 로드맵 제공
        3. **📈 지속 최적화**: 12주간 단계별 실행 가이드와 성과 추적
        """)
        
        if st.button("🚀 브랜딩 진단 시작하기", key="start_survey", type="primary"):
            st.session_state.current_page = "📝 브랜딩 설문조사"
            st.rerun()
    
    with col2:
        st.markdown("### 📊 플랫폼 현황 (2024-2025)")
        
        # 성과 지표 시각화
        metrics_data = {
            "포맷": ["캐러셀", "릴스", "스토리", "싱글포스트"],
            "참여율": [0.55, 0.50, 0.35, 0.25]
        }
        
        fig = px.bar(
            x=metrics_data["포맷"],
            y=metrics_data["참여율"],
            title="콘텐츠 포맷별 평균 참여율",
            color=metrics_data["참여율"],
            color_continuous_scale="Viridis"
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 **인사이트**: 캐러셀 포스트가 가장 높은 참여율을 보여주며, 스토리텔링에 최적화된 포맷입니다.")

def show_survey():
    st.markdown('<div class="section-header"><h2>📝 인스타그램 브랜딩 정밀 진단</h2></div>', unsafe_allow_html=True)
    
    # 진행률 표시
    progress = st.progress(0)
    progress_text = st.empty()
    
    with st.form("branding_survey"):
        # 섹션 1: 브랜드 기본 정보
        st.markdown('<div class="survey-question">', unsafe_allow_html=True)
        st.markdown("### 🏢 섹션 1: 브랜드 기본 정보")
        
        business_stage = st.selectbox(
            "현재 비즈니스 단계는?",
            options=list(SURVEY_DATA["business_stages"].keys()),
            format_func=lambda x: SURVEY_DATA["business_stages"][x],
            key="business_stage"
        )
        
        business_type = st.selectbox(
            "주요 사업 분야는?",
            options=list(SURVEY_DATA["business_types"].keys()),
            format_func=lambda x: SURVEY_DATA["business_types"][x],
            key="business_type"
        )
        
        instagram_status = st.selectbox(
            "인스타그램 계정 현재 상태는?",
            options=list(SURVEY_DATA["instagram_statuses"].keys()),
            format_func=lambda x: SURVEY_DATA["instagram_statuses"][x],
            key="instagram_status"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 섹션 2: 목표 및 우선순위
        st.markdown('<div class="survey-question">', unsafe_allow_html=True)
        st.markdown("### 🎯 섹션 2: 목표 및 우선순위")
        
        primary_goals = st.multiselect(
            "인스타그램을 통해 달성하고 싶은 주요 목표는? (우선순위별로 3개 선택)",
            options=list(SURVEY_DATA["primary_goals"].keys()),
            format_func=lambda x: SURVEY_DATA["primary_goals"][x],
            max_selections=3,
            key="primary_goals"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 섹션 3: 타겟 오디언스
        st.markdown('<div class="survey-question">', unsafe_allow_html=True)
        st.markdown("### 👥 섹션 3: 타겟 오디언스 분석")
        
        target_age_group = st.selectbox(
            "주요 타겟 고객의 연령대는?",
            options=list(SURVEY_DATA["age_groups"].keys()),
            format_func=lambda x: SURVEY_DATA["age_groups"][x],
            key="target_age_group"
        )
        
        target_gender = st.select_slider(
            "타겟 고객의 성별 분포는?",
            options=["주로 여성", "여성 중심", "균등 분포", "남성 중심", "주로 남성"],
            value="균등 분포",
            key="target_gender"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 섹션 4: 브랜드 아이덴티티
        st.markdown('<div class="survey-question">', unsafe_allow_html=True)
        st.markdown("### 🎨 섹션 4: 브랜드 아이덴티티")
        
        brand_archetype = st.selectbox(
            "브랜드가 속하는 아키타입은?",
            options=list(SURVEY_DATA["brand_archetypes"].keys()),
            format_func=lambda x: SURVEY_DATA["brand_archetypes"][x],
            key="brand_archetype"
        )
        
        # 브랜드 톤앤보이스 슬라이더
        st.markdown("**브랜드 톤앤보이스의 특성을 설정해주세요:**")
        
        col1, col2 = st.columns(2)
        with col1:
            formal_casual = st.slider("공식적 ↔ 캐주얼", 1, 10, 5, key="formal_casual")
            serious_fun = st.slider("진지함 ↔ 재미있음", 1, 10, 5, key="serious_fun")
        with col2:
            polite_bold = st.slider("정중함 ↔ 과감함", 1, 10, 5, key="polite_bold")
            factual_passionate = st.slider("사실적 ↔ 열정적", 1, 10, 5, key="factual_passionate")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 섹션 5: 경쟁사 분석
        st.markdown('<div class="survey-question">', unsafe_allow_html=True)
        st.markdown("### 🏆 섹션 5: 경쟁사 및 차별화")
        
        competitors = []
        for i in range(3):
            competitor = st.text_input(f"주요 경쟁사 {i+1}의 인스타그램 계정명", key=f"competitor_{i}")
            if competitor:
                competitors.append(competitor)
        
        differentiation = st.multiselect(
            "경쟁사 대비 차별화 포인트는?",
            ["더 나은 품질/성능", "더 저렴한 가격", "더 우수한 고객 서비스", 
             "더 혁신적인 기술/접근법", "더 강한 브랜드 스토리", "더 전문적인 expertise",
             "더 개인적인/친근한 접근", "더 지속가능한/윤리적 접근"],
            key="differentiation"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 섹션 6: 리소스 평가
        st.markdown('<div class="survey-question">', unsafe_allow_html=True)
        st.markdown("### 💼 섹션 6: 리소스 및 실행 역량")
        
        time_available = st.selectbox(
            "주간 인스타그램 콘텐츠 제작에 투입 가능한 시간은?",
            ["2시간 미만", "2-5시간", "5-10시간", "10-20시간", "20시간 이상"],
            key="time_available"
        )
        
        budget = st.selectbox(
            "월간 인스타그램 마케팅 예산은?",
            ["예산 없음", "10만원 미만", "10-30만원", "30-50만원", "50-100만원", "100만원 이상"],
            key="budget"
        )
        
        tools_available = st.multiselect(
            "현재 보유한 콘텐츠 제작 도구는?",
            ["스마트폰 카메라", "전문 카메라", "조명 장비", "편집 소프트웨어", 
             "디자인 도구", "비디오 편집 도구"],
            key="tools_available"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 제출 버튼
        submitted = st.form_submit_button("🎯 브랜딩 전략 생성하기", type="primary")
        
        if submitted:
            # 필수 필드 검증
            if not all([business_stage, business_type, target_age_group, brand_archetype]):
                st.error("모든 필수 항목을 입력해주세요.")
                return
            
            # 사용자 프로필 생성
            user_profile = UserProfile(
                id=str(uuid.uuid4()),
                business_stage=business_stage,
                business_type=business_type,
                instagram_status=instagram_status,
                target_age_group=target_age_group,
                target_gender=target_gender,
                primary_goals=primary_goals,
                brand_archetype=brand_archetype,
                tone_scores={
                    "formal_casual": formal_casual,
                    "serious_fun": serious_fun,
                    "polite_bold": polite_bold,
                    "factual_passionate": factual_passionate
                },
                competitors=competitors,
                differentiation=differentiation,
                time_available=time_available,
                budget=budget,
                tools_available=tools_available,
                created_at=datetime.now().isoformat()
            )
            
            # 전략 생성
            engine = StrategyEngine()
            strategy = engine.match_strategy(user_profile)
            
            # 세션에 저장
            st.session_state.user_profile = user_profile
            st.session_state.strategy = strategy
            st.session_state.survey_completed = True
            
            st.success("🎉 브랜딩 전략이 성공적으로 생성되었습니다!")
            st.info("📊 '결과 및 전략' 페이지에서 맞춤형 가이드를 확인하세요.")

def show_results():
    if not st.session_state.survey_completed:
        st.warning("먼저 브랜딩 설문조사를 완료해주세요.")
        return
    
    profile = st.session_state.user_profile
    strategy = st.session_state.strategy
    
    st.markdown('<div class="section-header"><h2>📊 맞춤형 브랜딩 전략 결과</h2></div>', unsafe_allow_html=True)
    
    # 브랜드 타입 및 전략 개요
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### 🎯 브랜드 타입: **{strategy.brand_type}**")
        st.markdown(f"**전략명**: {strategy.strategy_name}")
        
        st.markdown("#### 📋 콘텐츠 필러 (5개)")
        for i, pillar in enumerate(strategy.content_pillars, 1):
            st.markdown(f"{i}. **{pillar}**")
    
    with col2:
        st.markdown("### 📊 콘텐츠 믹스 비율")
        fig = px.pie(
            values=list(strategy.content_mix.values()),
            names=list(strategy.content_mix.keys()),
            title="권장 콘텐츠 구성"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # KPI 목표 설정
    st.markdown("### 🎯 주요 성과 지표 (KPI) 목표")
    
    kpi_cols = st.columns(len(strategy.kpi_targets))
    for i, (kpi, target) in enumerate(strategy.kpi_targets.items()):
        with kpi_cols[i]:
            st.metric(
                label=kpi.replace("_", " ").title(),
                value=f"{target}{'%' if kpi != '참여율' else '%'}",
                delta="목표값"
            )
    
    # 주간 실행 계획
    st.markdown("### 📅 12주 실행 로드맵")
    
    # 단계별 탭
    tab1, tab2, tab3 = st.tabs(["🏗️ 파운데이션 (1-2주)", "🚀 실행 (3-8주)", "📈 성장 (9-12주)"])
    
    with tab1:
        foundation_weeks = [plan for plan in strategy.weekly_plans if plan["week"] <= 2]
        for week_plan in foundation_weeks:
            with st.expander(f"Week {week_plan['week']}: {week_plan['phase']}"):
                for task in week_plan['tasks']:
                    st.markdown(f"- [ ] {task}")
                st.markdown(f"**🎯 주요 KPI**: {week_plan['kpi_focus']}")
    
    with tab2:
        execution_weeks = [plan for plan in strategy.weekly_plans if 3 <= plan["week"] <= 8]
        for week_plan in execution_weeks:
            with st.expander(f"Week {week_plan['week']}: {week_plan['phase']}"):
                for task in week_plan['tasks']:
                    st.markdown(f"- [ ] {task}")
                st.markdown(f"**🎯 주요 KPI**: {week_plan['kpi_focus']}")
    
    with tab3:
        growth_weeks = [plan for plan in strategy.weekly_plans if plan["week"] >= 9]
        for week_plan in growth_weeks:
            with st.expander(f"Week {week_plan['week']}: {week_plan['phase']}"):
                for task in week_plan['tasks']:
                    st.markdown(f"- [ ] {task}")
                st.markdown(f"**🎯 주요 KPI**: {week_plan['kpi_focus']}")
    
    # 권장 도구 및 리소스
    st.markdown("### 🛠️ 권장 도구 및 리소스")
    
    tool_cols = st.columns(3)
    for i, tool in enumerate(strategy.recommended_tools):
        with tool_cols[i % 3]:
            st.info(f"📱 {tool}")
    
    # 개인화된 브랜드 가이드 다운로드
    st.markdown("### 📄 브랜드 가이드 문서")
    
    brand_guide = generate_brand_guide(profile, strategy)
    
    st.download_button(
        label="📥 맞춤형 브랜드 가이드 다운로드",
        data=brand_guide,
        file_name=f"instagram_brand_guide_{profile.id[:8]}.txt",
        mime="text/plain"
    )

def generate_brand_guide(profile: UserProfile, strategy: BrandStrategy) -> str:
    """브랜드 가이드 문서 생성"""
    guide = f"""
📸 INSTAGRAM 브랜딩 가이드
생성일: {datetime.now().strftime('%Y-%m-%d')}
브랜드 ID: {profile.id[:8]}

{'='*50}
🎯 브랜드 전략 개요
{'='*50}

브랜드 타입: {strategy.brand_type}
전략명: {strategy.strategy_name}
비즈니스 단계: {SURVEY_DATA['business_stages'][profile.business_stage]}
사업 분야: {SURVEY_DATA['business_types'][profile.business_type]}

{'='*50}
👥 타겟 오디언스
{'='*50}

연령대: {SURVEY_DATA['age_groups'][profile.target_age_group]}
성별 분포: {profile.target_gender}
주요 목표: {', '.join([SURVEY_DATA['primary_goals'][goal] for goal in profile.primary_goals])}

{'='*50}
🎨 브랜드 아이덴티티
{'='*50}

브랜드 아키타입: {SURVEY_DATA['brand_archetypes'][profile.brand_archetype]}

브랜드 톤앤보이스:
- 공식적(1) ←→ 캐주얼(10): {profile.tone_scores['formal_casual']}/10
- 진지함(1) ←→ 재미있음(10): {profile.tone_scores['serious_fun']}/10  
- 정중함(1) ←→ 과감함(10): {profile.tone_scores['polite_bold']}/10
- 사실적(1) ←→ 열정적(10): {profile.tone_scores['factual_passionate']}/10

{'='*50}
📋 콘텐츠 전략
{'='*50}

콘텐츠 필러:
{chr(10).join([f"{i+1}. {pillar}" for i, pillar in enumerate(strategy.content_pillars)])}

콘텐츠 믹스 비율:
{chr(10).join([f"- {format}: {ratio}%" for format, ratio in strategy.content_mix.items()])}

월간 게시 빈도:
{chr(10).join([f"- {format}: {freq}개" for format, freq in strategy.posting_frequency.items()])}

{'='*50}
🎯 성과 목표 (KPI)
{'='*50}

{chr(10).join([f"- {kpi.replace('_', ' ').title()}: {target}%" for kpi, target in strategy.kpi_targets.items()])}

{'='*50}
🛠️ 권장 도구
{'='*50}

{chr(10).join([f"- {tool}" for tool in strategy.recommended_tools])}

{'='*50}
💼 리소스 현황
{'='*50}

가용 시간: {profile.time_available}/주
예산: {profile.budget}/월
보유 도구: {', '.join(profile.tools_available) if profile.tools_available else '없음'}

{'='*50}
🏆 경쟁사 분석
{'='*50}

주요 경쟁사: {', '.join(profile.competitors) if profile.competitors else '미지정'}
차별화 포인트: {', '.join(profile.differentiation) if profile.differentiation else '미지정'}

{'='*50}
📅 주간 실행 계획 (처음 4주)
{'='*50}

{chr(10).join([f"""
Week {plan['week']}: {plan['phase']}
목표: {plan['kpi_focus']}
할 일:
{chr(10).join([f"  - {task}" for task in plan['tasks']])}
""" for plan in strategy.weekly_plans[:4]])}

{'='*50}
💡 성공을 위한 핵심 팁
{'='*50}

1. 일관성 유지: 시각적 스타일과 브랜드 보이스를 모든 콘텐츠에서 일관되게 유지하세요.

2. 참여 우선: 좋아요보다는 댓글, 저장, 공유를 유도하는 콘텐츠에 집중하세요.

3. 스토리 활용: 일상적이고 진정성 있는 모습을 스토리로 꾸준히 공유하세요.

4. 데이터 기반 의사결정: 주간 인사이트를 반드시 확인하고 전략을 조정하세요.

5. 커뮤니티 중심: 팔로워와의 진정한 소통과 관계 구축에 집중하세요.

{'='*50}
📞 지원 및 문의
{'='*50}

이 가이드는 Instagram Branding Expert 시스템에서 생성되었습니다.
추가 문의사항이나 전략 조정이 필요한 경우 언제든 새로운 분석을 실행하세요.

생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return guide

def show_dashboard():
    st.markdown('<div class="section-header"><h2>📈 성과 대시보드</h2></div>', unsafe_allow_html=True)
    
    if not st.session_state.survey_completed:
        st.warning("먼저 브랜딩 설문조사를 완료해주세요.")
        return
    
    # 가상 성과 데이터 (실제 구현시 Instagram API 연동)
    st.markdown("### 📊 실시간 성과 모니터링")
    
    # KPI 메트릭
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="팔로워 수", 
            value="1,234", 
            delta="156 (+14.5%)",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="참여율", 
            value="2.3%", 
            delta="0.5% (+27.8%)",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="도달률", 
            value="15,678", 
            delta="2,345 (+17.6%)",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="웹사이트 클릭", 
            value="89", 
            delta="23 (+34.8%)",
            delta_color="normal"
        )
    
    # 성과 차트
    col1, col2 = st.columns(2)
    
    with col1:
        # 팔로워 성장 추이
        dates = pd.date_range(start='2024-01-01', end='2024-07-24', freq='W')
        followers = [1000 + i*15 + (i%4)*10 for i in range(len(dates))]
        
        fig = px.line(
            x=dates, 
            y=followers,
            title="팔로워 성장 추이",
            labels={'x': '날짜', 'y': '팔로워 수'}
        )
        fig.update_traces(line_color='#833AB4')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 콘텐츠 성과 분석
        content_types = ['릴스', '캐러셀', '스토리', '싱글포스트']
        engagement_rates = [2.5, 2.8, 1.2, 1.8]
        
        fig = px.bar(
            x=content_types,
            y=engagement_rates,
            title="콘텐츠 타입별 참여율",
            labels={'x': '콘텐츠 타입', 'y': '참여율 (%)'},
            color=engagement_rates,
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 주간 리포트
    st.markdown("### 📋 주간 성과 리포트")
    
    with st.expander("Week 30 (2024.07.15 - 2024.07.21) 성과 분석"):
        st.markdown("""
        #### 🎯 목표 달성 현황
        - ✅ **팔로워 증가**: 156명 (목표: 100명) - 156% 달성
        - ✅ **참여율**: 2.3% (목표: 2.0%) - 115% 달성  
        - ❌ **웹사이트 트래픽**: 89클릭 (목표: 120클릭) - 74% 달성
        
        #### 🏆 최고 성과 콘텐츠
        1. **릴스**: "5분 만에 브랜딩 팁" - 참여율 4.2%
        2. **캐러셀**: "브랜드 스토리 템플릿" - 참여율 3.8%
        3. **스토리**: "Q&A 세션" - 완료율 68%
        
        #### 🔧 다음 주 최적화 권장사항
        - 웹사이트 트래픽 증대를 위해 CTA 문구 강화
        - 릴스 콘텐츠 비중 확대 (현재 40% → 50%)
        - 스토리 링크 스티커 활용 빈도 증가
        """)
    
    # 개선 권장사항
    st.markdown("### 💡 AI 기반 개선 권장사항")
    
    recommendations = [
        {
            "우선순위": "높음",
            "영역": "콘텐츠 최적화", 
            "권장사항": "릴스 콘텐츠 비중을 50%로 확대하여 도달률 20% 향상 예상",
            "예상효과": "+20% 도달률"
        },
        {
            "우선순위": "중간",
            "영역": "참여 증대",
            "권장사항": "캐러셀 포스트에 인터랙티브 요소 추가 (폴, 퀴즈 등)",
            "예상효과": "+15% 참여율"
        },
        {
            "우선순위": "중간", 
            "영역": "트래픽 전환",
            "권장사항": "스토리 하이라이트에 링크 추가 및 바이오 링크 최적화",
            "예상효과": "+25% 웹사이트 클릭"
        }
    ]
    
    for rec in recommendations:
        priority_color = {"높음": "🔴", "중간": "🟡", "낮음": "🟢"}[rec["우선순위"]]
        st.markdown(f"""
        {priority_color} **{rec['영역']}** ({rec['우선순위']} 우선순위)
        - {rec['권장사항']}
        - 예상 효과: {rec['예상효과']}
        """)

def show_resources():
    st.markdown('<div class="section-header"><h2>📚 브랜딩 리소스 센터</h2></div>', unsafe_allow_html=True)
    
    # 탭으로 리소스 구분
    tab1, tab2, tab3, tab4 = st.tabs(["🛠️ 도구", "📖 가이드", "🎨 템플릿", "📊 벤치마크"])
    
    with tab1:
        st.markdown("### 🛠️ 추천 도구 및 앱")
        
        tools_categories = {
            "콘텐츠 제작": [
                {"이름": "Canva Pro", "용도": "디자인 및 템플릿", "가격": "월 12,000원", "추천도": "⭐⭐⭐⭐⭐"},
                {"이름": "VSCO", "용도": "사진 편집 및 필터", "가격": "월 19,900원", "추천도": "⭐⭐⭐⭐"},
                {"이름": "InShot", "용도": "비디오 편집", "가격": "무료/유료", "추천도": "⭐⭐⭐⭐"},
            ],
            "스케줄링": [
                {"이름": "Later", "용도": "포스트 예약 및 스케줄링", "가격": "월 $18", "추천도": "⭐⭐⭐⭐⭐"},
                {"이름": "Buffer", "용도": "소셜미디어 관리", "가격": "월 $6", "추천도": "⭐⭐⭐⭐"},
                {"이름": "Hootsuite", "용도": "다중 플랫폼 관리", "가격": "월 $49", "추천도": "⭐⭐⭐"},
            ],
            "분석": [
                {"이름": "Instagram Insights", "용도": "기본 성과 분석", "가격": "무료", "추천도": "⭐⭐⭐⭐"},
                {"이름": "Sprout Social", "용도": "고급 분석", "가격": "월 $99", "추천도": "⭐⭐⭐⭐⭐"},
                {"이름": "Iconosquare", "용도": "성과 추적", "가격": "월 $29", "추천도": "⭐⭐⭐⭐"},
            ]
        }
        
        for category, tools in tools_categories.items():
            st.markdown(f"#### {category}")
            for tool in tools:
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                with col1:
                    st.markdown(f"**{tool['이름']}**")
                with col2:
                    st.markdown(tool['용도'])
                with col3:
                    st.markdown(tool['가격'])
                with col4:
                    st.markdown(tool['추천도'])
            st.markdown("---")
    
    with tab2:
        st.markdown("### 📖 브랜딩 가이드")
        
        guides = [
            {
                "제목": "인스타그램 알고리즘 완전 정복 가이드",
                "설명": "2024-2025년 최신 알고리즘 변화와 대응 전략",
                "난이도": "초급-중급",
                "소요시간": "15분"
            },
            {
                "제목": "브랜드 아이덴티티 설정 워크북", 
                "설명": "체계적인 브랜드 정체성 구축 단계별 가이드",
                "난이도": "초급",
                "소요시간": "30분"
            },
            {
                "제목": "콘텐츠 기획 및 제작 마스터클래스",
                "설명": "매력적인 콘텐츠 아이디어 발굴과 제작 노하우",
                "난이도": "중급",
                "소요시간": "45분"
            },
            {
                "제목": "인플루언서 협업 전략 가이드",
                "설명": "효과적인 파트너십 구축과 ROI 측정 방법",
                "난이도": "고급", 
                "소요시간": "25분"
            }
        ]
        
        for guide in guides:
            with st.expander(f"📖 {guide['제목']}"):
                st.markdown(f"**설명**: {guide['설명']}")
                st.markdown(f"**난이도**: {guide['난이도']} | **소요시간**: {guide['소요시간']}")
                st.button(f"가이드 읽기", key=f"guide_{guide['제목']}")
    
    with tab3:
        st.markdown("### 🎨 디자인 템플릿")
        
        template_categories = {
            "포스트 템플릿": [
                "브랜드 소개 캐러셀",
                "제품 소개 템플릿", 
                "고객 후기 디자인",
                "교육 콘텐츠 레이아웃",
                "이벤트 홍보 템플릿"
            ],
            "스토리 템플릿": [
                "Q&A 스토리 템플릿",
                "비하인드 스토리 프레임",
                "제품 사용법 가이드",
                "투표 및 퀴즈 템플릿",
                "링크 스티커 디자인"
            ],
            "하이라이트 커버": [
                "미니멀 스타일",
                "브랜드 컬러 세트", 
                "아이콘 기반 디자인",
                "타이포그래피 중심",
                "일러스트 스타일"
            ]
        }
        
        for category, templates in template_categories.items():
            st.markdown(f"#### {category}")
            cols = st.columns(3)
            for i, template in enumerate(templates):
                with cols[i % 3]:
                    st.markdown(f"🎨 {template}")
                    st.button("다운로드", key=f"template_{category}_{i}")
    
    with tab4:
        st.markdown("### 📊 업계 벤치마크 데이터")
        
        # 업계별 벤치마크 차트
        benchmark_data = {
            "업계": ["패션", "뷰티", "음식", "기술", "여행", "피트니스"],
            "평균_팔로워": [15000, 25000, 8000, 12000, 18000, 22000],
            "평균_참여율": [1.8, 2.1, 2.5, 1.2, 2.0, 2.8],
            "월간_게시물": [20, 25, 15, 12, 18, 24]
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                x=benchmark_data["업계"],
                y=benchmark_data["평균_참여율"],
                title="업계별 평균 참여율",
                labels={'x': '업계', 'y': '참여율 (%)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(
                x=benchmark_data["평균_팔로워"],
                y=benchmark_data["평균_참여율"],
                text=benchmark_data["업계"],
                title="팔로워 수 vs 참여율",
                labels={'x': '평균 팔로워 수', 'y': '참여율 (%)'}
            )
            fig.update_traces(textposition="top center")
            st.plotly_chart(fig, use_container_width=True)
        
        # 성과 기준표
        st.markdown("#### 📈 성과 평가 기준표")
        
        performance_standards = pd.DataFrame({
            "지표": ["참여율", "팔로워 증가율", "도달률", "스토리 완료율"],
            "우수 (상위 10%)": ["3.0% 이상", "20% 이상", "30% 이상", "70% 이상"],
            "양호 (상위 25%)": ["2.0-3.0%", "15-20%", "20-30%", "60-70%"],
            "평균 (상위 50%)": ["1.0-2.0%", "10-15%", "10-20%", "50-60%"],
            "개선 필요": ["1.0% 미만", "10% 미만", "10% 미만", "50% 미만"]
        })
        
        st.dataframe(performance_standards, use_container_width=True)

if __name__ == "__main__":
    main()
