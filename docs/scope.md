# Game Spec Analyzer IA

## Descrição do Projeto

Sistema inteligente desenvolvido em Python para análise de compatibilidade entre jogos e hardware do usuário, utilizando IA (via APIs de modelos prontos) e web scraping para fornecer recomendações precisas e personalizadas.

## Objetivo

Criar uma solução escalável que permita aos usuários verificar rapidamente se seus computadores atendem aos requisitos para rodar jogos específicos, oferecendo recomendações detalhadas de configurações e otimizações. Inicialmente via linha de comando, com preparação para futura expansão via API REST.

## Arquitetura

### Estrutura de Módulos

1. **Shared (Compartilhado)**

   - Integrações com IA (OpenRouter e outros providers)
   - Implementações de Web Scraping
   - Utilitários comuns
   - Interfaces base

2. **Services (Serviços)**

   - Análise de Hardware
   - Análise de Jogos
   - Verificação de Drivers
   - Recomendações
   - Benchmarks

3. **CLI (Interface de Linha de Comando)**

   - Interação com usuário
   - Formatação de saída
   - Parsers de argumentos
   - Orquestração dos serviços

4. **HTTP (Futuro)**
   - API REST
   - Rotas
   - Middlewares
   - Documentação

### Princípios

- Módulos independentes e coesos
- Serviços reutilizáveis
- Fácil expansão para novas interfaces
- Configuração flexível de providers

## Funcionalidades Principais

### 1. Análise de Hardware

- Detecção automática das especificações do PC do usuário:
  - Processador (modelo, velocidade, núcleos)
  - Placa de vídeo (modelo, memória VRAM)
  - Memória RAM (quantidade, velocidade)
  - Armazenamento disponível
  - Sistema operacional e versão

### 2. Análise de Compatibilidade com Jogos

- Input do nome do jogo pelo usuário
- Coleta de requisitos mínimos e recomendados do jogo
- Comparação com hardware do usuário
- Análise via IA usando modelos prontos

### 3. Web Scraping de Benchmarks

- Coleta automatizada de dados de performance de fontes confiáveis
- Busca por configurações similares ao hardware do usuário
- Análise de benchmarks reais para estimativas mais precisas
- Fontes incluem:
  - Sites especializados em benchmarks
  - Fóruns de jogos
  - Plataformas de gaming

### 4. Verificação de Drivers

- Identificação da versão atual do driver da GPU
- Verificação da versão mais recente disponível
- Notificação sobre atualizações necessárias
- Link direto para download do driver atualizado

### 5. Recomendações Inteligentes

- Estimativa de FPS esperado em diferentes configurações
- Sugestões de configurações gráficas ideais
- Recomendações de otimização
- Alertas sobre possíveis gargalos de performance

## Tecnologias Utilizadas

### Core

- Python 3.x
- APIs de IA (OpenRouter)
- Web Scraping (BeautifulSoup/Scrapy)
- APIs de fabricantes (NVIDIA, AMD)

### Bibliotecas Principais

- Sistema: psutil, WMI (Windows Management Instrumentation)
- Web Scraping: BeautifulSoup4, requests
- HTTP: aiohttp, FastAPI (futuro)
- Processamento de Dados: pandas

### Providers de IA

- OpenRouter (principal)
- Suporte a múltiplos providers via interface comum
- Fácil substituição de modelos

## Interfaces

### CLI (Inicial)

- Interface por linha de comando
- Apresentação formatada dos resultados
- Opções de configuração via argumentos

### API REST (Futura)

- Endpoints RESTful
- Documentação via OpenAPI/Swagger
- Autenticação e rate limiting
- Respostas em JSON

## Fluxo de Funcionamento

1. Usuário insere o nome do jogo
2. Sistema coleta especificações do PC
3. Sistema busca informações do jogo e benchmarks
4. IA processa dados e gera análises
5. Sistema verifica drivers
6. Apresentação dos resultados ao usuário

## Saída de Dados

```
Nome do Jogo: [nome]
Status: [Pode Rodar / Não Recomendado]

Análise de Hardware:
- CPU: [Status]
- GPU: [Status]
- RAM: [Status]
- Storage: [Status]

Performance Esperada:
- FPS Estimado: [X-Y FPS]
- Qualidade Recomendada: [Baixa/Média/Alta/Ultra]

Configurações Recomendadas:
- Resolução: [Resolução ideal]
- Preset Gráfico: [Configuração]
- Configurações Específicas: [Lista de ajustes]

Status do Driver:
- Versão Atual: [versão]
- Versão Mais Recente: [versão]
- Status: [Atualizado/Desatualizado]
```

## Próximas Etapas

1. **Fase 1 - CLI**

   - Implementação da camada shared (IA e Web Scraping)
   - Desenvolvimento dos serviços principais
   - Implementação da interface CLI
   - Testes unitários e de integração

2. **Fase 2 - API (Opcional)**
   - Implementação da camada HTTP
   - Adaptação dos serviços para API REST
   - Documentação da API
   - Monitoramento e logging
