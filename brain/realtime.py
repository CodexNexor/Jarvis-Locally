import requests
import json
import os
from googlesearch import search
from dotenv import load_dotenv

load_dotenv()

def get_web_info(query, max_results=20, prints=False) -> str:
    results = list(search(query, num_results=max_results, advanced=True))
    response = []
    for link in results:
        response.append({"link": link.url, "title": link.title, "description": link.description})
    return json.dumps(response)

def generate(user_prompt, system_prompt="Be Short and Concise", prints=False) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    function_descriptions = [{
        "type": "function",
        "function": {
            "name": "get_web_info",
            "description": "Gets real-time information about the query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search on the web"
                    }
                },
                "required": ["query"]
            }
        }
    }]

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    data = {
        "model": "meta-llama/llama-3-70b-instruct",
        "messages": messages,
        "tools": function_descriptions,
        "max_tokens": 1024
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        response_message = result["choices"][0]["message"]

        if prints:
            print("Initial Response:", response_message)

        tool_calls = response_message.get("tool_calls", [])

        if tool_calls:
            available_functions = {"get_web_info": get_web_info}
            messages.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call["function"]["name"]
                function_args = json.loads(tool_call["function"]["arguments"])
                function_response = available_functions[function_name](**function_args)

                messages.append({
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })

            data["messages"] = messages
            second_response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
            second_response.raise_for_status()
            result2 = second_response.json()
            return result2["choices"][0]["message"]["content"]

        else:
            return response_message["content"]

    except requests.exceptions.RequestException as e:
        print("[ERROR] Exception during classification:", e)
        if e.response is not None:
            print("[DEBUG] Response Text:", e.response.text)
        return "An error occurred."

if __name__ == "__main__":
    response = generate(
        user_prompt="tell me name of mission for pakistan",
        prints=True,
        system_prompt="Be Short and Concise"
    )
    
    print("\nFinal Response:\n", response)
