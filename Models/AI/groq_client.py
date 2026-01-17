# groq_client.py
from groq import Groq

from Models.AI.llm_base import LLMClient


class GroqClient(LLMClient):
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def run_prompt(self, prompt, **kwargs):
        completion = self.client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )

        return self.normalise_response(completion.choices[0].message.content)
