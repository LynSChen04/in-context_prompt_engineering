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

#Problem 1:
def prompt_1():
    code = """public Map < String , Integer > countWordFrequency ( List < String > words ) {
Map < String , Integer > freqMap = new HashMap < >() ;
for ( String word : words ) {
freqMap . put ( word , freqMap . getOrDefault ( word , 0) + 1) ;
}
return freqMap ;
}"""
    zero_shot_prompt = f"Summarize the functionality of this Java method:\n{code}"
    few_shot_prompt = f"This Java method when inputted [\"apple\", \"banana\", \"apple\"] returns {{\"apple\": 2, \"banana\": 1}}\n and when inputted [\"red\", \"orange\", \"yellow\", \"orange\", \"orange\"] returns {{\"red\": 1, \"orange\": 3, \"yellow\": 1}}.\n\nNow, summarize the functionality of this Java method:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 2:
def prompt_2():
    code = """def sum_range ( start , end ) :
total = 0
for i in range ( start , end ) :
total += i
return total"""
    zero_shot_prompt = f"Fix the error in this Python method:\n{code}"
    few_shot_prompt = f"This Python method when inputted start = 1 and end = 5 should return 4 and when inputted start = 0 and end = 8 should return 8.\n\nNow, fix the error in this Python method:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 3:
def prompt_3():
    code="""int * getArray (int size ) {
int arr [ size ]; // Warning : local array
return arr ; // Bug: returning pointer to local variable
}"""
    zero_shot_prompt = f"Classify the bug in this C++ method:\n{code}"
    few_shot_prompt = f"This C++ method when inputted size = 5 should return a pointer to an array of size 5 and when inputted size = 10 should return a pointer to an array of size 10.\n\nNow, classify the bug in this C++ method:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 4:
def prompt_4():
    code = """def is_valid_email ( email ):
# TODO : Complete using regex
pass"""
    zero_shot_prompt = f"Complete the TODO in this Python method using regex to validate basic email addresses:\n{code}"
    few_shot_prompt = f"A valid email would be abcdef@gmail.com and an invalid email would be @dfe.com.\n\nNow, complete the TODO in this Python method using regex to validate basic email addresses:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 5:
def prompt_5():
    code = """from flask import Flask , jsonify
app = Flask ( __name__ )
@app . route (’/ greet / < username >’)
def greet ( username ) :
# TODO : Return a JSON greeting
pass"""
    zero_shot_prompt = f"Complete the TODO to create a '/greet/<username>' endpoint in this Flask app that returns a JSON greeting:\n{code}"
    few_shot_prompt = f"A valid endpoint would be /greet/John and the expected output would be {{\"greeting\": \"Hello, John!\"}}. Another valid endpoint would be /greet/Alicia and the expected output would be {{\"greeting\": \"Hello, Alicia!\"}}.\n\nNow, complete the TODO to create a '/greet/<username>' endpoint in this Flask app that returns a JSON greeting:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 6:
def prompt_6():
    code = """-- TODO : Design schema with appropriate keys and constraints
-- Tables : users (id , name ), books (id , title ), reviews (id , user_id , book_id ,
rating )"""
    zero_shot_prompt = f"Write the schema for a review app with users, books, and reviews: \n{code}"
    few_shot_prompt = f"A user with id 1 and name 'Alice' and a book with id 2 and title 'Python 101' should be able to leave a review with id 3, user_id 1, book_id 2, and rating 5.\n\nNow, write the schema for a review app with users, books, and reviews: \n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 7:
def prompt_7():
    code = """public int getLength ( String s ) {
return s . length () ; // What if s is null ?
}"""
    zero_shot_prompt = f"Identify any null dereference risk in this Java method:\n{code}"
    few_shot_prompt = f"This Java method when inputted s = 'hello' should return 5 and when inputted s = null should throw a NullPointerException.\n\nNow, identify any null dereference risk in this Java method:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 8:
def prompt_8():
    code = """def parse_csv_line ( line ) :
return line . split (’,’) # Incomplete : doesn ’t handle quoted fields"""
    zero_shot_prompt = f"Fix this parser so that it can handle quoted fields:\n{code}"
    few_shot_prompt = f"This parser should be able to handle lines like 'name, age, \"city, state\"' and return ['name', 'age', 'city, state'] and lines like 'name, age, city' and return ['name', 'age', 'city'].\n\nNow, fix this parser so that it can handle quoted fields:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 9:
def prompt_9():
    code = """data class Product ( val id : Int , val name : String , val price : Double )
// TODO : Create GET and POST endpoints using Ktor"""
    zero_shot_prompt = f"Convert this data class to a REST API using Ktor:\n{code}"
    few_shot_prompt = f"A GET request to /products should return a list of products and a POST request to /products should create a new product.\n\nNow, convert this data class to a REST API using Ktor:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 10:
def prompt_10():
    code = """def reverse_words ( sentence ) :
return ’ ’. join ( sentence . split () [:: -1])"""
    zero_shot_prompt = f"Summarize this Python function:\n{code}"
    few_shot_prompt = f"This function should return 'world hello' when inputted 'hello world' and 'Python is great' when inputted 'great is Python'.\n\nNow, summarize this Python function:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 11:
def prompt_11():
    zero_shot_prompt = "Write a Python function that checks if a number is prime."
    few_shot_prompt = "Write a Python function that checks if a number is prime. When inputted 1, it returns False, and when inputted 8 it returns True."
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 12:
def prompt_12():
    code = """def factorial ( n ) :
result = 1
for i in range (1 , n ) :
result *= i
return result"""
    zero_shot_prompt = f"Fix the bug in this Python method when 0 is inputted:\n{code}"
    few_shot_prompt = f"This Python method when inputted 0 should return 1 and when inputted 5 should return 120.\n\nNow, fix the bug in this Python method when 0 is inputted:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 13:
def prompt_13():
    code = """struct Node {
int data ;
struct Node * next ;
};
void deleteNode ( struct Node ** head , int key ) {
// TODO : Implement node deletion
}"""
    zero_shot_prompt = f"Implement the TODO in this C Code to delete a node in a linked list by value:\n{code}"
    few_shot_prompt = f"This C Code should delete the node with value 3 from the linked list 1 -> 2 -> 3 -> 4 and return the linked list 1 -> 2 -> 4.\n\nNow, implement the TODO in this C Code to delete a node in a linked list by value:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 14:
def prompt_14():
    code = """def fibonacci ( n ) :
# TODO : Base cases and recursive call
pass"""
    zero_shot_prompt = f"Implement the TODO in this rescursive Python method to calculate Fibonacci numbers:\n{code}"
    few_shot_prompt = f"Implement the TODO in this rescursive Python method to calculate Fibonacci numbers. When inputted 5, it should return the sum of the method with input 4 and input 3.\n\nNow, implement the TODO in this rescursive Python method to calculate Fibonacci numbers:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 15:
def prompt_15():
    code = """class Person :
def __init__ ( self ) :
# TODO : Add name , age , and optional email
pass"""
    zero_shot_prompt = f"Implement the TODO in this Python class to add name, age, and optional email:\n{code}"
    few_shot_prompt = f"Implement the TODO in this Python class to add name, age, and optional email. A Person object could have the name Isabella with an age of 23 and no email.\n\nNow, implement the TODO in this Python class to add name, age, and optional email:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 16:
def prompt_16():
    code = """public int binarySearch ( int [] arr , int target ) {
int left = 0 , right = arr . length - 1;
while ( left <= right ) {
int mid = ( left + right ) / 2;
// TODO : Compare and adjust bounds
}
return -1;
}"""
    zero_shot_prompt = f"Implement the TODO in this Java method to perform binary search:\n{code}"
    few_shot_prompt = f"This Java method should return the index of the target in the array. When inputted arr = [1, 2, 3, 4, 5] and target = 3, it should return 2.\n\nNow, implement the TODO in this Java method to perform binary search:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 17:
def prompt_17():
    code = """// Supposed to return true if x is even
bool isOdd (int x ) {
return x % 2 == 0; // Logic contradicts function name
}"""
    zero_shot_prompt = f"Identify the inconsistency between the name and logic in this C++ function:\n{code}"
    few_shot_prompt = f"When given inputs of 2, 4, or 6, it returns True. Identify the inconsistency between the name and logic in this C++ function:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 18:
#Prompt Chaining - do manually?

#Problem 19:
def prompt_19():
    code = """// Function that validates an input , calculates square , and returns result
int process (int x ) {
if ( x < 0) return -1;
return x * x ;
}"""
    zero_shot_prompt = f"Decompose the comment that summarizes this C++ function into logical steps:\n{code}"
    few_shot_prompt = f"This C++ function should return -1 when inputted -5 and return 25 when inputted 5. Decompose the comment that summarizes this C++ function into logical steps:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 20:
def prompt_20():
    code = """def calculate_average ( scores ) :
total = 0
# TODO : Complete to return average
pass"""
    zero_shot_prompt = f"Complete the TODO in this Python function:\n{code}"
    few_shot_prompt = f"This Python function should return 85.0 when inputted [80, 90, 85] and return 75.0 when inputted [70, 80, 75].\n\nNow, complete the TODO in this Python function:\n{code}"
    gpt4_response_1 = gpt4_response(zero_shot_prompt)
    gemini_response_1 = gemini_response(zero_shot_prompt)
    gpt4_response_2 = gpt4_response(few_shot_prompt)
    gemini_response_2 = gemini_response(few_shot_prompt)
    return [gpt4_response_1, gemini_response_1, gpt4_response_2, gemini_response_2]

#Problem 21:
#Bonus, probably want to compare zero-shot with prompt chaining

#Problem 22: same as above