# =========================================================
# Dr. APJ Abdul Kalam Digital Mentor (Educational Simulation)
# Ethics-first • National-security-safe • Voice-enabled
# =========================================================

import streamlit as st
from groq import Groq
from elevenlabs.client import ElevenLabs
import base64

# -----------------------------
# API CONFIG (from secrets)
# -----------------------------
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
ELEVENLABS_API_KEY = st.secrets.get("ELEVENLABS_API_KEY", "")
KALAM_VOICE_ID = st.secrets.get("KALAM_VOICE_ID", "")

if not GROQ_API_KEY or not ELEVENLABS_API_KEY or not KALAM_VOICE_ID:
    st.error("Missing API keys or Voice ID. Please set them in .streamlit/secrets.toml")
    st.stop()

groq_client = Groq(api_key=GROQ_API_KEY)
el_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# -----------------------------
# UI CONFIG
# -----------------------------
st.set_page_config(
    page_title="Dr. APJ Abdul Kalam Digital Mentor",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
.main { background-color: #000b1e; color: #e0e0e0; }
.stButton>button { background-color: #ffd700; color: black; font-weight: bold; }
.stSidebar { background-color: #0b132b; }
small.disclaimer { color:#b8b8b8; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Dr. APJ Abdul Kalam Digital Mentor")
st.write("Science • Defence (Education) • Space • Nation Building — Ethics First")

st.markdown(
    "<small class='disclaimer'>Disclaimer: This is a digital mentor inspired by Dr. APJ Abdul Kalam for educational purposes. "
    "It is not an official representation and does not provide classified defence information.</small>",
    unsafe_allow_html=True
)

# =========================================================
# DIGITAL MENTOR PROFILE (Identity + Style + Ethics)
# =========================================================
KALAM_SYSTEM_PROMPT = """
You are a Digital Mentor inspired by Dr. APJ Abdul Kalam — former President of India,
Aerospace Scientist, Bharat Ratna awardee, and a lifelong teacher of youth.

Mission:
Inspire students through science, discipline, ethics, innovation, and national purpose.

IDENTITY & VALUES
- Scientist, Teacher, Visionary Leader
- Aerospace Engineering, Missile Technology, Space Research
- Vision: Developed India (Viksit Bharat)
- Values: humility, integrity, scientific temper, patriotism, service to humanity, youth empowerment

COMMUNICATION & TEACHING STYLE
- Speak as a mentor and guide; tone inspiring, calm, respectful, fatherly
- Mix simple English and Telugu
- Address users as: "My dear young friend"
- Explain with clear examples and connect science to real life
- Motivate youth towards innovation and nation building
- You may reference: Wings of Fire, Ignited Minds, India Vision 2020

ETHICS & NATIONAL SECURITY (MANDATORY)
You must NOT discuss:
- Classified military information
- Current defence strategies
- Weapon construction methods
- Tactical/operational military details
- Security vulnerabilities

You may discuss ONLY:
- Public-domain defence history
- Educational aerospace & missile science
- DRDO, ISRO, IGMDP (publicly available knowledge)
- National development through science
- Career guidance for students

Always promote peace, development, ethical science, and responsible technology.

CLOSING
Always respond as a Digital Mentor inspired by Dr. APJ Abdul Kalam.
End with a brief motivation for youth and national progress.
Signature close: "Dream big. Work hard. Serve the nation. Build the future."
"""

# -----------------------------
# SESSION MEMORY
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# DEFENCE MIND MAP (Mermaid)
# -----------------------------
def generate_defense_mindmap():
    return """
    mindmap
      root((Indian Defence System — Education))
        IGMDP
          Agni
          Prithvi
          Akash
          Trishul
          Nag
        DRDO
          Aerospace
          Electronics
          Missiles
          Radars
        Viksit Bharat 2047
          Atmanirbhar Defence
          Indigenous Manufacturing
          Space & AI (Education)
        Career Path
          Aerospace Engineering
          Defence Scientist
          ISRO
          DRDO
    """

def render_mermaid(mermaid_code):
    html = f"""
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{ startOnLoad: true }});</script>
    <div class="mermaid">
    {mermaid_code}
    </div>
    """
    st.components.v1.html(html, height=600, scrolling=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🇮🇳 Kalam AI Menu")
if st.sidebar.button("📊 Defence Mind Map (Public Domain)"):
    st.subheader("Dr. Kalam Vision — Indian Defence Mind Map (Education)")
    render_mermaid(generate_defense_mindmap())

st.sidebar.markdown("---")
st.sidebar.write("Ethical AI | National Security Safe | Education Only")

# -----------------------------
# SHOW CHAT HISTORY
# -----------------------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# USER INPUT
# -----------------------------
user_query = st.chat_input("Ask the Digital Mentor...")

if user_query:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # -------------------------
    # AI RESPONSE (Groq)
    # -------------------------
    with st.chat_message("assistant"):
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": KALAM_SYSTEM_PROMPT},
                *st.session_state.chat_history
            ]
        )

        full_response = response.choices[0].message.content
        st.markdown(full_response)
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

    # -------------------------
    # VOICE OUTPUT (ElevenLabs)
    # -------------------------
    try:
        audio_stream = el_client.generate(
            text=full_response,
            voice=KALAM_VOICE_ID,
            model="eleven_multilingual_v2"
        )

        audio_bytes = b"".join(audio_stream)
        audio_base64 = base64.b64encode(audio_bytes).decode()

        audio_html = f"""
        <audio autoplay controls>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Voice generation error: {e}")
