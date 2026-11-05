
import os
import streamlit as st

from resume_manager import upload_resume, get_current_resume

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
            <p>Discover your resume's strengths and improvement opportunities.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎤 Interview Assessment</h3>
            <p>Prepare for Technical, Managerial, and HR interviews.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Target Role</h3>
            <p>Explore your desired career role and required skills.</p>
        </div>
        """, unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Skill Gap Analysis</h3>
            <p>Understand your current skills and target role requirements.</p>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="feature-card">
            <h3>📚 Learning Roadmap</h3>
            <p>Build a personalized learning journey.</p>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Career Mentor</h3>
            <p>Get AI-powered career and technical guidance.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚀 Getting Started")

    st.info(
        "Visit Resume Analysis to upload your resume "
        "and create your career profile."
    )


# ---------- RESUME ANALYSIS ----------
elif page == "Resume Analysis":

    st.title("📄 Resume Analysis")

    st.write(
        "Upload your PDF resume to create your personalized "
        "AI career profile."
    )

    st.divider()

    # Current saved resume
    current_resume = get_current_resume()

    if current_resume:
        st.success("You already have a saved resume profile.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📁 Current Resume")
            st.write(f"**Filename:** {current_resume['filename']}")
            st.write(
                f"**Last Updated:** {current_resume['updated_at']}"
            )
            st.write(
                f"**Extracted Characters:** "
                f"{len(current_resume['extracted_text'])}"
            )

        with col2:
            file_path = current_resume["file_path"]

            if os.path.isfile(file_path):
                with open(file_path, "rb") as file:
                    st.download_button(
                        label="⬇️ Download Current Resume",
                        data=file.read(),
                        file_name=current_resume["filename"],
                        mime="application/pdf"
                    )
            else:
                st.warning("The saved PDF file could not be found.")

        with st.expander("Preview Extracted Resume Text"):
            st.text_area(
                "Extracted Content",
                value=current_resume["extracted_text"],
                height=300,
                disabled=True
            )

        st.divider()
        st.markdown("### 🔄 Replace Resume")
        st.caption(
            "Uploading another resume will replace your existing "
            "career profile."
        )

    else:
        st.info("No resume uploaded yet. Upload your first resume below.")

    # PDF uploader
    uploaded_file = st.file_uploader(
        "Choose your resume (PDF)",
        type=["pdf"],
        help="Upload a text-readable PDF resume."
    )

    if uploaded_file is not None:

        if st.button("🚀 Upload and Save Resume", type="primary"):

            try:
                with st.spinner("Processing your resume..."):

                    result = upload_resume(uploaded_file)

                st.success("Resume uploaded and saved successfully!")

                st.write(f"**Filename:** {result['filename']}")
                st.write(
                    f"**Extracted Characters:** "
                    f"{result['character_count']}"
                )

                st.session_state["resume_upload_success"] = True

            except ValueError as error:
                st.error(str(error))

            except Exception as error:
                st.error(f"Resume upload failed: {error}")

    # Refresh saved resume information after successful upload
    if st.session_state.get("resume_upload_success", False):
        st.session_state["resume_upload_success"] = False
        st.rerun()


# ---------- OTHER PAGES ----------
else:

    page_details = {
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
