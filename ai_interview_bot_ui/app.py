import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Powered Interview Bot",
    layout="centered"
)

# ---------- STYLES ----------
st.markdown("""
<style>
.stApp { background-color: #0f172a; }
.box {
    background-color: #ffffff;
    padding: 35px;
    border-radius: 14px;
    border: 2px solid #e5e7eb;
    box-shadow: 0 10px 25px rgba(0,0,0,0.35);
}
.box h1 { text-align: center; color: #111827; }
.box p {
    text-align: center;
    font-size: 15px;
    line-height: 1.7;
    color: #374151;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "resume" not in st.session_state:
    st.session_state.resume = None

# ---------- QUESTIONS ----------
questions = [
    "Tell me about yourself.",
    "What are your technical skills?",
    "Describe a challenging situation you faced and how you handled it.",
    "Why should we hire you?"
]
total_questions = len(questions)

# ---------- HOME ----------
if st.session_state.page == "home":

    st.markdown("""
    <div class="box">
        <h1>🤖 AI Powered Interview Bot</h1>
        <p>
        An intelligent mock interview platform that supports
        live voice and text responses, resume-based interviews,
        and personalized feedback.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Start Interview"):
        st.session_state.page = "setup"

# ---------- SETUP ----------
elif st.session_state.page == "setup":

    st.markdown("""
    <div class="box">
        <h1>⚙️ Interview Setup</h1>
        <p>Select domain and upload resume</p>
    </div>
    """, unsafe_allow_html=True)

    domain = st.selectbox(
        "🎯 Select Interview Domain",
        ["IT", "HR", "Marketing"]
    )

    resume = st.file_uploader(
        "📄 Upload Resume (PDF)",
        type=["pdf"]
    )

    if resume:
        st.session_state.resume = resume
        st.success("Resume uploaded successfully")

    if st.button("➡️ Proceed to Interview"):
        st.session_state.domain = domain
        st.session_state.page = "interview"

# ---------- INTERVIEW ----------
elif st.session_state.page == "interview":

    q = st.session_state.q_index
    st.progress((q + 1) / total_questions)
    st.markdown(f"**Question {q + 1} of {total_questions}**")
    st.subheader(questions[q])

    mode = st.radio(
        "Choose answer mode",
        ["Text", "Voice (Live)"],
        horizontal=True,
        key=f"mode_{q}"
    )

    if mode == "Text":
        answer = st.text_area(
            "Your Answer",
            value=st.session_state.answers.get(q, {}).get("response", ""),
            height=150,
            key=f"text_{q}"
        )
        audio = None
    else:
        st.info("🎙️ Speak your answer")
        audio = st.audio_input("Record", key=f"audio_{q}")
        answer = "[Live voice response recorded]" if audio else ""

    def next_q():
        st.session_state.answers[q] = {
            "mode": mode,
            "response": answer,
            "audio": audio
        }
        if q + 1 < total_questions:
            st.session_state.q_index += 1
        else:
            st.session_state.page = "report"

    def prev_q():
        st.session_state.answers[q] = {
            "mode": mode,
            "response": answer,
            "audio": audio
        }
        if q > 0:
            st.session_state.q_index -= 1

    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("⬅ Back", on_click=prev_q, disabled=(q == 0))
    with col3:
        st.button("Next ➡" if q + 1 < total_questions else "Submit", on_click=next_q)

# ---------- REPORT ----------
elif st.session_state.page == "report":

    st.markdown("""
    <div class="box">
        <h1>📊 Interview Performance Report</h1>
        <p>Personalized interview summary</p>
    </div>
    """, unsafe_allow_html=True)

    st.metric("Confidence Score", "78%")
    st.metric("Performance Level", "Intermediate")

    st.subheader("📝 Responses")
    for i, qn in enumerate(questions):
        st.markdown(f"**Q{i+1}: {qn}**")
        st.write(st.session_state.answers[i]["response"])

    # ---------- PDF GENERATION ----------
    def generate_pdf():
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        text = c.beginText(40, 800)

        text.setFont("Helvetica", 11)
        text.textLine("AI Powered Interview Bot - Performance Report")
        text.textLine("")
        text.textLine("Confidence Level: Intermediate")
        text.textLine("Confidence Score: 78%")
        text.textLine("")

        for i, qn in enumerate(questions):
            text.textLine(f"Q{i+1}: {qn}")
            text.textLine(f"Answer: {st.session_state.answers[i]['response']}")
            text.textLine("")

        c.drawText(text)
        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer

    pdf = generate_pdf()

    st.download_button(
        "📥 Download Report (PDF)",
        data=pdf,
        file_name="Interview_Report.pdf",
        mime="application/pdf"
    )

    if st.button("🔄 Restart Interview"):
        st.session_state.page = "home"
        st.session_state.q_index = 0
        st.session_state.answers = {}
        st.session_state.resume = None
