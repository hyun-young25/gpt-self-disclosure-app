import streamlit as st
import pandas as pd
import datetime
from gtts import gTTS
from openai import OpenAI
import uuid
import os
import speech_recognition as sr

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.set_page_config(page_title="감정 중심 자기개방 실험", layout="centered")
st.title("🎤 감정 중심 자기개방 실험")
st.markdown("먼저 인터페이스 유형을 선택한 후, 3개의 질문을 선택하고 GPT와 상호작용해주세요.")

# 1. 인터페이스 선택
interface = st.radio("GPT와의 대화 방식 선택", ("📝 텍스트 인터페이스", "🎙️ 음성 인터페이스"))

# 2. 공통 질문
questions = [
    "1. 요즘 당신이 자주 하는 고민은 무엇인가요?",
    "2. 최근 가장 힘들었던 일이 있다면 무엇인가요?",
    "3. 누군가에게 털어놓지 못했던 이야기가 있다면 어떤 이야기인가요?",
    "4. 어떤 상황에서 외로움을 느끼나요?",
    "5. 당신에게 중요한 인간관계나 감정 경험은 어떤 것이 있나요?",
    "6. 지금 누군가에게 진심으로 전하고 싶은 말이 있다면 무엇인가요?"
]
selected_questions = st.multiselect("🧠 아래 질문 중 3개를 선택해주세요", questions, max_selections=3)

# 데이터 저장용
dialogue_data = []

# GPT 응답 함수
def ask_gpt(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 따뜻하고 공감적인 상담자야."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

# 음성 인식 함수
def record_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ 말해주세요...")
        audio = recognizer.listen(source, phrase_time_limit=10)
        try:
            return recognizer.recognize_google(audio, language="ko-KR")
        except:
            st.warning("음성을 인식하지 못했습니다.")
            return None

# TTS 함수
def speak(text):
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang="ko")
    tts.save(filename)
    return filename

# 3. 질문 응답
if len(selected_questions) == 3:
    st.success("선택이 완료되었습니다. 질문에 답변해주세요.")
    for q in selected_questions:
        st.subheader(f"🗨️ {q}")
        if interface == "📝 텍스트 인터페이스":
            user_input = st.text_area("✏️ 답변을 입력하세요:", key=q)
        else:
            if st.button(f"🎙️ '{q}'에 답변 말하기", key=f"btn_{q}"):
                user_input = record_voice()
                if user_input:
                    st.write(f"🧑 내 음성 인식 결과: **{user_input}**")
                else:
                    user_input = None
        if user_input:
            with st.spinner("GPT가 응답 중입니다..."):
                answer = ask_gpt(user_input)
            st.write("🤖 GPT 응답:")
            st.info(answer)
            if interface == "🎙️ 음성 인터페이스":
                audio_file = speak(answer)
                st.audio(audio_file, format="audio/mp3")
            dialogue_data.append({
                "질문": q,
                "사용자 응답": user_input,
                "GPT 응답": answer,
                "방식": interface,
                "시간": datetime.datetime.now().isoformat()
            })

# 4. 저장 및 설문 이동
if dialogue_data and st.button("💾 대화 저장 및 설문지로 이동"):
    df = pd.DataFrame(dialogue_data)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dialogue_{timestamp}.csv"
    df.to_csv(filename, index=False)
    st.success(f"대화가 저장되었습니다! 파일명: `{filename}`")
    st.markdown("👉 [📋 설문지 작성하러 가기](https://forms.gle/aG7AhGAjLyMSGUvS8)", unsafe_allow_html=True)
else:
    st.warning("모든 질문에 답변 후 저장 버튼을 눌러주세요.")
