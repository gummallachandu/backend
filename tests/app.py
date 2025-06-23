import streamlit as st
import os
from pathlib import Path
import json
from datetime import datetime
from src.orchestrator import start_supervisor_workflow
from src.agents.user_agent import user_agent
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app_log.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Project root
project_root = str(Path(__file__).parent.parent)

def init_session_state():
    """Initialize Streamlit session state"""
    if "workflow_id" not in st.session_state:
        st.session_state["workflow_id"] = None
    if "uploaded_file_path" not in st.session_state:
        st.session_state["uploaded_file_path"] = None
    if "workflow_running" not in st.session_state:
        st.session_state["workflow_running"] = False
    if "stories_file" not in st.session_state:
        st.session_state["stories_file"] = None
    if "current_stories" not in st.session_state:
        st.session_state["current_stories"] = None
    
    # Initialize the keys needed for the user approval workflow
    if "stories_for_approval" not in st.session_state:
        st.session_state["stories_for_approval"] = {}
    if "user_approval_status" not in st.session_state:
        st.session_state["user_approval_status"] = {}

def display_ui_components():
    """Display UI components based on the current session state."""
    
    workflow_id = st.session_state.get("workflow_id")
    if not workflow_id:
        st.info("Upload a file and start the workflow.")
        return

    # Debug information
    if st.session_state.get("workflow_running"):
        st.info(f"Workflow {workflow_id} is running. Please wait...")
        st.spinner()
        # Log session state for debugging
        logger.info(f"Session state during workflow: {st.session_state}")

    # Check if approval is pending for the current workflow
    if st.session_state.get("stories_for_approval", {}).get(workflow_id):
        stories_file_path = st.session_state["stories_for_approval"][workflow_id]
        stories = None
        
        # First try to get stories from session state
        if st.session_state.get("current_stories"):
            stories = st.session_state["current_stories"]
            logger.info("Using stories from session state")
        # If not in session state, try to read from file
        elif os.path.exists(stories_file_path):
            try:
                with open(stories_file_path, 'r') as f:
                    stories = json.load(f)
                logger.info(f"Read stories from file: {stories_file_path}")
                # Store in session state for future use
                st.session_state["current_stories"] = stories
            except Exception as e:
                logger.error(f"Error reading stories file: {e}")
                st.error(f"Error reading stories file: {e}")
                return
        else:
            st.error("Stories not found. Please try again.")
            logger.error(f"Stories file not found: {stories_file_path}")
            logger.info(f"Current session state: {st.session_state}")
            return
            
        if stories:
            st.subheader("Generated Stories for Your Approval")
            # If stories is a JSON string, parse it
            if isinstance(stories, str):
                try:
                    stories_data = json.loads(stories)
                    if "stories" in stories_data:
                        stories = stories_data["stories"]
                except:
                    pass
            
            # Display stories in a more readable format
            if isinstance(stories, list):
                for idx, story in enumerate(stories, 1):
                    with st.expander(f"Story {idx}: {story.get('summary', 'No Summary')}", expanded=True):
                        st.write("**Description:**", story.get('description', 'No Description'))
                        st.write("**Priority:**", story.get('priority', 'No Priority'))
                        st.write("**Story Points:**", story.get('story_points', 'Not Set'))
                        st.write("**Type:**", story.get('type', 'Not Set'))
            else:
                st.warning("Stories data is not in the expected format")
                logger.warning(f"Unexpected stories format: {type(stories)}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Approve Stories", key=f"approve_{workflow_id}"):
                    st.session_state["user_approval_status"][workflow_id] = "approved"
                    st.success("Stories approved! The workflow will now continue.")
                    # Force a rerun to clear the approval UI and show progress
                    time.sleep(2)
                    st.rerun()

            with col2:
                if st.button("Reject Stories", key=f"reject_{workflow_id}"):
                    st.session_state["user_approval_status"][workflow_id] = "rejected"
                    st.warning("Stories rejected. The workflow will now terminate.")
                    # Force a rerun to reflect the change
                    time.sleep(2)
                    st.rerun()
        else:
            st.error("No stories found for approval.")
            logger.error("Stories object is None or empty")

def main():
    st.title("SDLC Automation (Supervisor Orchestrated)")

    init_session_state()

    # File upload
    uploaded_file = st.file_uploader("Choose a file", type=['txt'])
    
    if uploaded_file is not None and not st.session_state.get("uploaded_file_path"):
        input_dir = os.path.join(project_root, "input")
        os.makedirs(input_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"upload_{timestamp}.txt"
        file_path = os.path.join(input_dir, new_filename)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state["uploaded_file_path"] = file_path
        st.success(f"File uploaded and saved as: {new_filename}")

    # Start workflow button
    if st.button("Start Workflow") and st.session_state["uploaded_file_path"]:
        if not st.session_state.get("workflow_running"):
            st.session_state["workflow_running"] = True
            st.session_state["workflow_id"] = f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            with st.spinner(f"Starting workflow {st.session_state.workflow_id}..."):
                # This will now block until the workflow is complete or needs input
                success = start_supervisor_workflow(
                    st.session_state["uploaded_file_path"], 
                    st.session_state.workflow_id
                )

            st.session_state["workflow_running"] = False # Workflow finished
            
            if success:
                st.success(f"Workflow {st.session_state.workflow_id} completed successfully!")
            else:
                st.error(f"Workflow {st.session_state.workflow_id} failed or was rejected.")
            
            # Reset for next run
            st.session_state["uploaded_file_path"] = None
            st.rerun()
        else:
            st.warning("A workflow is already in progress.")

    # This function will now handle showing the approval buttons
    display_ui_components()

if __name__ == "__main__":
    main()