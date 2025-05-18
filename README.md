# Game System Requirements Analyzer

An automated system for analyzing game compatibility and performance using AI.

## About

This project collects and analyzes:

1. **System Specifications**

   - Detailed hardware information (CPU, GPU, RAM, Storage)
   - Real-time metrics (temperatures, usage)
   - System drivers and versions

2. **Game Requirements**

   - Minimum and recommended requirements
   - System compatibility
   - Price and availability
   - Performance benchmarks

3. **AI-Powered Analysis**
   - Compatibility assessment
   - Performance predictions
   - Smart recommendations

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/game-spec-analyzer-ia.git
cd game-spec-analyzer-ia
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment:
   - Copy `.env.example` to `.env`
   - Set your OpenRouter API credentials:
     ```
     OPENROUTER_API_KEY=your_api_key_here
     OPENROUTER_MODEL=your_model_here  # e.g., openai/gpt-3.5-turbo
     ```

## Usage

### 1. Complete Game Analysis:

```bash
python main.py analyze "Game Name"
```

Example:

```bash
python main.py analyze "God of War"
```

This will display:

- Game requirements
- System compatibility
- Performance predictions
- Smart recommendations

### 2. Check System Specifications:

```bash
python main.py specs
```

Shows detailed information about:

- Processor
- Graphics card
- RAM
- Storage
- Operating system

### 3. Game Performance Analysis:

```bash
python main.py performance "Game Name"
```

Provides:

- Expected FPS ranges
- Recommended settings
- Performance bottlenecks

## Project Structure

```
src/
├── services/
│   ├── analyze_game_compatibility.py
│   ├── get_game_performance.py
│   ├── get_requirements.py
│   └── get_system_specs.py
└── shared/
    ├── providers/
    │   └── llm_provider.py
    └── scraping/
        ├── base_scraper.py
        ├── browser_scraper.py
        ├── game_benchmarks.py
        ├── game_system_requirements.py
        ├── google_scraper.py
        └── human_like_scraper.py
```

## Example Output

### Game Analysis

```
=== Analysis of 'Cyberpunk 2077' ===

Game Requirements:
----------------------------------------
Price: $59.99

Minimum:
  OS: Windows 10
  CPU: Intel Core i5-3570K
  RAM: 8 GB
  GPU: NVIDIA GeForce GTX 970
  Storage: 70 GB

Recommended:
  OS: Windows 10
  CPU: Intel Core i7-4790
  RAM: 16 GB
  GPU: NVIDIA GeForce GTX 1060 6GB
  Storage: 70 GB

Compatibility Analysis:
----------------------------------------
System Score: 8.5/10
- CPU: Exceeds recommended (✓)
- GPU: Meets recommended (✓)
- RAM: Exceeds minimum (!)
- Storage: Available (✓)

Performance Prediction:
----------------------------------------
Expected FPS (1080p, High Settings): 55-65
Recommended Settings:
- Resolution: 1080p
- Texture Quality: High
- Ray Tracing: Off
- DLSS: Quality
```

## Dependencies

- **Web Scraping**

  - selenium >= 4.1.0
  - webdriver-manager >= 3.8.0
  - beautifulsoup4 >= 4.9.3
  - lxml >= 4.9.0

- **System & Hardware**

  - psutil >= 5.9.0
  - wmi >= 1.5.1

- **Utilities**
  - requests >= 2.28.0
  - python-dotenv >= 0.19.0

## Features in Development

1. Detailed performance analytics
2. Multi-game comparison
3. Historical performance tracking
4. Game settings optimization
5. External API for remote queries
