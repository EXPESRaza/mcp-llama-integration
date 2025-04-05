import requests
import json
import logging
from typing import Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelContextClient:
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
        logger.info(f"Initialized ModelContextClient with server URL: {server_url}")
    
    def get_context(self, 
                   query_text: str, 
                   user_id: Optional[str] = None,
                   session_id: Optional[str] = None,
                   additional_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Fetch context information from the Model Context Protocol server.
        """
        request_data = {
            "query_text": query_text,
            "user_id": user_id,
            "session_id": session_id,
            "additional_context": additional_context or {}
        }
        
        logger.info(f"Sending context request for query: {query_text}")
        
        try:
            response = requests.post(
                f"{self.server_url}/context", 
                json=request_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching context: {e}")
            return {"error": str(e)}

class AIAssistant:
    def __init__(self, context_client: ModelContextClient):
        self.context_client = context_client
    
    def generate_response(self, user_query: str) -> str:
        """
        Generate a response to the user query with context enhancement.
        """
        # Get context from the MCP server
        context_data = self.context_client.get_context(user_query)
        
        # In a real application, you would send this context to an LLM
        # For demonstration, we'll just use the context directly
        if "error" in context_data:
            return f"Sorry, I couldn't generate a proper response due to: {context_data['error']}"
        
        context_elements = context_data.get("context_elements", [])
        
        if not context_elements:
            return "I don't have enough information to answer that question."
        
        # Use the context to build a response
        response = f"Based on the available information:\n\n"
        for element in context_elements:
            response += f"- {element['content']}\n"
        
        return response

def main():
    # Create a client connected to our MCP server
    context_client = ModelContextClient()
    
    # Initialize an assistant that uses the context
    assistant = AIAssistant(context_client)
    
    print("AI Assistant with Model Context Protocol")
    print("Type 'exit' to quit")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
            
        response = assistant.generate_response(user_input)
        print(f"\nAssistant: {response}")

if __name__ == "__main__":
    main()