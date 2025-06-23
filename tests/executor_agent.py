from autogen import UserProxyAgent
from src.tools.file_read_tool import read_file
import logging
import json
import os
from pathlib import Path
import streamlit as st

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_requirements_wrapper(file_path: str) -> str:
    """Process requirements and generate user stories."""
    try:
        logger.info(f"EXECUTOR: Processing requirements from: {file_path}")
        project_root = str(Path(__file__).parent.parent.parent)
        stories_dir = os.path.join(project_root, "stories")
        os.makedirs(stories_dir, exist_ok=True)

        # Handle relative paths by resolving against project root
        if file_path.startswith('./') or not os.path.isabs(file_path):
            file_path = os.path.join(project_root, file_path.lstrip('./'))
        
        # Ensure the file exists before reading
        if not os.path.exists(file_path):
            return f"Error: File not found at {file_path}"

        file_content = read_file(file_path)
        stories = []
        for line in file_content.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line[0].isdigit() and '.' in line or line.startswith('-'):
                if line.startswith('-'):
                    line = line[1:].strip()
                story = {
                    "summary": f"As a user, I want to {line.lower()}",
                    "description": f"User Story: As a user, I want to {line.lower()} so that I can achieve my goal efficiently.",
                    "priority": "Medium",
                    "story_points": 3,
                    "type": "User Story"
                }
                stories.append(story)

        filename = os.path.basename(file_path)
        stories_file = f"stories_{filename}"
        stories_path = os.path.join(stories_dir, stories_file)
        with open(stories_path, 'w') as f:
            json.dump(stories, f, indent=2)

        st.session_state["stories_file"] = stories_file
        st.session_state["workflow_status"] = "stories_generated"
        logger.info(f"EXECUTOR: Generated {len(stories)} stories at {stories_path}")
        return json.dumps({"status": "success", "message": f"Generated {len(stories)} stories", "file_path": stories_path})

    except Exception as e:
        logger.error(f"EXECUTOR: Error processing requirements: {str(e)}")
        return json.dumps({"status": "error", "message": f"Error: {str(e)}"})

def display_stories_from_folder() -> str:
    """Display stories from the stories folder."""
    try:
        # Get stories directory
        project_root = str(Path(__file__).parent.parent.parent)
        stories_dir = os.path.join(project_root, "stories")
        
        # Get stories file from session state
        stories_file = st.session_state.get("stories_file")
        logger.info(f"EXECUTOR: Looking for stories file: {stories_file}")
        
        if not stories_file:
            logger.warning("EXECUTOR: No stories file found in session state")
            return json.dumps({"status": "error", "message": "No stories file found"})
        
        # Construct full path to stories file
        stories_path = os.path.join(stories_dir, stories_file)
        logger.info(f"EXECUTOR: Reading stories from: {stories_path}")
        
        if not os.path.exists(stories_path):
            logger.warning(f"EXECUTOR: Stories file not found: {stories_path}")
            return json.dumps({"status": "error", "message": "Stories file not found"})
        
        # Read and return the stories
        try:
            with open(stories_path, 'r') as f:
                stories = json.load(f)
                logger.info(f"EXECUTOR: Successfully loaded {len(stories)} stories")
                # Store stories in session state for the UI
                st.session_state["current_stories"] = stories
                return json.dumps({
                    "status": "success",
                    "message": f"Loaded {len(stories)} stories",
                    "stories": stories
                })
        except Exception as e:
            logger.error(f"EXECUTOR: Error reading stories: {str(e)}")
            return json.dumps({"status": "error", "message": f"Error reading stories: {str(e)}"})
        
    except Exception as e:
        logger.error(f"EXECUTOR: Error displaying stories: {str(e)}")
        return json.dumps({"status": "error", "message": f"Error displaying stories: {str(e)}"})

# The ExecutorAgent is a UserProxyAgent that executes functions
executor_agent = UserProxyAgent(
    name="Executor_Agent",
    human_input_mode="NEVER",
    # The key change: directly map the function name to the callable
    function_map={
        "process_requirements_wrapper": process_requirements_wrapper,
        "display_stories_from_folder": display_stories_from_folder
    },
    code_execution_config=False,
    llm_config=False, # No LLM needed for pure execution
    system_message="You are an Executor Agent. You execute tool calls silently and return the result."
)
