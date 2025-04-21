import streamlit as st
import openai
import pandas as pd
import datetime

# OpenAI API Key (Streamlit Secrets 사용)
openai.api_key = st.secrets["openai"]["api_key"]

st.set_page_config(page_title="감정 중심 자기개방 실험", layout="centered")

st.title("🎤 감정 중심 자기개방 실험 (텍스트 인터페이스)")
st.markdown("아래 질문 중 3개를 자유롭게 선택해 GPT에게 이야기해 주세요.")

questions = [
    "1. 요즘 당신이 자주 하는 고민은 무엇인가요?",
    "2. 최근 가장 힘들었던 일이 있다면 무엇인가요?",
    "3. 누군가에게 털어놓지 못했던 이야기가 있다면 어떤 이야기인가요?",
    "4. 어떤 상황에서 외로움을 느끼나요?",
    "5. 당신에게 중요한 인간관계나 감정 경험은 어떤 것이 있나요?",
    "6. 지금 누군가에게 진심으로 전하고 싶은 말이 있다면 무엇인가요?"
]

selected_questions = st.multiselect("📝 질문 선택 (3개)", questions, max_selections=3)

if len(selected_questions) == 3:
    st.success("좋아요! 선택한 질문을 GPT에게 자유롭게 이야기해보세요.")
    dialogue = ""
    for q in selected_questions:
        st.subheader(f"🗨️ {q}")
        user_input = st.text_area(f"이 질문에 대한 당신의 이야기:", key=q)
        if user_input:
            with st.spinner("GPT가 응답 중..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "너는 공감적이고 따뜻한 상담자야."},
                        {"role": "user", "content": user_input}
                    ]
                )
                answer = response["choices"][0]["message"]["content"]
                st.write("🤖 GPT의 응답:")
                st.info(answer)

                dialogue += f"\n\n[질문] {q}\n[내 이야기] {user_input}\n[GPT 응답] {answer}\n"

    if st.button("💾 대화 내용 저장"):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dialogue_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(dialogue)
        st.success(f"대화가 `{filename}`로 저장되었습니다.")

else:
    st.warning("질문을 정확히 3개 선택해주세요.")
