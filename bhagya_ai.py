import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import os
from PIL import Image

# 1. API Key සැකසුම
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. භාග්‍ය AI හි අනන්‍යතාවය සහ කාර්මික විශේෂඥ දැනුම
system_instruction = (
    "ඔබේ නම 'භාග්‍ය' (Bhagya). ඔබව නිර්මාණය කළේ 'ශුභාග්‍ය' (Shubhagya) විසින්. "
    "ඔබ LB Engineering ආයතනයේ කාර්මික ස්වයංක්‍රීයකරණය (Industrial Automation) පිළිබඳ විශේෂඥ AI සහායකයෙකි. "
    "ඔබට Siemens, Mitsubishi, Xinje PLCs සහ Zoncn, HBD, Delta, Siemens, Hyundai, Parker VFDs, "
    "Servo Motors සහ Drives පිළිබඳ ගැඹුරු තාක්ෂණික දැනුමක් ඇත. "
    "පරිශීලකයා පෙළ මඟින්, හඬ පණිවිඩයක් (Voice) මඟින් හෝ දුරකථන/පරිගණක ගැලරියෙන්/WhatsApp මඟින් එවන ලද VFD Error Code එකක/යන්ත්‍රයක ඡායාරූපයක් මඟින් "
    "ගැටලුවක් ඉදිරිපත් කළ විට, ඊට අදාළ දෝෂය (Fault/Error Code), හේතුව (Reason) සහ නිවැරදි විසඳුම (Solution) "
    "ඉතා පැහැදිලිව සිංහලෙන් පියවරෙන් පියවර ලබා දෙන්න."
)

model = genai.GenerativeModel(
    model_name="gemini-3.6-flash",
    system_instruction=system_instruction
)

# 3. පිටුවේ මූලික සැකසුම් (Page Config)
st.set_page_config(page_title="Bhagya AI", page_icon="🤖", layout="centered")

# 4. Profile ඡායාරූපය සහ ප්‍රධාන ශීර්ෂය
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("profile.jpg"):
        st.image("profile.jpg", width=120)
    else:
        st.write("🧑‍💻")
with col2:
    st.title("🤖 භාග්‍ය (Bhagya AI)")
    st.caption("Industrial Automation & VFD Troubleshooting Expert")

st.write("ආයුබෝවන් ශුභාග්‍ය! මම භාග්‍ය. ඔබට අවශ්‍ය තාක්ෂණික සහාය ලබා ගැනීමට පහත ඕනෑම ක්‍රමයක් භාවිත කරන්න.")

# 5. ප්‍රධාන අංශ (Tabs)
tab1, tab2, tab3, tab4 = st.tabs([
    "💬 පෙළින් (Text)", 
    "🎙️ කටහඬින් (Voice)", 
    "📷 කැමරාවෙන් (Camera)",
    "📱 ගැලරියෙන්/WhatsApp Photo"
])

# --- TAB 1: TEXT CHAT ---
with tab1:
    with st.form(key='chat_form'):
        user_input = st.text_input("ඔබේ ගැටලුව මෙතන ලියන්න (සිංහලෙන් හෝ ඉංග්‍රීසියෙන්):")
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
                except Exception:
                    pass
            except Exception as e:
                st.error(f"දෝෂයක් මතු විය: {e}")

# --- TAB 2: VOICE MIC INPUT ---
with tab2:
    st.write("🎙️ පහත ඇති **Mic අයිකනය** ඔබා සිංහලෙන් හෝ ඉංග්‍රීසියෙන් ඔබේ ගැටලුව කතා කරන්න:")
    audio_file = st.audio_input("කතා කිරීමට මෙතන ඔබන්න")
    
    if audio_file is not None:
        st.audio(audio_file)
        if st.button("මෙම හඬ පණිවිඩය යවන්න"):
            with st.spinner('භාග්‍ය ඔබේ හඬ අසා පිළිතුරු සකසමින්...'):
                try:
                    audio_bytes = audio_file.read()
                    audio_part = {
                        "mime_type": "audio/wav",
                        "data": audio_bytes
                    }
                    prompt = "මෙම හඬ පණිවිඩයේ ඇති කාර්මික ගැටලුවට හෝ ප්‍රශ්නයට සිංහලෙන් පැහැදිලි පිළිතුරක් ලබා දෙන්න."
                    response = model.generate_content([prompt, audio_part])
                    
                    st.success(response.text)
                    
                    try:
                        tts = gTTS(text=response.text, lang='si')
                        audio_fp = io.BytesIO()
                        tts.write_to_fp(audio_fp)
                        st.audio(audio_fp, format='audio/mp3', autoplay=True)
                    except Exception:
                        pass
                except Exception as e:
                    st.error(f"හඬ සැකසීමේ දෝෂයක් මතු විය: {e}")

# --- TAB 3: CAMERA INPUT ---
with tab3:
    st.write("📷 කැමරාවෙන් VFD Error එකක ඡායාරූපයක් ලබා ගන්න:")
    camera_photo = st.camera_input("කැමරාව ක්‍රියාත්මක කරන්න")
    
    if camera_photo is not None:
        img = Image.open(camera_photo)
        st.image(img, caption="කැමරාවෙන් ගත් ඡායාරූපය", width=300)
        
        if st.button("මෙම Error එක පරීක්ෂා කරන්න (Camera)"):
            with st.spinner('භාග්‍ය ඡායාරූපය විශ්ලේෂණය කරමින්...'):
                try:
                    prompt = "මෙම VFD Error Code එක හෝ යන්ත්‍රයේ ඡායාරූපය පරීක්ෂා කර, මෙහි ඇති Error Code එක, හේතුව (Reason) සහ විසඳුම (Solution) සිංහලෙන් පැහැදිලි කරන්න."
                    response = model.generate_content([prompt, img])
                    st.success(response.text)
                    
                    try:
                        tts = gTTS(text=response.text, lang='si')
                        audio_fp = io.BytesIO()
                        tts.write_to_fp(audio_fp)
                        st.audio(audio_fp, format='audio/mp3', autoplay=True)
                    except Exception:
                        pass
                except Exception as e:
                    st.error(f"දෝෂයක් මතු විය: {e}")

# --- TAB 4: GALLERY / WHATSAPP PHOTO UPLOADER ---
with tab4:
    st.write("📱 **Phone එකේ හෝ PC ගැලරියේ (WhatsApp ඇතුළුව) Save කරගත් Error පින්තූර මෙතැනට Upload කරන්න:**")
    
    gallery_upload = st.file_uploader(
        "ဓာරූපයක් තෝරා ගැනීමට මෙතන ක්ලික් කරන්න (Browse Files)", 
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=False
    )
    
    if gallery_upload is not None:
        img = Image.open(gallery_upload)
        st.image(img, caption="Uploaded Error Photo", width=350)
        
        if st.button("🔍 මෙම ඡායාරූපය Analyze කරන්න"):
            with st.spinner('භාග්‍ය ඡායාරූපය පරීක්ෂා කරමින්...'):
                try:
                    prompt = (
                        "මෙය VFD Error එකක හෝ කාර්මික දෝෂයක ඡායාරූපයකි. "
                        "මෙහි පෙනෙන Error Code එක හඳුනාගෙන, ඊට හේතුව (Reason) සහ කළ යුතු නිවැරදි කිරීම්/විසඳුම (Solution) "
                        "සිංහලෙන් ඉතා පැහැදිලිව පියවරෙන් පියවර විස්තර කරන්න."
                    )
                    response = model.generate_content([prompt, img])
                    
                    st.success(response.text)
                    
                    try:
                        tts = gTTS(text=response.text, lang='si')
                        audio_fp = io.BytesIO()
                        tts.write_to_fp(audio_fp)
                        st.audio(audio_fp, format='audio/mp3', autoplay=True)
                    except Exception:
                        pass
                except Exception as e:
                    st.error(f"දෝෂයක් මතු විය: {e}")