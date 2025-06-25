Infrastructure Provisioning Request: AutoGen-Powered SDLC Automation Platform
To: DevOps Team
From: GenAI Development Team
Date: June 22, 2025

1. Project Overview
This document outlines the infrastructure requirements for deploying a new AI-powered SDLC automation platform. The system uses a multi-agent framework (AutoGen) to automate tasks from requirements analysis to Jira ticket creation, with a Streamlit front-end for user interaction and FastAPI for backend tools. The goal is to create a scalable, secure, and observable environment on AWS.

2. High-Level Architecture
The platform consists of two primary services running on an EKS cluster:

AutoGen Application (POD-1): A public-facing service that runs the main Streamlit UI and the core AutoGen supervisor and agent orchestration logic.

Tools Service (POD-2): An internal-only service that hosts FastAPI microservices, which are called by the AutoGen agents to perform specific tasks (e.g., file processing, API integrations).

The system will use S3 for input storage and DynamoDB as a persistent memory and state management layer for the agent workflows. All services will be monitored via CloudWatch logs.

3. Detailed Infrastructure Requirements
Please provision the following AWS resources:

a. AWS S3 (Input File Storage)

Bucket Name: genai-autogen-sdlc-input

Purpose: To store input files (e.g., requirement documents) uploaded by users via the Streamlit application.

Access Control: The AutoGen Application pod (POD-1) requires programmatic Read/Write access. This should be managed via an IAM Role for Service Account (IRSA).

b. AWS DynamoDB (Workflow State Management)

Table Name: genai-autogen-sdlc-workflows (Note: Clarified from genai-autogen-sdlc- to be more descriptive).

Purpose: To serve as a persistent, global memory store for the multi-agent system. The table will store workflow state, agent-to-agent context, task status, conversation history, and transitions.

Primary Key (Suggestion):

Partition Key: workflow_id (String)

Sort Key: state_id or timestamp (String or Number)

Access Control: Both the AutoGen Application pod (POD-1) and the Tools pod (POD-2) require programmatic Read/Write access (via IRSA).

c. AWS EKS (Application Compute)

Cluster Configuration: A standard EKS cluster provisioned to run containerized applications.

Deployment 1: AutoGen Application (POD-1)

Container Source: Git Repository genai-sdlc-autogent-app.

Purpose: Runs the main multi-agent workflow supervisor and the Streamlit UI.

Networking: Requires an Ingress controller (e.g., AWS Load Balancer Controller) to expose the Streamlit service to the public internet via a secure (HTTPS) endpoint.

Deployment 2: Tools Service (POD-2)

Container Source: Git Repository genai-sdlc-tool-app.

Purpose: Hosts backend tools as FastAPI microservices, which are called by the AutoGen agents (e.g., the Executor Agent).

Networking: Exposed internally within the cluster via a ClusterIP service. This pod should NOT be accessible from the public internet.

d. AWS CloudWatch (Logging & Monitoring)

Log Groups: Please create two distinct CloudWatch Log Groups to separate concerns and simplify debugging.

Log Group Naming Convention (Suggestion):

/eks/genai-sdlc/autogen-app (for POD-1)

/eks/genai-sdlc/tools-app (for POD-2)

Integration: Logs should be streamed from the EKS pods to their respective log groups, preferably using a log forwarder like Fluent Bit.

e. SonarQube (Code Quality & Security)

Requirement: A SonarQube dashboard for static analysis and security scanning.

Integration: Please integrate SonarQube into the CI/CD pipelines for both Git repositories (genai-sdlc-autogent-app and genai-sdlc-tool-app). This will enable automated code quality checks on every commit and pull request.

4. Summary of Requests
Service	Configuration / Name	Purpose & Key Notes
S3	genai-autogen-sdlc-input	Stores user-uploaded requirement files. Needs R/W access from POD-1.
DynamoDB	genai-autogen-sdlc-workflows	Persistent state management for agent workflows. Needs R/W access from both pods.
EKS	genai-sdlc (Cluster Name Suggestion)	Hosts the two main application services.
↳ Pod 1	genai-sdlc-autogent-app	Runs AutoGen/Streamlit UI. Public-facing via Ingress.
↳ Pod 2	genai-sdlc-tool-app	Runs FastAPI tools. Internal access only (ClusterIP).
CloudWatch	Two separate log groups	For isolated logging of the AutoGen app and the Tools service.
SonarQube	New project dashboard	Integrated with both Git repos for CI/CD code quality scanning.
Please let us know if you have any questions or require further details. We are available to discuss the architecture and requirements at your convenience.

