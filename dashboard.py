
import streamlit as st

st.set_page_config(
    page_title="ResumeMentor AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM STYLING ----------
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
    }

    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }

    .hero {
        padding: 35px;
        border-radius: 18px;
        background: linear-gradient(120deg, #172554, #312E81, #1E1B4B);
        border: 1px solid #3730A3;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 38px;
        color: white;
        margin-bottom: 10px;
    }

    .hero p {
        color: #D1D5DB;
        font-size: 17px;
    }

    .feature-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 14px;
        padding: 22px;
        min-height: 190px;
        margin-bottom: 15px;
    }

    .feature-card h3 {
        color: #F3F4F6;
        font-size: 20px;
    }

    .feature-card p {
        color: #9CA3AF;
        font-size: 14px;
    }

    .section-heading {
        color: #F3F4F6;
        font-size: 24px;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("# 🎯 ResumeMentor AI")
    st.caption("Your Resume. Your Skills. Your AI Mentor.")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Resume Analysis",
            "Interview Assessment",
            "Target Role",
            "Learning Roadmap",
            "AI Chat"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.caption("AI-powered career development")
    st.caption("Project status: Under Development")


# ---------- DASHBOARD ----------
if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>Welcome to ResumeMentor AI 👋</h1>
        <p>
            Your personal AI-powered career mentor.
            Understand your strengths, improve your resume,
            prepare for interviews, and build your future.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">Your Career Development Hub</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📄 Resume Analysis</h3>
            <p>
                Upload your resume and discover its strengths,
                weaknesses, and improvement opportunities.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎤 Interview Assessment</h3>
            <p>
                Prepare for Technical, Managerial, and HR
                interviews at different difficulty levels.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Target Role</h3>
            <p>
                Explore your desired career role and identify
                the skills needed to pursue it.
            </p>
        </div>
        """, unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Skill Gap Analysis</h3>
            <p>
                Understand the difference between your current
                skills and your target role requirements.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="feature-card">
            <h3>📚 Learning Roadmap</h3>
            <p>
                Build a personalized learning path to improve
                your knowledge and career readiness.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Career Mentor</h3>
            <p>
                Interact with an AI assistant for career,
                resume, and technical guidance.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚀 Getting Started")

    st.info(
        "Your career dashboard is being prepared. "
        "Resume upload and personalized analysis will be "
        "integrated in the next development stages."
    )


# ---------- OTHER PAGES ----------
else:
    page_details = {
        "Resume Analysis": (
            "📄 Resume Analysis",
            "Upload and analyze your resume with AI. Coming soon."
        ),
        "Interview Assessment": (
            "🎤 Interview Assessment",
            "Technical, Managerial, and HR interview assessments. Coming soon."
        ),
        "Target Role": (
            "🎯 Target Role",
            "Explore career roles and required skills. Coming soon."
        ),
        "Learning Roadmap": (
            "📚 Learning Roadmap",
            "Build your personalized learning journey. Coming soon."
        ),
        "AI Chat": (
            "🤖 AI Career Mentor",
            "Your existing AI chat functionality will be integrated here."
        )
    }

    title, description = page_details[page]

    st.title(title)
    st.info(description)
