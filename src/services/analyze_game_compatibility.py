from dataclasses import dataclass
from typing import List, Optional
from src.shared.providers import LLMProvider

@dataclass
class CompatibilityAnalysis:
    can_run: bool
    performance_level: str  # 'Baixo', 'Médio', 'Alto'
    expected_issues: List[str]
    recommended_settings: Optional[str] = None
    upgrade_suggestions: Optional[List[str]] = None

def analyze_game_compatibility(system_specs, game_requirements):
    """
    Analisa a compatibilidade entre as especificações do sistema e os requisitos do jogo.
    
    Args:
        system_specs: Objeto contendo as especificações do sistema
        game_requirements: Objeto contendo os requisitos do jogo
        
    Returns:
        CompatibilityAnalysis: Resultado da análise
    """
    llm_provider = LLMProvider()
    
    # Constrói o prompt para a análise
    system_prompt = """
    Você é um especialista em análise de compatibilidade de hardware para jogos.
    Sua tarefa é analisar as especificações de um computador e os requisitos de um jogo,
    e fornecer uma análise detalhada da compatibilidade e performance esperada.
    
    IMPORTANTE: Você deve responder APENAS com um objeto JSON válido, sem nenhum texto adicional antes ou depois.
    O JSON deve seguir exatamente este formato:
    {
        "can_run": true/false,                        # obrigatório, booleano
        "performance_level": "Baixo"/"Médio"/"Alto",  # obrigatório, string
        "expected_issues": [                          # obrigatório, array
            "problema 1",
            "problema 2"
        ],
        "recommended_settings": "string com configurações", # opcional
        "upgrade_suggestions": [                           # opcional
            "sugestão 1",
            "sugestão 2"
        ]
    }
    """
    
    # Prepara as informações do sistema em um formato claro
    system_info = f"""
    Especificações do Sistema:
    CPU: {system_specs.cpu_name} ({system_specs.cpu_cores} cores, {system_specs.cpu_threads} threads)
    GPU: {system_specs.gpu_name} ({system_specs.gpu_memory_total}GB VRAM)
    RAM: {system_specs.ram_total}GB {system_specs.ram_type or ''} {system_specs.ram_speed or ''}MHz
    Sistema: {system_specs.os_name} {system_specs.os_version}
    DirectX: {system_specs.directx_version or 'Não especificado'}
    """
    
    # Prepara os requisitos do jogo
    game_info = "Requisitos do Jogo:\n"
    if game_requirements.minimum:
        game_info += "\nMínimos:\n"
        for key, value in game_requirements.minimum.items():
            if key != "status":
                game_info += f"{key}: {value}\n"
    
    if game_requirements.recommended:
        game_info += "\nRecomendados:\n"
        for key, value in game_requirements.recommended.items():
            if key != "status":
                game_info += f"{key}: {value}\n"
    
    # Monta o prompt completo
    analysis_prompt = f"""
    Por favor, analise a compatibilidade entre o sistema e o jogo com os seguintes detalhes:

    {system_info}

    {game_info}

    Forneça uma análise detalhada considerando:
    1. Se o jogo pode rodar no sistema
    2. Qual nível de performance pode ser esperado
    3. Possíveis problemas ou limitações
    4. Configurações recomendadas para melhor experiência
    5. Sugestões de upgrade se necessário
    
    Retorne a análise no formato JSON especificado.
    """
    
    try:
        # Obtém a análise do LLM
        result = llm_provider.generate_response(
            prompt=analysis_prompt,
            system_prompt=system_prompt,
            temperature=0.2  # Reduzindo a temperatura para respostas mais consistentes
        )
        
        # Remove possíveis caracteres especiais ou texto antes/depois do JSON
        import re
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if not json_match:
            raise ValueError("Resposta não contém JSON válido")
            
        json_str = json_match.group()
        
        # Converte o resultado JSON em um objeto CompatibilityAnalysis
        import json
        analysis_dict = json.loads(json_str)
        
        return CompatibilityAnalysis(
            can_run=analysis_dict['can_run'],
            performance_level=analysis_dict['performance_level'],
            expected_issues=analysis_dict['expected_issues'],
            recommended_settings=analysis_dict.get('recommended_settings'),
            upgrade_suggestions=analysis_dict.get('upgrade_suggestions')
        )
        
    except Exception as e:
        raise Exception(f"Erro ao analisar compatibilidade do jogo: {str(e)}")
