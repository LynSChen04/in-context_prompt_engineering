import os
from openai import AzureOpenAI
from google import genai
from dotenv import load_dotenv


def setUpEnviroment():
    load_dotenv()
    global client, gemini_client
    
    client = AzureOpenAI(
        api_version=os.environ["AZURE_API"],
        azure_endpoint=os.environ["AZURE_ENDPOINT"],
        api_key=os.environ["AZURE_TOKEN"]
    )
    gemini_client = genai.Client(api_key=os.environ["GEMINI_TOKEN"])

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

#Prompting types used: zero-shot and few-shot prompting

def prompt(zero_shot_prompt, few_shot_prompt, code=""):
    gpt4_response_1 = gpt4_response(zero_shot_prompt+code)
    gemini_response_1 = gemini_response(zero_shot_prompt+code)
    gpt4_response_2 = gpt4_response(few_shot_prompt+code)
    gemini_response_2 = gemini_response(few_shot_prompt+code)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

