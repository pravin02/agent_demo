# app.py
from pydantic_ai import Tool
from pydantic import BaseModel, Field, model_validator
from typing import List, Dict, Tuple, Literal
import ollama
from ollama import Client
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
# Set up API keys

MODEL_NAME = os.getenv("MODEL_NAME") or ""
OLLAMA_BASE_URL = os.getenv("MODEL_BASE_URL")
client = Client()

# Define the tutoring session state model
class TutorSession(BaseModel):
    topic: str = Field(description="Current topic being discussed")
    difficulty: Literal["beginner", "intermediate", "advanced"] = Field(
        default="beginner",
        description="User's difficulty level"
    )
    progress: int = Field(
        default=0,
        description="Current progress percentage (0-100)",
        gt=-1,
        le="100"
    )
    user_confidence: int = Field(
        default=3,
        description="User's confidence level (1-5)",
        ge=1,
        le=5
    )
    concepts_mastered: List[str] = Field(
        default_factory=list,
        description="List of concepts the user has mastered"
    )
    resources: List[str] = Field(
        default_factory=list,
        description="List of recommended learning resources"
    )
    exercises: List[Dict] = Field(
        default_factory=list,
        description="List of practice exercises"
    )
    
    @model_validator(mode='after')
    def validate_progress(self):
        """Ensure progress is within valid range"""
        if self.progress < 0:
            self.progress = 0
        elif self.progress > 100:
            self.progress = 100
        return self

# Define tools for the AI tutor
class CodeExecutor:
    def execute(self, code: str) -> str:
        try:
            response = ollama.generate(
                model=MODEL_NAME,
                prompt=f"```python\n{code}\n```",
                format="json"
            )
            return response["response"]
        except Exception as e:
            return f"Error executing code: {str(e)}"

class ConceptExplainer:
    def explain(self, topic: str, difficulty: str) -> str:
        explanations = {
            "beginner": "Simple explanation for beginners",
            "intermediate": "Intermediate explanation with examples",
            "advanced": "Advanced explanation with complex concepts"
        }
        return explanations.get(difficulty, "Standard explanation")

class ExerciseGenerator:
    def generate(self, topic: str, difficulty: str) -> List[Dict]:
        exercises = []
        if difficulty == "beginner":
            exercises = [
                {"question": "What is the basic concept?", "type": "multiple_choice", "answer": "A"},
                {"question": "Can you identify examples?", "type": "text", "answer": "Example answer"}
            ]
        elif difficulty == "intermediate":
            exercises = [
                {"question": "How would you apply this concept?", "type": "code", "answer": "Code solution"},
                {"question": "What are the limitations?", "type": "text", "answer": "Limitation explanation"}
            ]
        else:
            exercises = [
                {"question": "How would you optimize this concept?", "type": "code", "answer": "Optimized solution"},
                {"question": "What are the advanced applications?", "type": "text", "answer": "Advanced applications"}
            ]
        return exercises

# Define the AI tutor agent
class AITutor:
    def __init__(self):
        self.tools = [
            Tool(
                name="code_executor",
                function=CodeExecutor().execute,
                description="Execute code snippets and get results"
            ),
            Tool(
                name="concept_explainer",
                function=ConceptExplainer().explain,
                description="Get explanations for concepts at different difficulty levels"
            ),
            Tool(
                name="exercise_generator",
                function=ExerciseGenerator().generate,
                description="Generate practice exercises based on topic and difficulty"
            )
        ]
        
        # Initialize the LLM
        self.llm = self._get_llm()
    
    def _get_llm(self):
        # In a real implementation, this would use the Ollama model
        return lambda prompt: ollama.generate(
            model= MODEL_NAME,
            prompt=prompt,
            format="json"
        )

    def run(self, input_text: str, state: TutorSession) -> Tuple[str, TutorSession]:
        """Run the AI tutor with the given input and update the state"""
        prompt : str = f"""
        You are an AI tutor helping a student learn programming concepts.
        Current state: {state.json()}
        
        User input: {input_text}
        
        Your response should be helpful and educational.
        You can use the following tools if needed:
        - code_executor: To execute code snippets
        - concept_explainer: To get explanations for concepts
        - exercise_generator: To generate practice exercises
        
        Remember to maintain the conversation state and update it appropriately.
        """
        
        # In a real implementation, this would call the LLM and parse the response
        # For this example, we'll simulate a response
        #response = "This is a simulated response from the AI tutor."
        print(f"run: input_text: {prompt}")
        response = client.generate(model=MODEL_NAME, prompt=prompt)["response"]  
        
        
        # Update the state based on the response
        new_state = state.copy()
        new_state.progress += 10  # Simulate progress increase
        
        return response, new_state

# Main tutoring interface
def main():
    # Initialize session state
    if 'tutor' not in st.session_state:
        st.session_state.tutor = AITutor()
    
    if 'session_state' not in st.session_state:
        st.session_state.session_state = TutorSession(
            topic="Human Anatomy",
            difficulty="beginner",
            progress=1,
            user_confidence=3,
            concepts_mastered=[],
            resources=[],
            exercises=[]
        )
    
    # # Update session state with current state
    # st.session_state.session_state = st.session_state.tutor.run(
    #     input_text="What is science?",
    #     state=st.session_state.session_state
    # )[1]  # Get the updated state
    
    # Sidebar with user controls
    with st.sidebar:
        st.title("Pydantic AI Tutor")
        
        # Topic selection
        topic = st.text_input("Enter a topic:", value=st.session_state.session_state.topic or "")
        if topic:
            st.session_state.session_state.topic = topic
        
        # Difficulty selection
        difficulty = st.selectbox(
            "Select difficulty level:",
            options=["beginner", "intermediate", "advanced"],
            index=["beginner", "intermediate", "advanced"].index(st.session_state.session_state.difficulty)
        )
        #st.session_state.session_state.difficulty = difficulty
        
        # Confidence slider
        confidence = st.slider(
            "Your confidence level:",
            min_value=1,
            max_value=5,
            value=st.session_state.session_state.user_confidence
        )
        st.session_state.session_state.user_confidence = confidence
        
        # Submit button
        if st.button("Submit"):
            response, new_state = st.session_state.tutor.run(
                input_text=topic,
                state=st.session_state.session_state
            )
            st.session_state.session_state = new_state
            st.success("Response generated!")
        
        # Reset button
        if st.button("Reset"):
            st.session_state.session_state = TutorSession(
                topic="Welcome to Pydantic AI Tutor",
                difficulty="beginner",
                progress=0,
                user_confidence=3,
                concepts_mastered=[],
                resources=[],
                exercises=[]
            )
    
    # Main chat interface
    st.header(f"Learning: {st.session_state.session_state.topic}")
    
    # Display progress
    st.progress(st.session_state.session_state.progress)
    
    # Display current state
    st.json({
        "Difficulty": st.session_state.session_state.difficulty,
        "Confidence": st.session_state.session_state.user_confidence,
        "Progress": st.session_state.session_state.progress,
        "Mastered concepts": st.session_state.session_state.concepts_mastered
    })
    
    # User input
    user_input = st.text_area("Ask a question or request help:", 
                           value=st.session_state.session_state.topic or "")
    
    if st.button("Send"):
        if user_input:
            response, new_state = st.session_state.tutor.run(
                input_text=user_input,
                state=st.session_state.session_state
            )
            st.session_state.session_state = new_state
            st.write("AI Tutor:", response)

# Run the app
if __name__ == "__main__":
    main()
