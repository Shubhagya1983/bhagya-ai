import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import os
from PIL import Image

# Gemini API Key 
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# භාග්‍ය AI හි අනන්‍යතාවය සහ කාර්මික දැනුම
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="ඔබේ නම 'භාග්‍ය' (Bhagya). ඔබව නිර්මාණය කළේ 'ශුභාග්‍ය' (Shubhagya) විසින්. ඔබ LB Engineering ආයතනයේ කාර්මික ස්වයංක්‍රීයකරණය පිළිබඳ AI සහායකයෙකි. ඔබට Siemens, Mitsubishi, Xinje PLC සහ Zoncn, HBD, Delta, Siemens, Hyundai, Parker VFD සහ servo මෝටර් පිළිබඳ විශේෂඥ දැනුමක් ඇත. VFD Error Code එකක හෝ යන්ත්‍රයක පින්තූරයක් දුන් විට, එහි දෝෂ කේතය කුමක්දැයි පරීක්ෂා කර, ඊට හේතුව සහ විසඳුම සිංහලෙන් පැහැදිලිව ලබා දෙන්න."
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

st.write("ආයුබෝවන් ශුභාග්‍ය! මම භාග්‍ය. VFD දෝෂ කේත හෝ කාර්මික ගැටලු සඳහා ඡායාරූපයක් ලබා දී උදව් ලබා ගන්න.")

# ටැබ් ක්‍රමයට පෙළ හෝ කැමරාව තෝරාගැනීමට සැලැස්වීම
tab1, tab2 = st.tabs(["💬 පණිවිඩයක් ලිවීම", "📷 ඡායාරූපයක් ලබා දීම (Error Photo)"])

with tab1:
    with st.form(key='chat_form'):
        user_input = st.text_input("ඔබේ ගැටලුව මෙතන ලියන්න:")
        submit_button = st.form_submit_button(label="යවන්න")

    if submit_button and user_input:
        with st.spinner('භාග්‍ය පිළිතුරු සකසමින්...'):
            try:
                response = model.generate_content(user_input)
                st.success(response.text)
                
                try:
                    tts = gTTS(text=response.text, lang='si')
                    audio_fp = io.BytesIO()
                    tts.write_to_fp(audio_fp)
                    st.audio(audio_fp, format='audio/mp3', autoplay=True)
                except Exception as e:
                    pass
            except Exception as e:
                st.error(f"දෝෂයක් මතු විය: {e}")

with tab2:
    st.write("VFD එකේ Error Code එක හෝ පුවරුවේ පින්තූරයක් මෙතැනින් ලබා දෙන්න:")
    camera_photo = st.camera_input("කැමරාව ක්‍රියාත්මක කරන්න")
    
    uploaded_photo = st.file_uploader("অথবা ෆයිල් එකකින් Upload කරන්න", type=["jpg", "jpeg", "png"])
    
    image_to_analyze = camera_photo if camera_photo else uploaded_photo
    
    if image_to_analyze is not None:
        img = Image.open(image_to_analyze)
        st.image(img, caption="ලබා දුන් ඡායාරූපය", width=300)
        
        if st.button("මෙම Error එක පරීක්ෂා කරන්න"):
            with st.spinner('භාග්‍ය ඡායාරූපය විශ්ලේෂණය කරමින්...'):
                try:
                    # Gemini වෙත පින්තූරය සහ ප්‍රශ්නය යැවීම
                    prompt = "මෙම VFD Error Code එක හෝ යන්ත්‍රයේ දෝෂය පරීක්ෂා කර, මෙහි ඇති දෝෂයට හේතුව (Reason) සහ ඊට දිය යුතු විසඳුම (Solution) සිංහලෙන් පැහැදිලි කරන්න."
                    response = model.generate_content([prompt, img])
                    
                    st.success(response.text)
                    
                    try:
                        tts = gTTS(text=response.text, lang='si')
                        audio_fp = io.BytesIO()
                        tts.write_to_fp(audio_fp)
                        st.audio(audio_fp, format='audio/mp3', autoplay=True)
                    except Exception as e:
                        pass
                except Exception as e:
                    st.error(f"දෝෂයක් මතු විය: {e}")