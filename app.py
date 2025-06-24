
import streamlit as st
import pandas as pd
from openai import OpenAI

# OpenAI Client (새 방식)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# CSV 파일 
workout_df = pd.read_csv("workout.csv")

st.title("🏋️ GPT 기반 맞춤 운동 피드백 코치")

# 부위 다중 선택
selected_parts = st.multiselect("운동 부위를 선택하세요", workout_df['부위'].unique())

# 선택된 부위에 따라 운동 필터링
if selected_parts:
    filtered_df = workout_df[workout_df['부위'].isin(selected_parts)]
else:
    filtered_df = workout_df

# 운동 선택
selected_exercises = st.multiselect(
    "오늘 수행한 운동을 선택하세요:",
    options=filtered_df['운동'].unique(),
    default=None
)

# 오늘 루틴 정리
if selected_exercises:
    today_df = filtered_df[filtered_df['운동'].isin(selected_exercises)]
    st.subheader("📋 오늘의 루틴 요약")
    st.dataframe(today_df[['운동', '자극 정확도', '자세']])

    # GPT 입력 생성
    routine_summary = "\n".join(
        [f"- {row['운동']}: {row['자세'] or '자세 정보 없음'}" for _, row in today_df.iterrows()]
    )

    # GPT 응답 받기
    if st.button("🧠 GPT 피드백 받기"):
        with st.spinner("GPT가 루틴을 분석 중입니다..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "너는 전문가 트레이너야. 사용자의 운동 루틴을 보고 피드백을 주고, 필요한 개선점이나 추가 운동을 제안해."},
                    {"role": "user", "content": f"오늘의 운동 루틴:\n{routine_summary}\n피드백을 주세요."}
                ]
            )
            st.success("✅ 피드백 완료!")
            st.markdown(response.choices[0].message.content)
else:
    st.info("오늘 수행한 운동을 선택하면 GPT 피드백을 받을 수 있어요.")
