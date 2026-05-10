from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Replace with your actual Azure AI Foundry resource and project names
resource_name = "<your-resource-name>"
project_name = "<your-project-name>"

# Construct the endpoint URL
endpoint = f"https://{resource_name}.services.ai.azure.com/api/projects/{project_name}"

# Create the credential using DefaultAzureCredential
credential = DefaultAzureCredential()

try:
    # Create the AIProjectClient to authenticate
    project_client = AIProjectClient(endpoint=endpoint, credential=credential)
    
    # Verify authentication by getting project information
    project = project_client.projects.get()
    
    print("Successfully authenticated to Azure AI Foundry!")
    print(f"Project Name: {project.name}")
    print(f"Project Description: {project.description}")

except Exception as e:
    print(f"Authentication failed: {e}")
    print("Make sure you have run 'az login' and have the necessary permissions.")