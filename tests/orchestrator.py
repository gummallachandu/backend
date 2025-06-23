from src.agents.ba_agent import ba_agent
from src.agents.executor_agent import executor_agent
from src.agents.user_agent import user_agent
from src.agents.supervisor_agent import SupervisorAgent
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def start_supervisor_workflow(file_path: str, workflow_id: str) -> bool:
    """Starts the definitive, LLM-driven supervisor workflow."""
    try:
        # Create the supervisor agent with direct access to other agents
        supervisor = SupervisorAgent(
            ba_agent=ba_agent,
            executor_agent=executor_agent,
            user_agent=user_agent
        )
        
        logger.info(f"Orchestrator: Starting DEFINITIVE workflow {workflow_id}")
        
        # Process requirements
        stories_file_path = supervisor.process_requirements(file_path)
        if stories_file_path.startswith("Error:"):
            logger.error(f"Orchestrator: Requirements processing failed: {stories_file_path}")
            return False
            
        # Request user approval
        approval_status = supervisor.request_user_approval(stories_file_path, workflow_id)
        if approval_status != "approved":
            logger.error(f"Orchestrator: User rejected stories: {approval_status}")
            return False
            
        # Create Jira tickets
        result = supervisor.create_jira_tickets(stories_file_path)
        if "successfully" not in result.lower():
            logger.error(f"Orchestrator: Jira ticket creation failed: {result}")
            return False
            
        logger.info("Orchestrator: Workflow completed successfully")
        return True
            
    except Exception as e:
        logger.error(f"Orchestrator: Critical error during workflow execution: {str(e)}", exc_info=True)
        return False
