import streamlit as st
import pandas as pd
import datetime
from openai import OpenAI

# OpenAI 클라이언트 설정
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.set_page_config(page_title="감정 중심 자기개방 실험", layout="centered")

st.title("🎤 감정 중심 자기개방 실험 (텍스트 인터페이스)")
st.markdown("아래 질문 중 3개를 선택하여 자유롭게 GPT와 이야기해 주세요.")

questions = [
    "1. 요즘 당신이 자주 하는 고민은 무엇인가요?",
    "2. 최근 가장 힘들었던 일이 있다면 무엇인가요?",
    "3. 누군가에게 털어놓지 못했던 이야기가 있다면 어떤 이야기인가요?",
    "4. 어떤 상황에서 외로움을 느끼나요?",
    "5. 당신에게 중요한 인간관계나 감정 경험은 어떤 것이 있나요?",
    "6. 지금 누군가에게 진심으로 전하고 싶은 말이 있다면 무엇인가요?"
]

selected_questions = st.multiselect("📝 질문 선택 (정확히 3개)", questions, max_selections=3)

if len(selected_questions) == 3:
    st.success("좋아요! 선택한 질문에 대해 GPT와 대화해보세요.")
    dialogue_data = []

    for q in selected_questions:
        st.subheader(f"🗨️ {q}")
        user_input = st.text_area(f"당신의 이야기:", key=q)
        if user_input:
            with st.spinner("GPT가 응답 중..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "너는 따뜻하고 공감적인 상담자야."},
                            {"role": "user", "content": user_input}
                        ]
                    )
                    answer = response.choices[0].message.content
                    st.write("🤖 GPT의 응답:")
                    st.info(answer)

                    dialogue_data.append({
                        "질문": q,
                        "사용자 응답": user_input,
                        "GPT 응답": answer,
                        "대화시각": datetime.datetime.now().isoformat()
                    })
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

    if dialogue_data and st.button("💾 대화 내용 저장 및 설문지로 이동"):
        df = pd.DataFrame(dialogue_data)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"dialogue_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)
        st.success(f"대화가 저장되었습니다! 파일명: `{csv_filename}`")

        st.markdown("👉 아래 버튼을 눌러 사후 설문을 작성해주세요.")
        st.markdown("[📋 설문지 작성하러 가기](https://forms.gle/aG7AhGAjLyMSGUvS8)", unsafe_allow_html=True)

else:
    st.warning("질문을 정확히 3개 선택해주세요.")
