import streamlit as st
from groq import Groq

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Customer Support AI Agent", page_icon="🤖")
st.title("🤖 Customer Support AI Agent")
st.caption("Ask me anything about our products, orders, or support policies.")

# ---------- SYSTEM PROMPT (defines the agent's persona/business) ----------
SYSTEM_PROMPT = """You are a friendly, professional customer support AI agent for
'BrightCart', an online electronics store. You help customers with:
- Order status and shipping questions
- Product recommendations
- Returns and refunds (30-day return policy, free returns)
- Troubleshooting basic product issues
Always be polite, concise, and helpful. If you don't know something specific
(like a real order number), politely say you'd need to check the system and
suggest contacting human support at support@brightcart.example.com."""

# ---------- API KEY ----------
# Get a FREE API key at https://console.groq.com (no credit card required)
api_key = st.secrets.get("GROQ_API_KEY", None) or st.sidebar.text_input(
    "Enter your free Groq API key", type="password"
)

if not api_key:
    st.info("👈 Enter your free Groq API key in the sidebar to start chatting. Get one at https://console.groq.com")
    st.stop()

client = Groq(api_key=api_key)

# ---------- CHAT HISTORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Display past messages (skip system prompt)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- USER INPUT ----------
user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # fast, free Groq model
                messages=st.session_state.messages,
                temperature=0.5,
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
