import os
LLM_TYPE = os.getenv("LLM_TYPE") or "Ollama_mistral:latest"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL") or "http://knight.simpragma.com:11081"
openai_api_key = os.getenv("OPENAI_API_KEY") or "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"

if os.getenv('top_p'):
    top_p = float(os.getenv('top_p'))
else:
    top_p = 0.7

if os.getenv('temparature'):
    temparature = float(os.getenv('temparature'))
else:
    temparature = 0


if os.getenv('top_k'):
    top_k = int(os.getenv('top_k'))
else:
    top_k = 20

LLM_CONFIG = {"temparature":temparature, "top_p":top_p, "top_k":top_k}