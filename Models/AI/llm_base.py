# Models/llm_base.py
import json
from abc import ABC, abstractmethod

class LLMClient(ABC):
    @abstractmethod
    def run_prompt(self, prompt, **kwargs):
        pass
    def normalise_response(self, response):
        
        try:
            response = response.replace('```','').replace('json','')
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(f"Raw response: {response}")
            raise

class LLMFactory:
    @staticmethod
    def get_client(client_type, api_key):
        if client_type == "groq":
            from Models.AI.groq_client import GroqClient
            return GroqClient(api_key)
        elif client_type == "openai":
            from Models.AI.openai_client import OpenAIClient
            return OpenAIClient(api_key)
        elif client_type == "claude":
            from Models.AI.claude_client import ClaudeClient
            return ClaudeClient(api_key)
        else:
            raise ValueError(f"Unsupported LLM client type: {client_type}")