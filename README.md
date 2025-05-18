# Game System Requirements Analyzer

Sistema automatizado para análise de compatibilidade e performance de jogos usando IA.

## Sobre o Projeto

O projeto coleta e analisa:

1. **Especificações do Sistema**

   - Hardware detalhado (CPU, GPU, RAM, Storage)
   - Métricas em tempo real (temperaturas, uso)
   - Drivers e versões do sistema

2. **Requisitos dos Jogos**

   - Requisitos mínimos e recomendados
   - Compatibilidade com diferentes sistemas
   - Preço e disponibilidade

## Instalação

1. Clone o repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Uso

### 1. Análise Completa de um Jogo:

```bash
python main.py analyze "Nome do Jogo"
```

Exemplo:

```bash
python main.py analyze "God of War"
```

Isso mostrará:

- Requisitos do jogo
- Compatibilidade com o sistema

### 2. Verificar Especificações do Sistema:

```bash
python main.py specs
```

Mostra informações detalhadas sobre:

- Processador
- Placa de vídeo
- Memória RAM
- Armazenamento
- Sistema operacional

## Estrutura do Projeto

```
src/
  ├── services/
  │   ├── get_requirements.py    # Requisitos dos jogos
  │   └── get_system_specs.py    # Specs do sistema
  └── shared/
      └── scraping/
          ├── game_system_requirements.py
          └── browser_scraper.py
```

## Exemplo de Saída

### Análise de Jogo

```
=== Análise de 'Cyberpunk 2077' ===

Requisitos do Jogo:
----------------------------------------
Preço: R$ 199,90

Mínimos:
  OS: Windows 10
  CPU: Intel Core i5-3570K
  RAM: 8 GB
  GPU: NVIDIA GeForce GTX 970
  Storage: 70 GB

Recomendados:
  OS: Windows 10
  CPU: Intel Core i7-4790
  RAM: 16 GB
  GPU: NVIDIA GeForce GTX 1060 6GB
  Storage: 70 GB
```

## Próximos Passos

1. Análise detalhada de compatibilidade
2. Recomendações personalizadas por jogo
3. API para consulta externa
