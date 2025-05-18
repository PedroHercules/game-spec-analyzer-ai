# Game System Requirements Analyzer

Sistema automatizado para análise de compatibilidade e performance de jogos usando IA.

## Sobre o Projeto

O projeto coleta dados detalhados para alimentar uma IA que analisará:

- Compatibilidade de jogos com o hardware
- Performance esperada (FPS)
- Possíveis gargalos
- Recomendações de configurações
- Sugestões de upgrade

### Dados Coletados

1. **Hardware:**

   - **CPU**: modelo, cores, threads, frequências, temperatura, uso
   - **GPU**: modelo (dedicada ou integrada), memória, drivers
   - **RAM**: quantidade, velocidade, tipo (DDR4/DDR5)
   - **Storage**: tipo (SSD/HDD/NVMe), espaço, velocidades

2. **Sistema:**

   - Sistema Operacional e build
   - Versão do DirectX
   - Drivers e atualizações

3. **Jogos:**
   - Requisitos mínimos e recomendados
   - Performance reportada por usuários
   - Configurações sugeridas

## Instalação

1. Clone o repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Uso

### Analisar Requisitos de um Jogo:

```bash
python main.py check "Nome do Jogo"
```

Exemplo:

```bash
python main.py check "God of War"
```

### Verificar Especificações do Sistema:

```bash
python main.py specs
```

### Exemplo de Saída:

```
=== Análise do Sistema ===

Processador:
  Modelo: AMD Ryzen 7 5800X
  Núcleos: 8 físicos, 16 threads
  Frequência: 3.8GHz (Base) / 4.7GHz (Max)
  Temperatura: 65°C
  Uso: 25%

Memória RAM:
  Total: 32GB
  Em uso: 12GB
  Disponível: 20GB
  Velocidade: 3200MHz
  Tipo: DDR4

Placa de Vídeo:
  Modelo: NVIDIA GeForce RTX 3070
  Memória: 8GB GDDR6
  Driver: 531.41

Armazenamento:
  Tipo: NVMe SSD
  Total: 1000GB
  Livre: 450GB
  Em uso: 550GB

Sistema:
  Windows 11 Pro (22H2)
  DirectX 12
```

## Estrutura do Projeto

```
src/
  ├── services/
  │   ├── get_requirements.py    # Coleta requisitos de jogos
  │   └── get_system_specs.py    # Coleta specs do sistema
  └── shared/
      └── scraping/             # Funcionalidade de scraping
```

## Próximos Passos

1. Integração com IA para:

   - Análise de compatibilidade
   - Previsão de performance
   - Recomendações personalizadas
   - Benchmarks comparativos

2. Coleta de dados adicionais:

   - Benchmarks em tempo real
   - Métricas de temperatura
   - Uso de VRAM
   - Performance em diferentes resoluções

3. Base de conhecimento:
   - Padrões de performance
   - Problemas comuns
   - Soluções recomendadas
   - Histórico de atualizações
