import openai
import time

class DebateAgent:
    def __init__(self, name, api_key, model_name, role):
        self.name = name
        self.api_key = api_key
        self.model_name = model_name
        self.role = role

    def think(self, user_query, context):
        openai.api_key = self.api_key
        openai.api_base = "https://openrouter.ai/api/v1"

        prompt = f"""You are {self.role}, debating on the user's query:
        "{user_query}"

        Your goal is to provide a chain-of-thought reasoning before concluding your position.
        Consider all nuances and reason step-by-step. Then write your final opinion.

        Context from previous exchanges:
        {context}

        Begin your reasoning now:"""

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']

class MetaAI:
    def __init__(self, api_key, model_name="mistralai/mistral-7b-instruct"):
        self.api_key = api_key
        self.model_name = model_name

    def synthesize(self, user_query, agent_outputs):
        openai.api_key = self.api_key
        openai.api_base = "https://openrouter.ai/api/v1"

        combined_output = "\n\n".join(
            [f"{agent}: {output}" for agent, output in agent_outputs.items()]
        )

        prompt = f"""You are a neutral Meta-AI. Two agents have debated the following question:

        "{user_query}"

        Their arguments are:
        {combined_output}

        Analyze both responses. Decide whether the agents agree or not.
        If they agree, summarize their shared answer. If they disagree, explain the disagreement and decide who is more persuasive with justification.

        Provide your final decision and reasoning."""

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response['choices'][0]['message']['content']
