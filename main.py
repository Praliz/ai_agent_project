import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions
from functions.call_function import call_function
def main():

    #loading API KEY
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key == None:
        raise RuntimeError("API KEY not loaded")
    client = genai.Client(api_key = api_key)

    #parsing the input from the user
    parser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")

    #verbose is just a bolean value to handle if i want more or less info.
    parser.add_argument("--verbose",action="store_true", help="enable verbose output")
    args = parser.parse_args()
    #Messege types to keep conversation
    messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    
    for _ in  range(20):

        response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),
        )
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if response.usage_metadata is None:
            raise RuntimeError("API failed, at or before Metadata_level")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:",response.usage_metadata.candidates_token_count)
        function_results = []
        if response.function_calls:
            for func in response.function_calls:
                function_call_result = call_function(func,args.verbose)
                if not function_call_result.parts:
                    raise Exception("empty .parts list")
                if function_call_result.parts[0].function_response == None:
                    raise Exception("Function response object is None")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("actual function reponse is None")
                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(response.text)
            break
        # to make the response more clean i can use this ("Response:\n" +) before my response.text.
    else:
        print(f"Loop exausted without breaking")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
