# Import necessary modules
from langchain_core.prompts import ChatPromptTemplate  # type: ignore
from langchain_community.llms import Ollama  # type: ignore
import streamlit as st  # type: ignore
import asyncio



# Define a prompt template for the fitness plan generator
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a knowledgeable and empathetic fitness coach, skilled in creating personalized fitness plans. Your specialty is tailoring workout routines and nutrition advice to meet the specific goals, needs, and preferences of each individual. Each plan you create is well-rounded, achievable, and designed to motivate and guide individuals towards their fitness objectives."),
        ("user", "Fitness Goal: {goal}\nCurrent Fitness Level: {fitness_level}\nAvailable Equipment: {equipment}\nPreferred Workout Types: {workout_types}\nAny Specific Constraints or Preferences: {constraints}\n\nGenerate a detailed and personalized fitness plan, including a workout routine and dietary suggestions, based on the provided information.")
    ]
)

# Set up the Streamlit framework
st.title('AI-Powered Fitness Plan Generator with LLAMA')  # Set the title of the Streamlit app

# Create text input fields in the Streamlit app
goal = st.text_input("Fitness Goal (e.g., weight loss, muscle gain):")
fitness_level = st.text_input("Current Fitness Level (e.g., beginner, intermediate, advanced):")
equipment = st.text_input("Available Equipment (e.g., dumbbells, treadmill):")
workout_types = st.text_input("Preferred Workout Types (e.g., cardio, strength training):")
constraints = st.text_input("Any Specific Constraints or Preferences (e.g., time limitations, dietary restrictions):")

# Initialize the Ollama model (ensure it's loaded only once)
@st.cache_resource
def load_model():
    return Ollama(model="llama3")

llm = load_model()

# Create an asynchronous function to generate the fitness plan
async def generate_fitness_plan(goal, fitness_level, equipment, workout_types, constraints):
    # Prepare the input for the prompt
    input_text = {
        "goal": goal or "General fitness",
        "fitness_level": fitness_level or "beginner",
        "equipment": equipment or "none",
        "workout_types": workout_types or "general",
        "constraints": constraints or "none"
    }
    
    # Generate the fitness plan using the chain
    chain = prompt | llm
    return chain.invoke(input_text)

# Display the submit button
if st.button("Generate Fitness Plan"):
    # Check if the required fields are filled
    if goal and fitness_level:
        with st.spinner('Generating fitness plan...'):
            response = asyncio.run(generate_fitness_plan(goal, fitness_level, equipment, workout_types, constraints))
        st.write(response)
    else:
        st.write("Please enter at least the fitness goal and current fitness level.")
