import argparse
from src.services.get_requirements import get_requirements
from src.services.get_system_specs import get_system_specs
from src.services.analyze_game_compatibility import analyze_game_compatibility

def print_system_specs(specs):
    """Exibe as especificações do sistema de forma formatada para análise."""
    print("\n=== Análise do Sistema ===\n")
    
    print("Processador:")
    print(f"  Modelo: {specs.cpu_name}")
    print(f"  Arquitetura: {specs.cpu_architecture or 'Não disponível'}")
    print(f"  Núcleos: {specs.cpu_cores} físicos, {specs.cpu_threads} threads")
    print(f"  Frequência Base: {specs.cpu_freq_base}GHz")
    print(f"  Frequência Máxima: {specs.cpu_freq_max}GHz")
    if specs.cpu_temp:
        print(f"  Temperatura: {specs.cpu_temp}°C")
    if specs.cpu_load:
        print(f"  Uso atual: {specs.cpu_load}%")
    
    print("\nMemória RAM:")
    print(f"  Total: {specs.ram_total}GB")
    print(f"  Em uso: {specs.ram_used}GB")
    print(f"  Disponível: {specs.ram_free}GB")
    if specs.ram_speed:
        print(f"  Velocidade: {specs.ram_speed}MHz")
    if specs.ram_type:
        print(f"  Tipo: {specs.ram_type}")
    
    print("\nPlaca de Vídeo:")
    print(f"  Modelo: {specs.gpu_name}")
    if specs.gpu_architecture:
        print(f"  Arquitetura: {specs.gpu_architecture}")
    if specs.gpu_memory_total:
        print(f"  Memória: {specs.gpu_memory_total}GB {specs.gpu_memory_type or ''}")
    if specs.gpu_driver:
        print(f"  Driver: {specs.gpu_driver}")
        if specs.gpu_driver_date:
            print(f"  Data do Driver: {specs.gpu_driver_date}")
    if specs.gpu_resolution:
        print(f"  Resolução: {specs.gpu_resolution}")
        if specs.gpu_refresh_rate:
            print(f"  Taxa de Atualização: {specs.gpu_refresh_rate}Hz")
    
    # Mostra tecnologias suportadas
    if specs.gpu_tech_support:
        print("\n  Tecnologias Suportadas:")
        if specs.gpu_tech_support.get('dlss'):
            print("    - NVIDIA DLSS")
        if specs.gpu_tech_support.get('ray_tracing'):
            print("    - Ray Tracing")
        if specs.gpu_tech_support.get('dx12_ultimate'):
            print("    - DirectX 12 Ultimate")
        if specs.gpu_tech_support.get('fsr'):
            print("    - AMD FSR")
    
    print("\nArmazenamento:")
    for device in specs.storage_devices:
        print(f"\n  Drive ({device.mount_point}):")
        print(f"    Tipo: {device.type}")
        print(f"    Capacidade: {device.total}GB")
        print(f"    Livre: {device.free}GB")
        print(f"    Em uso: {device.total - device.free}GB")
    
    print("\nSistema:")
    print(f"  Sistema Operacional: {specs.os_name} {specs.os_version}")
    if specs.os_build:
        print(f"  Build: {specs.os_build}")
    if specs.directx_version:
        print(f"  DirectX: {specs.directx_version}")

def print_game_analysis(game_name):
    """Exibe análise completa do jogo incluindo requisitos e compatibilidade."""
    print(f"\n=== Análise de '{game_name}' ===\n")
    
    # Obtém requisitos
    print("Buscando requisitos...")
    requirements = get_requirements(game_name)
    if not requirements:
        print("Não foi possível encontrar os requisitos do jogo.")
        return
    
    # Obtém especificações do sistema
    print("\nAnalisando sistema...")
    specs = get_system_specs()
    
    # Realiza análise de compatibilidade
    print("\nAnalisando compatibilidade...")
    try:
        analysis = analyze_game_compatibility(specs, requirements)
        
        # Mostra resultado da análise
        print("\n=== Resultado da Análise ===")
        print("-" * 40)
        print(f"Pode rodar o jogo? {'Sim' if analysis.can_run else 'Não'}")
        print(f"Performance esperada: {analysis.performance_level}")
        
        if analysis.expected_issues:
            print("\nPossíveis problemas:")
            for issue in analysis.expected_issues:
                print(f"  - {issue}")
        
        print("\nAnálise Detalhada:")
        print("-" * 40)
        print("\nProcessador:")
        print(analysis.performance_details.cpu_analysis)
        
        print("\nPlaca de Vídeo:")
        print(analysis.performance_details.gpu_analysis)
        
        print("\nMemória RAM:")
        print(analysis.performance_details.ram_analysis)
        
        print("\nArmazenamento:")
        print(analysis.performance_details.storage_impact)
        
        print("\nEstimativas de FPS:")
        for resolution, fps in analysis.performance_details.estimated_fps.items():
            print(f"\n  {resolution}:")
            print(f"    Baixa: {fps.baixa}")
            print(f"    Média: {fps.media}")
            print(f"    Alta: {fps.alta}")
            print(f"    Ultra: {fps.ultra}")
        
        print("\nConfigurações Recomendadas:")
        print(analysis.recommended_settings)
        
        if analysis.upgrade_suggestions:
            print("\nSugestões de Upgrade:")
            for suggestion in analysis.upgrade_suggestions:
                print(f"  - {suggestion}")
    except Exception as e:
        print(f"\nErro ao analisar compatibilidade: {str(e)}")
    
    # Mostra requisitos detalhados
    print("\nRequisitos do Jogo:")
    print("-" * 40)
    if requirements.price:
        print(f"Preço: {requirements.price}")
        
    print("\nMínimos:")
    if not requirements.minimum:
        print("  Não disponível")
    else:
        for key, value in requirements.minimum.items():
            if key == "status" and value == "Não disponível":
                print("  Não disponível")
                break
            print(f"  {key}: {value}")
            
    print("\nRecomendados:")
    if not requirements.recommended:
        print("  Não disponível")
    else:
        for key, value in requirements.recommended.items():
            if key == "status" and value == "Não disponível":
                print("  Não disponível")
                break
            print(f"  {key}: {value}")
    
    print(f"\nFonte: {requirements.source_url}")

def main():
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(
        description='Analisa requisitos e performance de jogos.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Grupo de subcomandos
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Comando: analisar jogo
    analyze_parser = subparsers.add_parser('analyze', help='Análise completa de um jogo')
    analyze_parser.add_argument(
        'game',
        help='Nome do jogo para análise',
        type=str,
        nargs='+'
    )
    
    # Comando: verificar specs
    specs_parser = subparsers.add_parser('specs', help='Mostra especificações do sistema')
    
    # Parse os argumentos
    args = parser.parse_args()
    
    try:
        if args.command == 'analyze':
            # Análise completa do jogo
            game_name = ' '.join(args.game)
            print_game_analysis(game_name)
                
        elif args.command == 'specs':
            # Mostra especificações do sistema
            print("\nColetando informações do sistema...")
            specs = get_system_specs()
            print_system_specs(specs)
            
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"\nErro: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()
