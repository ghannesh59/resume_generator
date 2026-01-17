# services/ai_client_service.py
from Models.AI.llm_base import LLMFactory


class AIClientService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIClientService, cls).__new__(cls)
            cls._instance._clients = {}
        return cls._instance

    def get_client(self, client_type, api_key):
        if client_type not in self._clients:
            self._clients[client_type] = LLMFactory.get_client(client_type, api_key)
        return self._clients[client_type]

    def run_prompt(self, prompt, client_type, api_key, **kwargs):
        client = self.get_client(client_type, api_key)
        return client.run_prompt(prompt, **kwargs)


ai_client_service = AIClientService()
