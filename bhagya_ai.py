import streamlit as st
import google.generativeai as genai
import os
import time
import PyPDF2
from PIL import Image

# 1. API Key සැකසුම (GitHub වෙත ආරක්ෂිතව Upload කිරීම සඳහා)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. භාග්‍ය AI හි කාර්මික විශේෂඥ දැනුම
system_instruction = (
    "ඔබේ නම 'භාග්‍ය' (Bhagya). ඔබව නිර්මාණය කළේ 'ශුභාග්‍ය' (Shubhagya) විසින්. "
    "ඔබ LB Engineering ආයතනයේ කාර්මික ස්වයංක්‍රීයකරණය (Industrial Automation) පිළිබඳ විශේෂඥ AI සහායකයෙකි. "
    "ඔබට Siemens, Mitsubishi, Xinje PLCs සහ Zoncn (T200 / NZ100), HBD, Delta, Siemens, Hyundai, Parker VFDs, "
    "Servo Motors සහ Drives පිළිබඳ ගැඹුරු තාක්ෂණික දැනුමක් ඇත. "
    "විශේෂයෙන්ම Zoncn T200 VFD පරාමිතීන් සම්බන්ධයෙන් ඉතා සැලකිලිමත් වන්න: "
    "P0.02 යනු Command Source Selection වේ (0: Keypad, 1: Terminal, 2: Communication). "
    "P0.03 යනු Main Frequency Source X Selection වේ (0/1: Digital setting, 2: FIV, 3: FIC, ආදී වශයෙන්). "
    "පරිශීලකයා පෙළ මඟින්, හඬ පණිවිඩයක් මඟින් හෝ ඡායාරූපයක් මඟින් ගැටලුවක් ඉදිරිපත් කළ විට, "
    "අදාළ VFD අත්පොත්වලට (Manuals) පදනම්ව නිවැරදි පරාමිතීන් සහ තොරතුරු සිංහලෙන් පියවරෙන් පියවර ලබා දෙන්න."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
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

st.write("ආයුබෝවන් ශුභාග්‍ය! මම භාග්‍ය. ඔබට අවශ්‍ය තාක්ෂණික සහාය ලබා ගැනීමට පහත ක්‍රම භාවිත කරන්න.")

# 5. ප්‍රධාන අංශ 5 (Tabs)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 පෙළින්", 
    "🎙️ කටහඬින්", 
    "📷 කැමරාවෙන්",
    "📱 ගැලරියෙන්",
    "📚 VFD Manuals"
])

MAX_RETRIES = 3
RETRY_DELAY = 15

# --- TAB 1: TEXT CHAT ---
with tab1:
    with st.form(key='chat_form'):
        user_input = st.text_input("ඔබේ ගැටලුව මෙතන ලියන්න (සිංහලෙන් හෝ ඉංග්‍රීසියෙන්):")
        submit_button = st.form_submit_button(label="යවන්න")

    if submit_button and user_input:
        with st.spinner('භාග්‍ය පිළිතුරු සකසමින්...'):
            for attempt in range(MAX_RETRIES):
                try:
                    response = model.generate_content(user_input)
                    st.success(response.text)
                    break
                except Exception as e:
                    if "429" in str(e) or "quota" in str(e).lower():
                        if attempt < MAX_RETRIES - 1:
                            st.warning(f"⏳ පද්ධතිය කාර්යබහුලයි. තත්පර {RETRY_DELAY} කින් නැවත උත්සාහ කරයි...")
                            time.sleep(RETRY_DELAY)
                        else:
                            st.error("API සීමාව ඉක්මවා ඇත. කරුණාකර මිනිත්තු කිහිපයකින් නැවත උත්සාහ කරන්න.")
                    else:
                        st.error(f"දෝෂයක් මතු විය: {e}")
                        break

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
                    audio_part = {"mime_type": "audio/wav", "data": audio_bytes}
                    prompt = "මෙම හඬ පණිවිඩයේ ඇති කාර්මික ගැටලුවට සිංහලෙන් පැහැදිලි පිළිතුරක් ලබා දෙන්න."
                    response = model.generate_content([prompt, audio_part])
                    st.success(response.text)
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
                    prompt = "මෙම VFD Error Code එක පරීක්ෂා කර, හේතුව සහ විසඳුම සිංහලෙන් පැහැදිලි කරන්න."
                    response = model.generate_content([prompt, img])
                    st.success(response.text)
                except Exception as e:
                    st.error(f"දෝෂයක් මතු විය: {e}")

# --- TAB 4: GALLERY / WHATSAPP PHOTO UPLOADER ---
with tab4:
    st.write("📱 **Phone එකේ හෝ PC ගැලරියේ (WhatsApp ඇතුළුව) Save කරගත් Error පින්තූර මෙතැනට Upload කරන්න:**")
    gallery_upload = st.file_uploader("ඡායාරූපයක් තෝරා ගැනීමට මෙතන ක්ලික් කරන්න", type=["jpg", "jpeg", "png", "webp"])
    
    if gallery_upload is not None:
        img = Image.open(gallery_upload)
        st.image(img, caption="Uploaded Error Photo", width=350)
        
        if st.button("🔍 මෙම ඡායාරූපය Analyze කරන්න"):
            with st.spinner('භාග්‍ය ඡායාරූපය පරීක්ෂා කරමින්...'):
                try:
                    prompt = "මෙහි පෙනෙන Error Code එක හඳුනාගෙන, ඊට හේතුව සහ කළ යුතු නිවැරදි කිරීම් සිංහලෙන් විස්තර කරන්න."
                    response = model.generate_content([prompt, img])
                    st.success(response.text)
                except Exception as e:
                    st.error(f"දෝෂයක් මතු විය: {e}")

# --- TAB 5: MULTIPLE PDF DATA SHEET READER ---
with tab5:
    st.write("📚 **පද්ධතියේ ගබඩා කර ඇති VFD Manuals වලින් ප්‍රශ්න අසන්න:**")
    
    # vfd ෆෝල්ඩරයේ ඇති PDF ලැයිස්තුව ගැනීම
    folder_path = "vfd"
    if os.path.exists(folder_path):
        pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
        
        if pdf_files:
            selected_pdf = st.selectbox("ඔබට අවශ්‍ය Data Sheet එක තෝරන්න:", pdf_files)
            pdf_question = st.text_input("මෙම Data Sheet එකෙන් දැනගැනීමට අවශ්‍ය දේ අසන්න:")
            
            if st.button("🔍 Manual එකෙන් හොයන්න") and pdf_question:
                pdf_file_path = os.path.join(folder_path, selected_pdf)
                with st.spinner(f'භාග්‍ය {selected_pdf} කියවමින්...'):
                    try:
                        pdf_reader = PyPDF2.PdfReader(pdf_file_path)
                        pdf_text = ""
                        # මුල් පිටු 15 පමණක් කියවීම (වේගය වැඩි කිරීමට සහ API සීමා වළක්වා ගැනීමට)
                        for page in range(min(15, len(pdf_reader.pages))):
                            pdf_text += pdf_reader.pages[page].extract_text()
                        
                        prompt = f"පහත දැක්වෙන්නේ '{selected_pdf}' VFD Manual එකෙහි දත්තයි. එය කියවා අසා ඇති ප්‍රශ්නයට සිංහලෙන් නිවැරදි පිළිතුරක් දෙන්න.\n\nප්‍රශ්නය: {pdf_question}\n\nManual දත්ත: {pdf_text[:30000]}"
                        response = model.generate_content(prompt)
                        st.success(response.text)
                    except Exception as e:
                        st.error(f"PDF කියවීමේ දෝෂයක් මතු විය: {e}")
        else:
            st.warning("vfd ෆෝල්ඩරය තුළ PDF ෆයිල් කිසිවක් නොමැත.")
    else:
        st.error("⚠️ 'vfd' නමින් ෆෝල්ඩරයක් සොයාගත නොහැක. කරුණාකර එය සාදා PDF ෆයිල් ඒ තුළට දමන්න.")