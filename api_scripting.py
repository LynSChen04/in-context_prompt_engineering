import os
from openai import OpenAI
from google import genai

#GITHUB token
with open("token.txt", "r") as file:
    token = file.read().strip()
os.environ["GITHUB_TOKEN"] = token

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"],
)

with open("gemini_key.txt", "r") as file:
    gemini_token = file.read().strip()
os.environ["GEMINI_TOKEN"] = gemini_token

gemini_client = genai.Client(api_key=os.environ["GEMINI_TOKEN"])

#Need to use models ChatGPT (GPT-4), Claude (Anthropic), Gemini (Google), own choice
#API for Claude costs 5 dollars

def gpt4_response(prompt, tokens=1024, temperature=0.7, role="user"):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": role, "content": prompt},
        ],
        max_tokens=tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content

def gemini_response(prompt):
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text
