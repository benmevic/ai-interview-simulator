import streamlit as st
import os
from config import Config
from database.db_manager import DatabaseManager
from services.auth_service import AuthService
from services.openai_service import OpenAIService
from services.cv_analyzer import CVAnalyzer

# Initialize services
db_manager = DatabaseManager()
auth_service = AuthService(db_manager)
openai_service = OpenAIService()
cv_analyzer = CVAnalyzer(openai_service)

# Page configuration
st.set_page_config(
    page_title="AI Interview Simulator",
    page_icon="🎯",
    layout="wide"
)

def main():
    st.title("🎯 AI Interview Simulator")
    st.write("Welcome to the AI-powered interview practice platform!")
    
    # Initialize session state
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Authentication
    if st.session_state.user is None:
        show_auth_page()
    else:
        show_main_app()

def show_auth_page():
    """Display authentication page."""
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            success, user_data, message = auth_service.login_user(username, password)
            if success:
                st.session_state.user = user_data
                st.success(message)
                st.rerun()
            else:
                st.error(message)
    
    with tab2:
        st.subheader("Register")
        new_username = st.text_input("Username", key="register_username")
        new_email = st.text_input("Email", key="register_email")
        new_password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        if st.button("Register"):
            if new_password != confirm_password:
                st.error("Passwords do not match!")
            else:
                success, message = auth_service.register_user(new_username, new_email, new_password)
                if success:
                    st.success(message + " Please login.")
                else:
                    st.error(message)

def show_main_app():
    """Display main application after authentication."""
    # Sidebar
    with st.sidebar:
        st.write(f"👤 Welcome, {st.session_state.user['username']}!")
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()
        
        st.divider()
        page = st.radio("Navigation", ["New Interview", "My Interviews", "Profile"])
    
    # Main content
    if page == "New Interview":
        show_new_interview_page()
    elif page == "My Interviews":
        show_my_interviews_page()
    elif page == "Profile":
        show_profile_page()

def show_new_interview_page():
    """Page for starting a new interview."""
    st.header("Start New Interview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        difficulty = st.selectbox(
            "Difficulty Level",
            ["easy", "medium", "hard"]
        )
        num_questions = st.slider("Number of Questions", 3, 10, 5)
    
    with col2:
        use_cv = st.checkbox("Upload CV for personalized questions")
        
    cv_file = None
    if use_cv:
        cv_file = st.file_uploader("Upload your CV (PDF)", type=['pdf'])
    
    if st.button("Start Interview", type="primary"):
        st.info("Interview feature coming soon! The backend is now set up.")
        # TODO: Implement interview logic

def show_my_interviews_page():
    """Page showing user's interview history."""
    st.header("My Interview History")
    
    interviews = db_manager.get_user_interviews(st.session_state.user['id'])
    
    if not interviews:
        st.info("You haven't taken any interviews yet. Start your first interview!")
    else:
        for interview in interviews:
            with st.expander(f"Interview on {interview['created_at']} - {interview['status']}"):
                st.write(f"**Difficulty:** {interview['difficulty_level']}")
                st.write(f"**Questions:** {interview['question_count']}")
                if interview['score']:
                    st.write(f"**Score:** {interview['score']:.1f}%")
                st.write(f"**Status:** {interview['status']}")

def show_profile_page():
    """Page showing user profile."""
    st.header("Profile")
    
    user = st.session_state.user
    st.write(f"**Username:** {user['username']}")
    st.write(f"**Email:** {user['email']}")
    st.write(f"**Member since:** {user['created_at']}")
    
    # Statistics
    interviews = db_manager.get_user_interviews(user['id'])
    st.subheader("Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Interviews", len(interviews))
    
    with col2:
        completed = len([i for i in interviews if i['status'] == 'completed'])
        st.metric("Completed", completed)
    
    with col3:
        if completed > 0:
            avg_score = sum(i['score'] for i in interviews if i['score']) / completed
            st.metric("Average Score", f"{avg_score:.1f}%")
        else:
            st.metric("Average Score", "N/A")

if __name__ == "__main__":
    main()