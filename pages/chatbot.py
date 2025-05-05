import os
from dotenv import load_dotenv
import streamlit as st
from pathlib import Path
import base64
from typing import Dict, List
import google.generativeai as genai

# --- Load environment variables ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- Gemini-based Assistant ---
# --- Gemini-based Assistant ---
class AIAssistant:
    def __init__(self):
        self.chatbot = GeminiChat()
    
    def generate_response(self, user_input: str) -> str:
        return self.chatbot.get_response(user_input)

class GeminiChat:
    def __init__(self):
        # Use the correct model name for current API version
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.chat = self.model.start_chat(history=[])

    def get_response(self, user_input):
        try:
            response = self.chat.send_message(user_input)
            return response.text
        except Exception as e:
            # Enhanced error handling
            error_msg = f"⚠️ AI Service Error: {str(e)}"
            if "404" in str(e):
                error_msg += "\n\nPlease check:\n1. Model availability\n2. API endpoint configuration\n3. Account permissions"
            return error_msg

# --- Image Handling ---
def img_to_base64(img_path):
    try:
        img_path = Path(img_path).absolute()
        if not img_path.exists():
            return None
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image {img_path}: {str(e)}")
        return None

def get_assets_dir():
    possible_locations = [
        Path(__file__).parent.absolute() / "assets",
        Path(__file__).parent.parent.absolute() / "assets",
        Path.cwd().absolute() / "assets"
    ]
    for location in possible_locations:
        if location.exists():
            return location
    assets_dir = Path(__file__).parent.absolute() / "assets"
    assets_dir.mkdir(exist_ok=True)
    return assets_dir

assets_dir = get_assets_dir()

# --- Custom CSS ---
def get_custom_css(bg_image=None, profile_image=None):
    bg_style = f' url("data:image/jpeg;base64,{bg_image}")'
    
    return f"""
    <style>
    .stApp {{
        background: {bg_style};
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: white;
    }}

    .profile-img {{
        width: 150px;
        height: 150px;
        object-fit: cover;
        border-radius: 50%;
        border: 3px solid #64FFDA;
        box-shadow: 0 0 15px rgba(100, 255, 218, 0.6);
        animation: float 6s ease-in-out infinite;
    }}

    .user-message {{
        background-color: rgba(100, 255, 218, 0.2);
        border-radius: 10px;
        padding: 10px 15px;
        margin: 10px 0;
        border-left: 3px solid #64FFDA;
    }}

    .assistant-message {{
        background-color: rgba(139, 92, 246, 0.2);
        border-radius: 10px;
        padding: 10px 15px;
        margin: 10px 0;
        border-left: 3px solid #8b5cf6;
    }}

    .gradient-text {{
        background: linear-gradient(90deg, #64FFDA, #8b5cf6);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-weight: bold;
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-8px); }}
    }}
    </style>
    """

# --- Main Application ---
def main():
    # Load images
    bg_image = img_to_base64(assets_dir / "bg4.jpg")
    profile_image = img_to_base64(assets_dir / "hafsa.png")
    
    # Apply custom CSS
    st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")
    st.markdown(get_custom_css(bg_image, profile_image), unsafe_allow_html=True)

    # Initialize session state
    if "assistant" not in st.session_state:
        st.session_state.assistant = AIAssistant()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar with profile
    with st.sidebar:
        if profile_image:
            st.markdown(f"""
            <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{profile_image}" class="profile-img">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="width:150px; height:150px; border-radius:50%; background:#112240; 
                        margin: 0 auto 20px auto; display:flex; align-items:center; 
                        justify-content:center; border:3px solid #64FFDA; color:#64FFDA;">
                AI
            </div>
            """, unsafe_allow_html=True)

        st.markdown("## <span class='gradient-text' > Hafsa Kamali AI Assistant</span>", unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-top: 20px;">
            <p>Ask me about:</p>
            <ul>
                <li>Technology</li>
                <li>Machine Learning</li>
                <li>Web Development</li>
                <li>Data Science</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**Model: Gemini Pro**")
        st.markdown("**Provider: Google AI**")

    # Main Area
    st.markdown("# <span class='gradient-text'>Personal AI Assistant</span>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: rgba(17, 34, 64, 0.7); border-radius: 15px; padding: 20px; margin-bottom: 20px; color: white;">
    <h2 style="color: #64FFDA;">About the Founder: <span class='gradient-text'> Hafsa Kamali </span></h2>
    <p>Hafsa Kamali is an innovative technologist and AI enthusiast passionate about bridging the gap between cutting-edge technology and practical applications. With a strong background in machine learning, web development, and data science, she has developed this intelligent AI assistant to make advanced technological solutions more accessible.</p>

    <h3 style="color: #8b5cf6;">Professional Highlights</h3>
    <ul style="list-style-type: none; padding-left: 0;">
        <li>🚀 Expert in Machine Learning and Artificial Intelligence</li>
        <li>💻 Certified Web Developer</li>
        <li>📊 Data Science Practitioner</li>
        <li>🌐 Technology Innovation Advocate</li>
    </ul>

    <p>Through this AI assistant, Hafsa aims to demonstrate the potential of conversational AI in providing intelligent, context-aware support across various technological domains.</p>
    </div>
    """, unsafe_allow_html=True)

    chat_container = st.container()

    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)

        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">👻<strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">🐱‍👓<strong>Assistant:</strong> {message["content"]}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    user_input = st.chat_input("Type your message here...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            ai_response = st.session_state.assistant.generate_response(user_input)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        st.rerun()

if __name__ == "__main__":
    main()
