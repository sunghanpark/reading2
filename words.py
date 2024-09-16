import streamlit as st
import time
from gtts import gTTS
import os
import base64

def get_audio_player(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("temp.mp3")
    with open("temp.mp3", "rb") as f:
        audio_bytes = f.read()
    os.remove("temp.mp3")
    audio_base64 = base64.b64encode(audio_bytes).decode()
    return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'

def reveal_sentence(sentence, placeholder, speed):
    words = sentence.split()
    for i in range(len(words)):
        placeholder.text_area("문장 표시", " ".join(words[:i+1]), height=100)
        time.sleep(1 / speed)  # 속도에 따른 지연 시간 조절
    
def show_bracket_mode(sentence):
    words = sentence.split()
    if words:
        return f"({words[0]}) {' '.join(words[1:])}"
    return ""

def main():
    st.set_page_config(page_title="문장 점진적 공개 앱", page_icon="📚")
    st.title("문장 점진적 공개 앱")
    
    languages = {
        "English": "en",
        "한국어": "ko",
        "日本語": "ja",
        "中文": "zh-cn",
        "Español": "es",
        "Français": "fr",
        "Deutsch": "de"
    }
    
    selected_language = st.selectbox("언어 선택", list(languages.keys()))
    
    sentence = st.text_input("문장 입력", placeholder="여기에 문장을 입력하세요")
    
    mode = st.radio("모드 선택", ["점진적 공개 모드", "괄호 모드"])
    
    speed = st.slider("표시 속도", min_value=1, max_value=10, value=5)
    
    if st.button("실행"):
        if mode == "점진적 공개 모드":
            placeholder = st.empty()
            reveal_sentence(sentence, placeholder, speed)
        else:
            bracketed = show_bracket_mode(sentence)
            st.text_area("괄호 모드 결과", bracketed, height=100)
            if st.button("전체 문장 보기"):
                st.text_area("전체 문장", sentence, height=100)
        
        # TTS 실행
        st.markdown(get_audio_player(sentence, languages[selected_language]), unsafe_allow_html=True)

    st.sidebar.header("앱 정보")
    st.sidebar.info("이 앱은 문장을 점진적으로 공개하거나 괄호 모드로 표시합니다.")
    st.sidebar.info(f"선택된 언어: {selected_language}")
    st.sidebar.info(f"현재 표시 속도: {speed}")

if __name__ == "__main__":
    main()
