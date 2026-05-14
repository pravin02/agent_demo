from base_agent import BaseAgent
import json


class ExtractionAgent(BaseAgent):
    """Agent responsible for the extracting useful information from the user's prompt"""

    def extract_details(self, user_input: str):
        system_prompt = (
            "You are a travel data extraction expert, extract travel information and the only valid JSON nothing else."
            "If information is missing, make reasonable estimates based on the context."
        )

        user_prompt = f"""
            Extract the following information from the user's travel request:
            User_Request: "{user_input}"
            Return a JSON object with:
            {{
                "destination": "City, Country",
                "duration": "Number of days (estimate if not specified default 7)",
                "budget": "estimate budget in INR (estimate if not specified 30,000)",
                "travel_type": "Solo/Adventure/Cultural/Relaxation/Family/Romantic/Business",
                "no_of_travelers": "number of people travelling (default 2)"
            }}
            return only the JSON object, something fails return error in below format,

            {{
                "status": "False",
                "error": "Failure message could be validation"
            }}

            """
        
        try:
            response = self.invoke(system_prompt, user_prompt)
            print(f"Response was: {response}")
            return response
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            

        return {
            "destination": "unknown",
            "duration": 7,
            "budget": 30000,
            "travel_type": "General",
            "no_of_travellers": 2,
        }
