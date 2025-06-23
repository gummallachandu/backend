from autogen import ConversableAgent
from src.config.settings import LLM_CONFIG
import logging
import json
import time
import streamlit as st
import os

logger = logging.getLogger(__name__)

def process_requirements(file_path: str, ba_agent, executor_agent) -> str:
    """A standalone function that encapsulates the requirements processing logic."""
    logger.info(f"TOOL: Running requirements processing for {file_path}")
    
    # Have BA Agent process the requirements
    chat_result = ba_agent.initiate_chat(
        recipient=executor_agent,
        message=f"Please process the requirements file at: {file_path}. Call process_requirements_wrapper with this file path.",
        clear_history=True,
        max_turns=2
    )
    
    if not chat_result or not chat_result.summary:
        logger.error("No response received from BA Agent")
        return "Error: Requirements processing failed. No response from the BA Agent."
    
    # Log the full BA-Agent chat history for debugging
    logger.info("BA-Agent chat history:")
    for msg in chat_result.chat_history:
        logger.info(f"{msg['name']}: {msg['content']}")
    
    last_message_str = chat_result.summary
    if "error" in last_message_str.lower() or "failed" in last_message_str.lower():
        logger.error(f"BA Agent reported error: {last_message_str}")
        return f"Error: Requirements processing failed: {last_message_str}"
    
    try:
        # Try to find and parse the JSON response
        json_part = last_message_str[last_message_str.find('{'):last_message_str.rfind('}')+1]
        tool_output = json.loads(json_part)
        stories_file_path = tool_output.get("file_path")
        if not stories_file_path:
            raise ValueError("Could not find 'file_path' in the response.")
        return stories_file_path
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Error parsing BA Agent response: {e}")
        return f"Error: {e}. Full response: {last_message_str}"

def request_user_approval(stories_file_path: str, workflow_id: str) -> str:
    """A standalone function that requests user approval via the Streamlit UI."""
    if not workflow_id:
        return "Error: Cannot request approval because workflow_id is not set."
    
    logger.info("TOOL: Requesting user approval via UI.")
    st.session_state["stories_for_approval"][workflow_id] = stories_file_path
    st.session_state["user_approval_status"][workflow_id] = "pending"
    
    while st.session_state.get("user_approval_status", {}).get(workflow_id) == "pending":
        time.sleep(2)

    approval_status = st.session_state.get("user_approval_status", {}).get(workflow_id, "rejected")
    
    if workflow_id in st.session_state.get("stories_for_approval", {}):
        del st.session_state["stories_for_approval"][workflow_id]
    if workflow_id in st.session_state.get("user_approval_status", {}):
        del st.session_state["user_approval_status"][workflow_id]
    
    return approval_status

def create_jira_tickets(stories_file_path: str) -> str:
    """A standalone function that simulates the Jira ticket creation phase."""
    logger.info("TOOL: Creating Jira tickets (simulated).")
    return f"Jira tickets for stories in {stories_file_path} created successfully."

class SupervisorAgent(ConversableAgent):
    """
    The central, LLM-driven supervisor that orchestrates the workflow by directly interacting with other agents.
    """
    def __init__(self, ba_agent=None, executor_agent=None, user_agent=None, **kwargs):
        super().__init__(
            name="Supervisor_Agent",
            system_message="""You are the SDLC supervisor. Your job is to orchestrate the workflow by:
1. First, sending the requirements file to the BA Agent for processing
2. Then having the User Agent display the stories and get approval
3. Finally creating Jira tickets once approved

When you receive a file path, initiate a chat with the BA Agent to process it.
When you receive approval, proceed with Jira ticket creation.
If any step fails, reply with {"TERMINATE": "<reason>"}.
When all steps complete successfully, reply with {"TERMINATE": "success"}.
""",
            llm_config=LLM_CONFIG,
            human_input_mode="NEVER",
            **kwargs
        )
        self.ba_agent = ba_agent
        self.executor_agent = executor_agent
        self.user_agent = user_agent
        logger.info("SupervisorAgent initialized.")

    def process_requirements(self, file_path: str) -> str:
        """Process requirements by having BA Agent work with Executor Agent."""
        logger.info(f"Processing requirements from: {file_path}")
        
        if not self.ba_agent:
            return "Error: BA Agent not initialized"
            
        chat_result = self.ba_agent.initiate_chat(
            recipient=self.executor_agent,
            message=f"Please process the requirements file at: {file_path}. Call process_requirements_wrapper with this file path.",
            clear_history=True,
            max_turns=2
        )
        
        if not chat_result or not chat_result.summary:
            logger.error("No response received from BA Agent")
            return "Error: Requirements processing failed. No response from the BA Agent."
        
        # Log the full BA-Agent chat history for debugging
        logger.info("BA-Agent chat history:")
        for msg in chat_result.chat_history:
            # Handle different message formats safely
            sender = msg.get('name', msg.get('role', 'Unknown'))
            content = msg.get('content', 'No content')
            logger.info(f"{sender}: {content}")
        
        last_message_str = chat_result.summary
        if "error" in last_message_str.lower() or "failed" in last_message_str.lower():
            logger.error(f"BA Agent reported error: {last_message_str}")
            return f"Error: Requirements processing failed: {last_message_str}"
        
        try:
            # Try to find and parse the JSON response
            json_part = last_message_str[last_message_str.find('{'):last_message_str.rfind('}')+1]
            tool_output = json.loads(json_part)
            stories_file_path = tool_output.get("file_path")
            if not stories_file_path:
                raise ValueError("Could not find 'file_path' in the response.")
            
            # Set the stories file in session state for the User Agent to display
            st.session_state["stories_file"] = os.path.basename(stories_file_path)
            
            # Have User Agent work with Executor Agent to display the stories
            if self.user_agent and self.executor_agent:
                display_result = self.user_agent.initiate_chat(
                    recipient=self.executor_agent,
                    message=f"Please display the stories from {stories_file_path} for user approval. Call display_stories_from_folder to show them.",
                    clear_history=True,
                    max_turns=2
                )
                logger.info(f"User Agent display result: {display_result.summary if display_result else 'No response'}")
                
                # Parse the display result to get stories
                if display_result and display_result.summary:
                    try:
                        display_json = json.loads(display_result.summary)
                        if display_json.get("status") == "success" and "stories" in display_json:
                            st.session_state["current_stories"] = display_json["stories"]
                    except Exception as e:
                        logger.error(f"Error parsing display result: {e}")
            
            return stories_file_path
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Error parsing BA Agent response: {e}")
            return f"Error: {e}. Full response: {last_message_str}"

    def request_user_approval(self, stories_file_path: str, workflow_id: str) -> str:
        """Request user approval via the Streamlit UI."""
        if not workflow_id:
            return "Error: Cannot request approval because workflow_id is not set."
        
        logger.info("Requesting user approval via UI.")
        # Store both the file path and the current stories in the session state
        st.session_state["stories_for_approval"][workflow_id] = stories_file_path
        st.session_state["user_approval_status"][workflow_id] = "pending"
        
        # If we have stories in memory, make sure they're available for display
        if "current_stories" not in st.session_state and os.path.exists(stories_file_path):
            try:
                with open(stories_file_path, 'r') as f:
                    st.session_state["current_stories"] = json.load(f)
            except Exception as e:
                logger.error(f"Error loading stories from file: {e}")
        
        while st.session_state.get("user_approval_status", {}).get(workflow_id) == "pending":
            time.sleep(2)

        approval_status = st.session_state.get("user_approval_status", {}).get(workflow_id, "rejected")
        
        # Clean up session state
        if workflow_id in st.session_state.get("stories_for_approval", {}):
            del st.session_state["stories_for_approval"][workflow_id]
        if workflow_id in st.session_state.get("user_approval_status", {}):
            del st.session_state["user_approval_status"][workflow_id]
        if "current_stories" in st.session_state:
            del st.session_state["current_stories"]
        
        return approval_status

    def create_jira_tickets(self, stories_file_path: str) -> str:
        """Create Jira tickets (simulated)."""
        logger.info("Creating Jira tickets (simulated).")
        return f"Jira tickets for stories in {stories_file_path} created successfully."

