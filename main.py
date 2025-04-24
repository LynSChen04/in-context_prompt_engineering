import api_scripting as prompts
import promptEval

prompts.setUpEnviroment()

example = prompts.prompt_1()


print("zero1")
print(example[0])
print("zero2")
print(example[1])
print("few1")
print(example[2])
print("few2")
print(example[3])