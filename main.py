import argparse
from src.services.get_requirements import get_requirements
from src.services.get_system_specs import get_system_specs

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
    if specs.gpu_memory_total:
        print(f"  Memória: {specs.gpu_memory_total}GB")
    if specs.gpu_driver:
        print(f"  Driver: {specs.gpu_driver}")
    
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

def print_game_requirements(requirements):
    """Exibe os requisitos do jogo de forma formatada."""
    print(f"\nRequisitos para '{requirements.title}':")
    if requirements.price:
        print(f"Preço: {requirements.price}")
        
    print("\nRequisitos Mínimos:")
    if not requirements.minimum:
        print("  Não disponível")
    else:
        for key, value in requirements.minimum.items():
            if key == "status" and value == "Não disponível":
                print("  Não disponível")
                break
            print(f"  {key}: {value}")
        
    print("\nRequisitos Recomendados:")
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
        description='Analisa requisitos técnicos de jogos e especificações do sistema.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Grupo de subcomandos
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Comando: verificar jogo
    check_parser = subparsers.add_parser('check', help='Verifica requisitos de um jogo')
    check_parser.add_argument(
        'game',
        help='Nome do jogo para análise',
        type=str,
        nargs='+'
    )
    
    # Comando: mostrar specs
    specs_parser = subparsers.add_parser('specs', help='Mostra especificações do sistema')
    
    # Parse os argumentos
    args = parser.parse_args()
    
    try:
        if args.command == 'check':
            # Verifica requisitos do jogo
            game_name = ' '.join(args.game)
            print("\nIniciando análise dos requisitos...")
            requirements = get_requirements(game_name)
            
            if requirements:
                print_game_requirements(requirements)
            else:
                print(f"\nNão foi possível encontrar requisitos para '{game_name}'.")
                
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
