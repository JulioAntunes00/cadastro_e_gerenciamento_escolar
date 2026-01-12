import google.generativeai as genai
import config

genai.configure(api_key=config.GEMINI_API_KEY)

print("=== Modelos disponíveis para sua Chave ===")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Erro ao listar: {e}")