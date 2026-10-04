from ollama import Client
import animation
from prompt_toolkit import print_formatted_text
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import *
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from ghostprint import typewrite
import subprocess
import json
import datetime
import os
ollamaclient = Client(host="http://192.168.2.127:11434")
spinner = animation.Wait('spinner', text='penguin is working')

def execute_bash_command(command: str) -> str:
    """Execute bash commands in a linux shell environnemnt. Give command as full string.
    Args:
        command -> str
        """

    spinner.stop()
    print("Using bash command: ")
    result = subprocess.run(command, cwd="/home/ferdinand", shell=True, capture_output=True, text=True)
    try:
        print_formatted_text(HTML(f'<violet>{str(command)}</violet>'))
        print_formatted_text(HTML(f'<seagreen>{str(result.stdout.strip())}</seagreen>'))
    except:
        print('Printing command output was aborted. Command was executed')

    spinner.start()
    return result.stdout.strip()

def get_memory_entry(keyword: str) -> str:
    """Get memory entries by keyword. The tool will return all the memory entries matching the keyword. Use this tool when searching for a solution for problem you already solved.
    Args:
        keyword -> str
    """
    spinner.stop()
    print("Using get_memory_entry()")
    print(keyword)
    spinner.start()
    matching_entries = []
    with open("memory.json", "r+") as file:
        data = json.load(file)
        for entry in data["memory_entries"]:
            if len(set(keyword.split()).intersection(set(entry["keyword"].split()))) != 0 or len(set(keyword.split()).intersection(set(entry["entry"].split()))) != 0:
                matching_entries.append(entry)
        file.seek(0)
        json.dump(data, file, indent=4)
    return str(matching_entries)

def enter_memory_entry(keyword: str, entry: str) -> str:
    """Enter memory entry with keyword and entry. The tool will enter your memory entry. Use when solved a relevant problem to remember the solution. The keyword is to refind it later, so keep it clear. You may give your entry in the entry argument.
    Args:
        keyword -> str
        entry -> str
    """
    spinner.stop()
    print("Using enter_memory_entry()")
    print(keyword, entry)
    spinner.start()
    entryjson = {"timestamp": datetime.datetime.now(), "keyword": keyword, "entry": entry}
    try:
        with open("memory.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"memory_entries": []}
    data["memory_entries"].append(entryjson)
    with open("memory.json.tmp", "w", encoding="utf-8") as temp_file:
        json.dump(data, temp_file, indent=4, ensure_ascii=False, default=str)
    os.replace("memory.json.tmp", "memory.json")
    print("Successfully updated file safely!")

    return str([keyword, entry])

def bottom_toolbar():
    return HTML('This may not work... <b><style bg="ansired">DO IT YOURSELF</style></b>!')

list_of_tools = ["execute_bash_command", "get_memory_entry", "enter_memory_entry"]
tool_dict = {"execute_bash_command": execute_bash_command, "enter_memory_entry": enter_memory_entry, "get_memory_entry": get_memory_entry}
messages_memory = [{'role': 'system', 'content': "You are a linux ai-assistant called penguin. You can execute bash commands and use your memory to help the user completiting tasks. ALWAYS provide a final answer WITHOUT tool calls to inform he user baout your results."}]
messages = []
custom_style = Style.from_dict({
    '': 'bg:#2c3e50 fg:#ecf0f1',  # Hintergrund dunkelblau, Text weiß
    'prompt': 'bg:#2980b9 fg:#ffffff bold',
})
session = PromptSession(history=FileHistory(".history"), bottom_toolbar=bottom_toolbar, style=custom_style)
def run_agent(message, maximal_num_turns):
    global messages_memory
    global messages
    messages = []
    messages_memory.append({'role': 'user', 'content': message})
    messages = messages_memory
    spinner.start()
    for turn_number in range(maximal_num_turns):
        response = ollamaclient.chat(model="qwen3.5:2b_context", messages=messages, tools=[execute_bash_command, get_memory_entry, enter_memory_entry])

        message_out = response["message"]

        messages.append(message_out)
        messages_memory.append(message_out)
        tool_calls = message_out.get("tool_calls") or []
        if not tool_calls:
            spinner.stop()
            return message_out["content"]
        for call in tool_calls:
            function_name = call["function"]["name"]
            function_args_list = call["function"]["arguments"]
            if function_name not in list_of_tools:
                spinner.stop()
                result = json.dumps({'error': f'Unknown tool or function: {function_name}'})
            else:
                result = tool_dict[function_name](**function_args_list)
            messages.append({'role': 'tool', 'name': function_name, 'content': result})
            messages_memory.append({'role': 'tool', 'name': function_name, 'content': result})

    spinner.stop()

    return "No final answer: running out of turns."

style = Style.from_dict(
    {
        "frame.border": "#893333",
    }
)


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    completer = WordCompleter(['/exit'], ignore_case=True)
    while True:
        user_input = session.prompt(HTML('<ansired>penguin></ansired> '), completer=completer, show_frame=True, style=style, auto_suggest=AutoSuggestFromHistory(), enable_history_search=True)
        if user_input == "/exit":
            print('Exiting penguin.')
            break
        else:
            typewrite(run_agent(user_input, 30), speed=0.01)

if __name__ == "__main__":
    main()