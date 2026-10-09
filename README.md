# penguin
Simple, minimalist AI-Agent for Linux that runs on almost every device

## Why?
Ever used an AI Agent before? If you did so, you might have noticed some kind of problems with this kind of technology: too much at the wrong place. Especially when you use an agent like claude code or Pi with a local model, the sheer mass of the structure that's perfect for coding work makes the framework unusable for simple tasks like updating a library or so. So here is penguin, the simplest AI Agent ever made. Penguin will definitely not build your next project, but it will create the folder structure for you and clean up after, when you see what I mean. At the end, penguin is also a Linux specific software, like a stupid Siri for all the old Linux computers out there.

## LLM
Penguin uses (at the moment) the qwen3.5:2b model with Ollama as inference. The model can run at a good conversation speed on most modern laptops and a bit slower on older machines, the minimum I reached with an eight years old Lenovo Thinkpad(i5, 7th generation?) was 7 t/s. I recommend using an 32k context window, which is enough for most applications you will run with penguin.

## Installing

