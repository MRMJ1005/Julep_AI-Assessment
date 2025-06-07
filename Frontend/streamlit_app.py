import streamlit as st
import os
from dotenv import load_dotenv
import sys 
import yaml
import time 
load_dotenv()
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Backend.main import create_client,create_agent,create_task,start_execution,create_task_definition



st.title("A Perfect DAY exists NOW !! - with the help of Julep Agent🤖 ")

st.write("Hi!I am Riya your perfect day planner! I will help you plan your day in a perfect way! So what kind of a day you want to have?")

# Create a dropdown for day plan selection
day_plans = ["❤️ A romantic Day",
    "🏞️ An Adventurous one",
    "🍕 A foodie tour of the city",
    "🗺️ A Tourist plan"
]
selected_plan = st.selectbox(
    "Choose your perfect day plan:",
    day_plans,
    index=None,
    placeholder="Select a day plan..."
)


location_cities=["New Delhi","Chennai","Hyderabad","Vijayawada","Kolkata","Jaipur","Ahmedabad",
                 "Surat","Pune","Bhopal","Indore","Bengaluru","Mysore","Coimbatore","Tirupati","Pondicherry",
                 "Goa","Kashmir","Shimla","Manali","Ladakh","Dharamshala","Amritsar","Amravati","Aurangabad","Bhubaneswar",
                 "Chandigarh","Chhattisgarh","Chhatrapati Shivaji Terminus","Durgapur","Gandhinagar","Gurgaon","Guwahati","Haldwani",
                 "Haryana","Indore","Jaipur","Jodhpur","Kolkata","Lucknow","Mumbai",
                 "Mysore","Nagpur","Nashik","Noida","Pondicherry","Pune","Rajasthan","Surat","Thiruvananthapuram","Udaipur","Ujjain","Varanasi","Vijayawada",
                 "Visakhapatnam","Yamunanagar"]

selected_location=st.selectbox("Select a location",
                               location_cities,
                               index=None
                               ,placeholder="Which city you wanna plan your day in?")

# Wait for the execution to complete
if st.button("Get the result"):
    JULEP_API_KEY = os.getenv("JULEP_API_KEY")
    client = create_client(JULEP_API_KEY)
    agent = create_agent(client)
    if selected_plan == "❤️ A romantic Day":
        yaml_file_path = os.path.join(parent_dir, 'YAML Files\\romantic_day_planning.yaml')
    if selected_plan == "🏞️ An Adventurous one":
        yaml_file_path = os.path.join(parent_dir, 'YAML Files\\adventurous_day_plan.yaml')
    if selected_plan == "🍕 A foodie tour of the city":
        yaml_file_path = os.path.join(parent_dir, 'YAML Files\\foodie_day_planner.yaml')
    if selected_plan == "🗺️ A Tourist plan":
        yaml_file_path = os.path.join(parent_dir, 'YAML Files\\tourist_plan.yaml')
    
    with open(yaml_file_path, 'r') as file:
        task_definition = yaml.safe_load(file)
        


    task = create_task(agent,task_definition,client)

    location=[selected_location]
    execution = start_execution(task,client,location)
    result = client.executions.get(execution.id)



    while (result := client.executions.get(execution.id)).status not in ['succeeded', 'failed']:
        # st.write(result.status)
        time.sleep(1)

    # Print the result
    if result.status == "succeeded":
        st.write(result.output['final_plan'])
    else:
        print(f"Error: {result.error}")