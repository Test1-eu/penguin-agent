# penguin
Simple, minimalist AI-Agent for Linux that runs on almost every device

## LLM
Penguin uses (at the moment) the qwen3.5:2b model with Ollama as inference. The model can run at a good conversation speed on most modern laptops and a bit slower on older machines, the minimum I reached with an eight years old Lenovo Thinkpad(i5, 7th generation?) was 7 t/s. I recommend using an 32k context window, which is enough for most applications you will run with penguin.

## Installing & Quick Start
### One-line install command using pipx:
[pipx](https://github.com/pypa/pipx) is a modern PyPi Installer for CLI applications - like apt but for python. Use it to install the  ```penguin-agent-package``` with a systemwide command  ```penguin``` :

```
sudo pipx install --global --program-name penguin penguin-agent-package
```

Then type ```penguin``` in your terminal
### Standard install using pip:
[pip](https://github.com/pypa/pip) is the standard PyPi Installer. Install  ```penguin-agent-package``` using pip in a virtual environment:

```
pip install penguin-agent-package
```

>[!WARNING]
>This will not install the systemwide  ```penguin``` command. You need to add it manually to PATH.

## Features
Penguin is a very, very simple tool:
+ Uses an Ollama backend(see [LLM](#llm))
+ Three basic tools in the agent-loop:
    * execute_bash_command
    * get_memory_entry
    * enter_memory_entry
+ Executes bash commands always at ```~```
+ Uses [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) to manage sessions with history and suggestions
+ Uses memory.json file for managing the agent memory

## Run it

