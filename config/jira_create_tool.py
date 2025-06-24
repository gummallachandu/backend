from atlassian import Jira
import os
from dotenv import load_dotenv
import logging
from typing import Dict

# Configure logging
logger = logging.getLogger(__name__)

# Load .env file
load_dotenv()

def create_jira_story(input_dict: Dict) -> str:
    """Create a Jira story with specified summary and description."""
    logger.info(f"Received input: {input_dict}")
    try:
        jira_url = os.getenv("JIRA_INSTANCE_URL")
        jira_username = os.getenv("JIRA_USERNAME")
        jira_api_token = os.getenv("JIRA_API_TOKEN")

        if not jira_url:
            logger.error("JIRA_INSTANCE_URL not set")
            raise ValueError("JIRA_INSTANCE_URL not set")
        if not jira_username:
            logger.error("JIRA_USERNAME not set")
            raise ValueError("JIRA_USERNAME not set")
        if not jira_api_token:
            logger.error("JIRA_API_TOKEN not set")
            raise ValueError("JIRA_API_TOKEN not set")

        jira = Jira(
            url=jira_url,
            username=jira_username,
            password=jira_api_token,
            cloud=True
        )
        logger.info(f"Jira client initialized with URL {jira_url}")

        project_key = os.getenv("JIRA_PROJECT_KEY", "SDLC")
        fields = {
            "project": {"key": project_key},
            "summary": input_dict.get("summary", "New User Story"),
            "description": input_dict.get("description", ""),
            "issuetype": {"name": "Story"}
        }

        logger.info(f"Creating Jira story with fields: {fields}")
        issue = jira.create_issue(fields=fields)
        issue_key = issue.get("key", "Unknown issue key")
        logger.info(f"Created Jira story: {issue_key}")
        return issue_key
    except Exception as e:
        logger.error(f"Error creating Jira story: {str(e)}")
        raise Exception(f"Error creating Jira story: {str(e)}")