from autogen import ConversableAgent
from src.config.settings import LLM_CONFIG
from src.agents.executor_agent import process_requirements_wrapper

# Define the llm_config with the tool schema for the BA Agent
llm_config_with_tool = LLM_CONFIG.copy()
llm_config_with_tool["tools"] = [
    {
        "type": "function",
        "function": {
            "name": "process_requirements_wrapper",
            "description": "Process a requirements file to generate Jira user stories.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The absolute path to the requirements text file."
                    }
                },
                "required": ["file_path"]
            }
        }
    }
]


ba_agent = ConversableAgent(
    name="BA_Agent",
    system_message="You are a Business Analyst. Your only job is to analyze the user's request and, when provided with a file path, call the `process_requirements_wrapper` tool. Do not ask for confirmation. Call the tool directly.",
    llm_config=llm_config_with_tool, # Use the config with the tool schema
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1, # Only one attempt to call the tool
    code_execution_config=False,
    function_map={"process_requirements_wrapper": process_requirements_wrapper}  # Register the function
)