from dataclasses import dataclass
from typing import List, Optional
from src.shared.providers import LLMProvider

@dataclass
class PerformanceEstimates:
    baixa: str
    media: str
    alta: str
    ultra: str

@dataclass
class PerformanceDetails:
    cpu_analysis: str
    gpu_analysis: str
    ram_analysis: str
    storage_impact: str
    estimated_fps: dict[str, PerformanceEstimates]

@dataclass
class CompatibilityAnalysis:
    can_run: bool
    performance_level: str  # 'Baixo', 'Médio', 'Alto'
    expected_issues: List[str]
    recommended_settings: str
    upgrade_suggestions: List[str]
    performance_details: PerformanceDetails

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
    Você é um especialista altamente qualificado em análise de compatibilidade de hardware para jogos.
    Sua tarefa é realizar uma análise técnica extremamente detalhada e precisa comparando as especificações 
    do computador com os requisitos do jogo.
    
    REGRAS CRÍTICAS:
    1. Todas as respostas DEVEM ser em português
    2. Seja extremamente técnico e preciso nas análises
    3. Compare SEMPRE com os requisitos mínimos E recomendados
    4. IMPORTANTE: Hardware mais recente é geralmente mais potente que hardware antigo
       - Um i7 ou i5 de 13ª geração é MUITO mais potente que um i5 de 2ª ou 6ª geração
       - Uma RTX 4050, mesmo laptop, é mais potente que uma GTX 960 ou 1060
       - Considere a arquitetura e eficiência dos componentes modernos
    5. Analise a compatibilidade real do hardware:
       - Compare gerações de processadores (ex: 13ª gen > 6ª gen)
       - Compare arquiteturas de GPU (ex: RTX 4000 > GTX 1000)
       - Considere memória e velocidade da RAM
       - Avalie recursos especiais (DLSS, Ray Tracing, etc)
    6. Forneça estimativas de FPS realistas para o hardware
    7. Sugira upgrades APENAS se o componente estiver realmente abaixo dos requisitos
    8. Considere o impacto real da velocidade da RAM e tipo de armazenamento
    9. Retorne APENAS o JSON, sem texto adicional
    
    O JSON deve seguir exatamente este formato (mantenha as chaves em inglês, mas TODO o conteúdo em português):
    {
        "can_run": true/false,                # se o jogo pode rodar no sistema
        "performance_level": "Baixo"/"Médio"/"Alto",  # nível geral de performance esperado
        "expected_issues": [                  # lista detalhada de possíveis problemas
            "Descrição técnica detalhada do problema 1",
            "Descrição técnica detalhada do problema 2"
        ],
        "recommended_settings": "Configurações detalhadas incluindo: resolução, taxa de quadros alvo, qualidade de texturas, sombras, iluminação, DLSS/FSR (se disponível), etc.",
        "upgrade_suggestions": [              # sugestões específicas e justificadas de upgrade (apenas se necessário)
            "Sugestão detalhada de upgrade 1 com justificativa técnica e ganho esperado",
            "Sugestão detalhada de upgrade 2 com justificativa técnica e ganho esperado"
        ],
        "performance_details": {              # análise profunda por componente
            "cpu_analysis": "Análise detalhada do processador comparando gerações, arquiteturas e capacidades reais",
            "gpu_analysis": "Análise detalhada da GPU incluindo geração, arquitetura, VRAM e recursos especiais",
            "ram_analysis": "Análise da RAM considerando quantidade, velocidade e impacto na performance",
            "storage_impact": "Análise do impacto do tipo de armazenamento nos tempos de carga",
            "estimated_fps": {
                "1080p": {
                    "baixa": "FPS esperado em configurações baixas",
                    "media": "FPS esperado em configurações médias",
                    "alta": "FPS esperado em configurações altas",
                    "ultra": "FPS esperado em configurações ultra"
                }
            }
        }
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
    Realize uma análise técnica extremamente detalhada da compatibilidade entre o sistema e o jogo.
    LEMBRE-SE: Hardware mais recente é geralmente mais potente que hardware antigo, mesmo que tenha
    especificações aparentemente menores. Compare as gerações e arquiteturas dos componentes.

    {system_info}

    {game_info}

    Considere cuidadosamente:
    1. Comparação precisa das gerações e arquiteturas dos componentes
    2. Análise detalhada da performance esperada em cada resolução
    3. Identificação de possíveis limitações (apenas se realmente existirem)
    4. Recomendações específicas de configurações para melhor experiência
    5. Sugestões de upgrade (APENAS se o hardware for realmente inferior aos requisitos)
    6. Estimativas realistas de FPS considerando o hardware moderno
    7. Avaliação do impacto de cada componente na performance final
    8. Considerações sobre tecnologias modernas (DLSS, FSR, Ray Tracing)
    9. Impacto da RAM e armazenamento no desempenho
    
    IMPORTANTE: Considere que hardware mais recente (últimas gerações) é geralmente
    superior em performance ao hardware mais antigo, mesmo com especificações aparentemente menores.
    
    Retorne a análise completa no formato JSON especificado.
    """
    
    try:
        # Obtém a análise do LLM
        result = llm_provider.generate_response(
            prompt=analysis_prompt,
            system_prompt=system_prompt,
            temperature=0.1  # Reduzindo ainda mais a temperatura para maior consistência
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
        
        # Criar objeto PerformanceEstimates para cada resolução
        fps_estimates = {}
        for resolution, fps_data in analysis_dict['performance_details']['estimated_fps'].items():
            fps_estimates[resolution] = PerformanceEstimates(
                baixa=fps_data['baixa'],
                media=fps_data['media'],
                alta=fps_data['alta'],
                ultra=fps_data['ultra']
            )
        
        # Criar objeto PerformanceDetails
        performance_details = PerformanceDetails(
            cpu_analysis=analysis_dict['performance_details']['cpu_analysis'],
            gpu_analysis=analysis_dict['performance_details']['gpu_analysis'],
            ram_analysis=analysis_dict['performance_details']['ram_analysis'],
            storage_impact=analysis_dict['performance_details']['storage_impact'],
            estimated_fps=fps_estimates
        )
        
        # Retornar análise completa
        return CompatibilityAnalysis(
            can_run=analysis_dict['can_run'],
            performance_level=analysis_dict['performance_level'],
            expected_issues=analysis_dict['expected_issues'],
            recommended_settings=analysis_dict['recommended_settings'] or '',
            upgrade_suggestions=analysis_dict.get('upgrade_suggestions', []),
            performance_details=performance_details
        )
        
    except Exception as e:
        raise Exception(f"Erro ao analisar compatibilidade do jogo: {str(e)}")
