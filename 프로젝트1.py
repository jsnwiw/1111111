import time  # 추가된 코드: Import -> import (소문자 수정)
import matplotlib.pyplot as plt  # np에서 plt로 수정
import numpy as np
import pandas as pd
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="학생만족도 대시보드", layout="wide")


# --- CSS: 글래스모피즘 및 애니메이션 효과 ---
st.markdown(
    """
    <style>
    /* 전체 배경 설정 */
    .stApp {
        background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
        background-attachment: fixed;
    }

    /* 애니메이션 정의 */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* 사이드바 글래스 스타일 */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* 메인 카드 스타일 (글래스모피즘) */
    .stMetric, .stDataFrame, .stAlert, div.stButton > button {
        animation: fadeInUp 0.8s ease-out;
    }

    /* 버튼 스타일 커스텀 */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.3);
        color: #1c1c1c;
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        font-weight: bold;
        width: 100%;
    }

    div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.5);
        transform: scale(1.02);
        border: 1px solid #ffffff;
    }

    /* 입력창 및 슬라이더 스타일 */
    .stTextInput input, .stSlider {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }
    
    /* 타이틀 애니메이션 및 폰트 */
    h1 {
        color: #2c3e50;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: fadeInUp 0.5s ease-out;
    }
    
    /* 결과 박스 글래스 효과 */
    .element-container div.stAlert {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)  # 추가된 코드: CSS 오타(h1 {~) 수정 및 파이썬 문법 정리


# 메인 타이틀
st.title("✨ 학생만족도 대시보드")
st.markdown("##### 학생만족도 실시중입니다. 아래의 데이터를 확인해 주세요.")


# 세션 상태 초기화
if "responses" not in st.session_state:
    st.session_state.responses = []


# 사이드바 입력창
st.sidebar.header("📝 입력 섹션")
student_name = st.sidebar.text_input(
    "학생 이름 입력", value="", placeholder="이름을 입력하세요"
)
st.sidebar.markdown("---")
st.sidebar.header("📊 만족도")
score = st.sidebar.slider(
    "만족도 점수", min_value=0, max_value=100, value=50, step=1
)
student_제출 = st.sidebar.button("🚀 데이터 제출하기")
view_button = st.sidebar.button("📂 저장된 답변 보기")


col1, col2 = st.columns([1, 1])


if student_제출:
    with st.spinner("데이터를 안전하게 처리 중입니다..."):
        progress_bar = st.progress(0)
        for progress in range(1, 101):
            time.sleep(0.01)  # 조금 더 빠르게 조절
            progress_bar.progress(progress)

    # 데이터 보정 및 저장
    raw_scores = [score]
    clipped_scores = np.clip(raw_scores, 0, 100)
    final_score = int(clipped_scores[0])
    name_to_save = student_name.strip() or "익명 학생"

    st.session_state.responses.append({
        "학생 이름": name_to_save,
        "만족도 점수": final_score,
        "시간": time.strftime("%H:%M:%S"),
    })

    with col1:
        st.markdown("### 처리 결과")
        if final_score >= 80:
            st.success(f"🌟 **아주 만족!** ({final_score}점)")
        elif final_score >= 50:
            st.info(f"😊 **보통 이상!** ({final_score}점)")
        else:
            st.warning(f"⚠️ **개선이 필요해요..** ({final_score}점)")
        # st.balloons() # 축하 애니메이션 추가


# 저장된 답변 보기 버튼 로직
if view_button:
    with col2:
        st.subheader("📋 저장된 답변 목록")
        if st.session_state.responses:
            df_responses = pd.DataFrame(st.session_state.responses)
            # 데이터프레임 스타일링
            st.dataframe(
                df_responses.style.highlight_max(
                    axis=0, subset=["만족도 점수"], color="#d4edda"
                ),
                use_container_width=True,
            )
        else:
            st.info(
                "아직 저장된 응답이 없습니다. 첫 번째 응답을 보내주세요!"
            )