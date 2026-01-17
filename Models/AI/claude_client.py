# claude_client.py
from anthropic import Anthropic

from Models.AI.llm_base import LLMClient


class ClaudeClient(LLMClient):
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)

    def run_prompt(self, prompt, **kwargs):
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )

        input_tokens = message.usage.input_tokens
        output_tokens = message.usage.output_tokens

        input_cost = (input_tokens / 1_000_000) * 3.00  
        output_cost = (output_tokens / 1_000_000) * 15.00

        total_cost = input_cost + output_cost

        return self.normalise_response(message.content[0].text), total_cost, input_tokens, output_tokens
