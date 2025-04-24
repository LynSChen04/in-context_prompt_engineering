import api_scripting as prompts
import json
import sys
from pathlib import Path
import nltk
from nltk.translate.meteor_score import meteor_score
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

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

def promptMeteorEvaluation(jsonFile):
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

def promptBleuEvaluation(candidate_strs, reference_strs, lang="python"):

    # Tokenize the candidate and reference strings
    candidate_tokens = candidate_strs.split()
    reference_tokens = [reference_strs.split()]  # BLEU expects a list of reference sentences

    # Calculate BLEU score
    smoothing_function = SmoothingFunction().method1
    bleu_score = sentence_bleu(reference_tokens, candidate_tokens, smoothing_function=smoothing_function)

    print(f"BLEU score: {bleu_score}")
    return bleu_score

if __name__ == '__main__':
    
    promptOutputfile = "prompts_output.json"
    promptEvalfile = "prompt_eval.json"
    if not Path(promptOutputfile).exists():
        promptGeneration()

    match(sys.argv[1]):
        case 'M':
            nltk.download('wordnet')
            nltk.download('omw-1.4')
            if not Path(promptEvalfile).exists():
                promptMeteorEvaluation("complete_outputs.json")
        case 'B':
            #method to method
            # Load the prompts_output.json file
            with open("complete_outputs.json", "r") as f:
                data = json.load(f)

            # Separate data into different JSON files
            zero_shot_data = {}
            few_shot_data = {}
            gpt_data = {}
            gemini_data = {}

            for key, value in data.items():
                zero_shot_data[key] = {
                    "GPT-4o_ZeroShot": value["GPT-4o_ZeroShot"],
                    "Gemini_ZeroShot": value["Gemini_ZeroShot"],
                    "language": value["language"]
                }
                few_shot_data[key] = {
                    "GPT-4o_FewShot": value["GPT-4o_FewShot"],
                    "Gemini_FewShot": value["Gemini_FewShot"],
                    "language": value["language"]
                }
                gpt_data[key] = {
                    "GPT-4o_ZeroShot": value["GPT-4o_ZeroShot"],
                    "GPT-4o_FewShot": value["GPT-4o_FewShot"],
                    "language": value["language"]
                }
                gemini_data[key] = {
                    "Gemini_ZeroShot": value["Gemini_ZeroShot"],
                    "Gemini_FewShot": value["Gemini_FewShot"],
                    "language": value["language"]
                }

                # Extract and store only code blocks
                for field in ["GPT-4o_ZeroShot", "Gemini_ZeroShot", "GPT-4o_FewShot", "Gemini_FewShot"]:
                    if field in value:
                        code_block = value[field]
                        if code_block.startswith("```") and code_block.endswith("```"):
                            lang_start = code_block.find("{") + 1
                            lang_end = code_block.find("}")
                            language = code_block[lang_start:lang_end] if lang_start > 0 and lang_end > lang_start else "unknown"
                            code_content = code_block[lang_end + 1:-3].strip()
                            value[field] = {"language": language, "code": code_content}

            # Write the separated data to JSON files
            with open("zero_shot_data.json", "w") as f:
                json.dump(zero_shot_data, f, indent=4)

            with open("few_shot_data.json", "w") as f:
                json.dump(few_shot_data, f, indent=4)

            with open("gpt_data.json", "w") as f:
                json.dump(gpt_data, f, indent=4)

            with open("gemini_data.json", "w") as f:
                json.dump(gemini_data, f, indent=4)
            # Convert dict values to strings for evaluation
            zero_shot_str = json.dumps(zero_shot_data, indent=4)
            few_shot_str = json.dumps(few_shot_data, indent=4)

            #promptEvaluation(zero_shot_str, few_shot_str)
            # promptEvaluation(gpt_data, gemini_data, "python")
            # Initialize a dictionary to store BLEU scores
            bleu_scores = {}

            # Iterate through all prompts and calculate BLEU scores
            for key, value in data.items():
                entry = {"prompt_id": key, "language": value["language"]}
                print(f"Processing {key}...")

                # Zero-shot vs Few-shot comparison
                if "GPT-4o_ZeroShot" in value and "GPT-4o_FewShot" in value:
                    gpt_zero_shot = value["GPT-4o_ZeroShot"]["code"] if isinstance(value["GPT-4o_ZeroShot"], dict) else value["GPT-4o_ZeroShot"]
                    gpt_few_shot = value["GPT-4o_FewShot"]["code"] if isinstance(value["GPT-4o_FewShot"], dict) else value["GPT-4o_FewShot"]
                    bleu_score = promptBleuEvaluation(gpt_zero_shot, gpt_few_shot, lang=value["language"])
                    entry["BLEU_GPT_ZeroShot_vs_FewShot"] = round(bleu_score, 4)

                if "Gemini_ZeroShot" in value and "Gemini_FewShot" in value:
                    gemini_zero_shot = value["Gemini_ZeroShot"]["code"] if isinstance(value["Gemini_ZeroShot"], dict) else value["Gemini_ZeroShot"]
                    gemini_few_shot = value["Gemini_FewShot"]["code"] if isinstance(value["Gemini_FewShot"], dict) else value["Gemini_FewShot"]
                    bleu_score = promptBleuEvaluation(gemini_zero_shot, gemini_few_shot, lang=value["language"])
                    entry["BLEU_Gemini_ZeroShot_vs_FewShot"] = round(bleu_score, 4)
                # GPT vs Gemini comparison
                if "GPT-4o_ZeroShot" in value and "Gemini_ZeroShot" in value:
                    gpt_zero_shot = value["GPT-4o_ZeroShot"]["code"] if isinstance(value["GPT-4o_ZeroShot"], dict) else value["GPT-4o_ZeroShot"]
                    gemini_zero_shot = value["Gemini_ZeroShot"]["code"] if isinstance(value["Gemini_ZeroShot"], dict) else value["Gemini_ZeroShot"]
                    bleu_score = promptBleuEvaluation(gpt_zero_shot, gemini_zero_shot, lang=value["language"])
                    entry["BLEU_ZeroShot_GPT_vs_Gemini"] = round(bleu_score, 4)

                if "GPT-4o_FewShot" in value and "Gemini_FewShot" in value:
                    gpt_few_shot = value["GPT-4o_FewShot"]["code"] if isinstance(value["GPT-4o_FewShot"], dict) else value["GPT-4o_FewShot"]
                    gemini_few_shot = value["Gemini_FewShot"]["code"] if isinstance(value["Gemini_FewShot"], dict) else value["Gemini_FewShot"]
                    bleu_score = promptBleuEvaluation(gpt_few_shot, gemini_few_shot, lang=value["language"])
                    entry["BLEU_FewShot_GPT_vs_Gemini"] = round(bleu_score, 4)

                bleu_scores[key] = entry

            # Save BLEU scores to a JSON file
            with open("BLEU_evaluation.json", "w") as f:
                json.dump(bleu_scores, f, indent=4)

            print("BLEU scores saved to BLEU_evaluation.json")