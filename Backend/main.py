from julep import Client
import time
import yaml
from dotenv import load_dotenv
import os
load_dotenv()

JULEP_API_KEY = os.getenv("JULEP_API_KEY")

def create_client(JULEP_API_KEY):
    client = Client(api_key=JULEP_API_KEY,environment='production')
    return client

def create_agent(client):

    agent = client.agents.create(
      name="Julep Trip Planning Agent",
      about="A Julep agent that can generate a detailed itinerary for visiting tourist attractions in some locations, considering the current weather conditions.",
    )

    return agent

# Load the task definition

def create_task_definition(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
      task_definition = yaml.safe_load(file)
    return task_definition
   


def create_task(agent,task_definition,client):
    task = client.tasks.create(
        agent_id=agent.id,
        **task_definition
    )
    return task


def start_execution(task,client,location):
# Create the execution
  execution = client.executions.create(
      task_id=task.id,
      input={
        "locations": location
      }
  )
  return execution


