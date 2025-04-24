import api_scripting as prompts
import subprocess
import json
from pathlib import Path


def promptGeneration():
    prompts.setUpEnviroment()
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

if __name__ == '__main__':
    file1 = "prompts_output.json"
    if not Path(file1).exists():
        promptGeneration()

    print("Done")
