import streamlit as st
import json
import os
from pathlib import Path
import logging
import time
from autogen import ConversableAgent
from src.config.settings import LLM_CONFIG

logger = logging.getLogger(__name__)

# The user agent is now a symbolic participant. Its role is to exist as a
# conceptual endpoint that the supervisor can hand off to. The actual UI
# interaction is handled by the frontend (app.py) and the supervisor's 
# waiting loop.

# Define the llm_config with the tool schema for the User Agent
llm_config_with_tool = LLM_CONFIG.copy()
llm_config_with_tool["tools"] = [
    {
        "type": "function",
        "function": {
            "name": "display_stories_from_folder",
            "description": "Display stories from the stories folder in the UI.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

user_agent = ConversableAgent(
    name="User_Agent",
    system_message="""You are a User Interface agent that helps display information to the user.
When asked to display stories, call the display_stories_from_folder function.
Do not ask for confirmation. Call the function directly.""",
    llm_config=llm_config_with_tool,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    code_execution_config=False
)

def display_stories_from_folder():
    """Display stories from the stories folder."""
    try:
        # Get stories directory
        project_root = str(Path(__file__).parent.parent.parent)
        stories_dir = os.path.join(project_root, "stories")
        
        # Get stories file from session state
        stories_file = st.session_state.get("stories_file")
        logger.info(f"Looking for stories file: {stories_file}")
        
        if not stories_file:
            # Try to find the most recent stories file
            story_files = [f for f in os.listdir(stories_dir) if f.startswith("stories_")]
            if story_files:
                stories_file = sorted(story_files)[-1]  # Get the most recent file
                logger.info(f"Found most recent stories file: {stories_file}")
                # Update session state with the found file
                st.session_state["stories_file"] = stories_file
            else:
                logger.warning("No stories file found. Please generate stories first.")
                return "No stories found"
        
        # Construct full path to stories file
        stories_path = os.path.join(stories_dir, stories_file)
        logger.info(f"Reading stories from: {stories_path}")
        
        if not os.path.exists(stories_path):
            logger.warning(f"Stories file not found: {stories_path}")
            return "Stories file not found"
        
        # Just verify the stories exist and are valid JSON
        try:
            with open(stories_path, 'r') as f:
                stories = json.load(f)
                logger.info(f"Successfully loaded {len(stories)} stories")
                # Don't display with st.json - let the main app handle UI
                return f"Stories loaded successfully. {len(stories)} stories ready for approval."
        except Exception as e:
            logger.error(f"Error reading stories: {str(e)}")
            return f"Error reading stories: {str(e)}"
        
    except Exception as e:
        logger.error(f"Error displaying stories: {str(e)}")
        return f"Error displaying stories: {str(e)}"

def display_code_from_folder():
    """Display generated code from the programs folder."""
    try:
        # Get programs directory
        project_root = str(Path(__file__).parent.parent.parent)
        programs_dir = os.path.join(project_root, "programs")
        
        # Get code file from session state
        code_file = st.session_state.get("code_file")
        logger.info(f"Looking for code file: {code_file}")
        
        if not code_file:
            # Try to find the most recent Python file
            code_files = [f for f in os.listdir(programs_dir) if f.endswith(".py")]
            if code_files:
                code_file = sorted(code_files)[-1]  # Get the most recent file
                logger.info(f"Found most recent code file: {code_file}")
                # Update session state with the found file
                st.session_state["code_file"] = code_file
            else:
                logger.warning("No code file found. Please generate code first.")
                return "No code found"
        
        # Construct full path to code file
        code_path = os.path.join(programs_dir, code_file)
        logger.info(f"Reading code from: {code_path}")
        
        if not os.path.exists(code_path):
            logger.warning(f"Code file not found: {code_path}")
            return "Code file not found"
        
        # Just verify the code exists and is readable
        try:
            with open(code_path, 'r') as f:
                code_content = f.read()
                logger.info(f"Successfully loaded code file: {len(code_content)} characters")
                # Don't display with st.code - let the main app handle UI
                return f"Code loaded successfully. {len(code_content)} characters ready for approval."
        except Exception as e:
            logger.error(f"Error reading code: {str(e)}")
            return f"Error reading code: {str(e)}"
        
    except Exception as e:
        logger.error(f"Error displaying code: {str(e)}")
        return f"Error displaying code: {str(e)}"