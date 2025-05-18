# Game System Requirements Analyzer

Sistema automatizado para análise de requisitos técnicos de jogos e especificações do sistema.

## Instalação

1. Clone o repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Uso

O sistema possui dois comandos principais:

### 1. Verificar requisitos de um jogo:

```bash
python main.py check "Nome do Jogo"
```

Por exemplo:

```bash
python main.py check "God of War"
python main.py check "Half-Life 2"
python main.py check "Cyberpunk 2077"
```

### 2. Verificar especificações do seu sistema:

```bash
python main.py specs
```

Isso mostrará informações detalhadas sobre:

- Processador (modelo, núcleos, frequência)
- Memória RAM (total, disponível, velocidade)
- Placa de Vídeo (modelo, memória, driver)
- Armazenamento (espaço total e livre)
- Sistema Operacional e DirectX

## Estrutura do Projeto

```
src/
  ├── services/                   # Serviços da aplicação
  │   ├── get_requirements.py    # Coleta requisitos de jogos
  │   └── get_system_specs.py    # Coleta specs do sistema
  └── shared/                    # Código compartilhado
      └── scraping/             # Funcionalidade de scraping
          ├── __init__.py
          └── game_system_requirements.py
```

## Exemplo de Saída

### Verificando um Jogo

```
Iniciando análise dos requisitos...

Requisitos para 'Half-Life 2':
Preço: R$ 20,69

Requisitos Mínimos:
  OS: Windows 7, Vista, XP
  Processor: 1.7 Ghz
  Memory: 512 MB RAM
  Graphics: DirectX 8.1 level Graphics Card
  Storage: 6.5 GB available space

Requisitos Recomendados:
  OS: Windows 7
  Processor: 2.4 Ghz
  Memory: 1 GB RAM
  Graphics: DirectX 9 level Graphics Card
  Storage: 6.5 GB available space
```

### Verificando o Sistema

```
Especificações do Sistema:

Processador:
  Modelo: Intel(R) Core(TM) i7-9700K CPU @ 3.60GHz
  Núcleos: 8 físicos, 8 threads
  Frequência: 3.6GHz (Base) / 4.9GHz (Max)

Memória RAM:
  Total: 32GB
  Disponível: 24GB
  Velocidade: 3200MHz

Placa de Vídeo:
  Modelo: NVIDIA GeForce RTX 3070
  Memória: 8GB
  Driver: 531.41

Armazenamento:
  Espaço Total: 1000GB
  Espaço Livre: 450GB

Sistema:
  Sistema Operacional: Windows 11 (10.0.22621)
  DirectX: DirectX 12
```
