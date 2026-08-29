import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import os

# Gemini API Key 
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# භාග්‍ය AI හි අනන්‍යතාවය සහ කාර්මික දැනුම
model = genai.GenerativeModel(
    model_name="gemini-3.6-flash",
    system_instruction="ඔබේ නම 'භාග්‍ය' (Bhagya). ඔබව නිර්මාණය කළේ 'ශුභාග්‍ය' (Shubhagya) විසින්. ඔබ LB Engineering ආයතනයේ කාර්මික ස්වයංක්‍රීයකරණය පිළිබඳ AI සහායකයෙකි. ඔබට Siemens S7-1200, Mitsubishi FX3U, Xinje XD3 PLC ගැන සහ Zoncn, HBD, Delta, Siemens VFD ගැන විශේෂඥ දැනුමක් ඇත. කරුණාකර සිංහලෙන් සහ ඉංග්‍රීසියෙන් මිත්‍රශීලීව පිළිතුරු දෙන්න. කටහඬින් ඇසීමට පහසු වන පරිදි පිළිතුරු කෙටි සහ පැහැදිලිව ලබා දෙන්න."
)

st.set_page_config(page_title="Bhagya AI", page_icon="🤖")

# ඡායාරූපය සහ මාතෘකාව පෙන්වීම
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("profile.jpg"):
        st.image("profile.jpg", width=120)
    else:
        st.write("🧑‍💻")
with col2:
    st.title("🤖 භාග්‍ය (Bhagya AI)")

st.write("ආයුබෝවන් ශුභාග්‍ය! මම භාග්‍ය. ඔබට අවශ්‍ය තාක්ෂණික සහාය ලබාදීමට මම සූදානම්.")

# ගැටලුව ලබා ගැනීම
with st.form(key='chat_form'):
    user_input = st.text_input("ඔබේ ගැටලුව මෙතන ලියන්න (කටහඬින් ටයිප් කිරීමට Phone එකේ Mic එක භාවිතා කරන්න):")
    submit_button = st.form_submit_button(label="යවන්න")

if submit_button:
    if user_input:
        with st.spinner('භාග්‍ය පිළිතුරු සකසමින්...'):
            try:
                response = model.generate_content(user_input)
                st.success(response.text)
                
                # සිංහලෙන් කතා කිරීම
                try:
                    tts = gTTS(text=response.text, lang='si')
                    audio_fp = io.BytesIO()
                    tts.write_to_fp(audio_fp)
                    st.audio(audio_fp, format='audio/mp3', autoplay=True)
                except Exception as e:
                    st.warning("හඬ නිකුත් කිරීමේ ගැටලුවකි.")
                    
            except Exception as e:
                st.error(f"දෝෂයක් මතු විය: {e}")
    else:
        st.warning("කරුණාකර ගැටලුවක් ඇතුළත් කරන්න.")