from openai import OpenAI
from Models.AI.llm_base import LLMClient


class OpenAIClient(LLMClient):
    def __init__(self, api_key):
        # openai.api_key = api_key
        self.client = OpenAI(api_key='sk-proj-50E1sywBeRlbkFJBGyd58KmOsywolfzzbPX')

    def run_prompt(self, prompt, **kwargs):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
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
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return self.normalise_response(response.choices[0].message.content)
