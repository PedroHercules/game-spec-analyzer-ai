import argparse
from src.services.get_requirements import get_requirements
from src.services.get_system_specs import get_system_specs

def print_system_specs(specs):
    """Exibe as especificações do sistema de forma formatada."""
    print("\nEspecificações do Sistema:")
    print("\nProcessador:")
    print(f"  Modelo: {specs.cpu_name}")
    print(f"  Núcleos: {specs.cpu_cores} físicos, {specs.cpu_threads} threads")
    print(f"  Frequência: {specs.cpu_freq_base}GHz (Base) / {specs.cpu_freq_max}GHz (Max)")
    
    print("\nMemória RAM:")
    print(f"  Total: {specs.ram_total}GB")
    print(f"  Disponível: {specs.ram_free}GB")
    if specs.ram_speed:
        print(f"  Velocidade: {specs.ram_speed}MHz")
    
    print("\nPlaca de Vídeo:")
    print(f"  Modelo: {specs.gpu_name}")
    if specs.gpu_memory:
        print(f"  Memória: {specs.gpu_memory}GB")
    if specs.gpu_driver:
        print(f"  Driver: {specs.gpu_driver}")
    
    print("\nArmazenamento:")
    print(f"  Espaço Total: {specs.disk_total}GB")
    print(f"  Espaço Livre: {specs.disk_free}GB")
    
    print("\nSistema:")
    print(f"  Sistema Operacional: {specs.os_name} {specs.os_version}")
    if specs.directx_version:
        print(f"  DirectX: {specs.directx_version}")

def main():
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(
        description='Analisa requisitos técnicos de jogos.',
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
            else:
                print(f"\nNão foi possível encontrar requisitos para '{game_name}'.")
                
        elif args.command == 'specs':
            # Mostra especificações do sistema
            specs = get_system_specs()
            print_system_specs(specs)
            
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"\nErro: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()
