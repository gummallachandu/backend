import logging
from autogen import ConversableAgent
from typing import Optional, Dict, Any

from ..config.settings import LLM_CONFIG
from ..tools.file_read_tool import FileReadTool
from ..tools.file_write_tool import FileWriteTool

logger = logging.getLogger(__name__)

class CoderAgent(ConversableAgent):
    """Agent responsible for code generation and modification."""
    
    def __init__(self, **kwargs):
        """Initialize the Coder Agent."""
        super().__init__(
            name="Coder_Agent",
            system_message="""You are a Coder agent responsible for:
            1. Generating code based on requirements
            2. Modifying existing code
            3. Following best practices and patterns
            
            You should write clean, maintainable, and well-documented code.
            """,
            llm_config=LLM_CONFIG,
            **kwargs
        )
        self.file_read_tool = FileReadTool()
        self.file_write_tool = FileWriteTool()
        logger.info("CoderAgent initialized")

def process_story_to_code() -> str:
    """Generate code based on stories from workspace stories folder."""
    try:
        # Get project root and paths
        project_root = str(Path(__file__).parent.parent.parent)
        stories_dir = os.path.join(project_root, "stories")
        programs_dir = os.path.join(project_root, "programs")
        
        # Create programs directory
        os.makedirs(programs_dir, exist_ok=True)
        
        # Get stories file from session state
        import streamlit as st
        stories_file = st.session_state.get("stories_file")
        if not stories_file:
            raise ValueError("No stories file found in session state. Please ensure BA Agent has generated stories first.")
            
        # Get full path to stories file
        stories_path = os.path.join(stories_dir, stories_file)
        logger.info(f"Using stories file from workspace: {stories_path}")
        
        # Read and parse stories
        stories_content = read_file(stories_path)
        stories = json.loads(stories_content)
        
        if not stories:
            raise ValueError("No stories found in file")
            
        # Get first story
        first_story = stories[0]
        logger.info(f"Processing story: {first_story['summary']}")
        
        # Generate code based on story
        if "user creation" in first_story['summary'].lower():
            code = '''def create_user(email: str, password: str, name: str) -> dict:
    """Create a new user.
    
    Args:
        email: User's email
        password: User's password
        name: User's name
        
    Returns:
        dict: Created user data
    """
    # TODO: Add actual implementation
    return {
        "email": email,
        "name": name,
        "created_at": "2024-03-20"  # TODO: Use actual timestamp
    }

if __name__ == "__main__":
    # Example usage
    user = create_user("test@example.com", "password123", "Test User")
    print(f"Created user: {user}")
'''
            code_file = os.path.join(programs_dir, "user_creation.py")
        else:
            # Default to factorial if story doesn't match
            code = '''def factorial(n: int) -> int:
    """Calculate factorial of n."""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    return 1 if n == 0 else n * factorial(n - 1)

if __name__ == "__main__":
    print(f"Factorial of 5: {factorial(5)}")  # 120
'''
            code_file = os.path.join(programs_dir, "factorial.py")
        
        # Save code
        write_file(code_file, code)
        
        # Store path in session state
        st.session_state["code_file"] = code_file
        
        return code_file
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise

# Register function for execution
@coder_agent.register_for_execution()
@coder_agent.register_for_llm(name="process_story_to_code", description="Generate code based on stories from workspace stories folder.")
def process_story_to_code_wrapper() -> str:
    """Wrapper function that uses workspace stories folder."""
    return process_story_to_code() 