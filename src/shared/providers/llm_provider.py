import os
import requests
from dotenv import load_dotenv

load_dotenv()

class LLMProvider:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.model = os.getenv('OPENROUTER_MODEL')
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY não encontrada no .env")
        if not self.model:
            raise ValueError("OPENROUTER_MODEL não encontrado no .env")

    def generate_response(self, prompt, system_prompt=None, temperature=0.7):
        """
        Gera uma resposta usando o modelo LLM configurado via OpenRouter.
        
        Args:
            prompt (str): O prompt principal para o modelo
            system_prompt (str, optional): Prompt de sistema que define o comportamento do modelo
            temperature (float, default=0.7): Controla a aleatoriedade das respostas
            
        Returns:
            str: A resposta gerada pelo modelo
            
        Raises:
            Exception: Se houver erro na chamada da API
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/pedro/game-spec-analyzer-ia",
            "X-Title": "Game Spec Analyzer IA"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro ao chamar OpenRouter API: {str(e)}"
            if response := getattr(e, 'response', None):
                error_msg += f"\nResponse: {response.text}"
            raise Exception(error_msg)
