import api_scripting as prompts
import json
from pathlib import Path
import nltk
from nltk.translate.meteor_score import meteor_score

def promptGeneration():
    #prompts.setUpEnviroment()
    #load prompt data
    with open("prompts.json", "r") as json_file:
        data = json.load(json_file)
    
    raw_data = {}

    for i in range(1,21):
        #magic value because prompt 18 had to be done differently
        if i == 18:
            continue
        print(i)
        key = f"prompt_{i}"
        responses = prompts.prompt(data[f"prompt_{i}"]["zero_shot_prompt"], data[f"prompt_{i}"]["few_shot_prompt"], data[f"prompt_{i}"]["code"])
        raw_data[key] = {
            "GPT-4o_ZeroShot": responses[0],
            "Gemini_ZeroShot": responses[1],
            "GPT-4o_FewShot": responses[2],
            "Gemini_FewShot": responses[3],
            "language": data[key]["language"]
            }

        
    with open("prompts_output.json", "w") as f:
        json.dump(raw_data, f, indent=4)

def promptEvaluation(jsonFile):
    # Read input from JSON
    with open(jsonFile, 'r') as f:
        data = json.load(f)
    results = []
    for prompt_id, content in data.items():
        entry = {"prompt_id": prompt_id, "language": content.get("language", "unknown")}

        # Define comparisons to run
        pairs_to_compare = [
            ("GPT-4o_ZeroShot", "Gemini_ZeroShot"),
            ("GPT-4o_FewShot", "Gemini_FewShot")
        ]

        for gpt_key, gemini_key in pairs_to_compare:
            if gpt_key in content and gemini_key in content:
                gpt_output = content[gpt_key]
                gemini_output = content[gemini_key]

                # METEOR score expects tokenized input
                references = [gpt_output.split()]
                hypothesis = gemini_output.split()

                score = meteor_score(references, hypothesis)
                score_key = f"meteor_{gpt_key}_vs_{gemini_key}"
                entry[score_key] = round(score, 4)

        results.append(entry)

    # Write results to output JSON
    with open('prompt_eval.json', 'w') as f:
        json.dump(results, f, indent=4)

    print("METEOR comparison scores saved to prompt_eval.json")

if __name__ == '__main__':
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    
    promptOuputfile = "prompts_output.json"
    promptEvalfile = "prompt_eval.json"
    if not Path(promptOuputfile).exists():
        promptGeneration()
    if not Path(promptEvalfile).exists():
        promptEvaluation(promptOuputfile)
