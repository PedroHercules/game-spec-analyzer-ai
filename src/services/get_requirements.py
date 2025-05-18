from src.shared.scraping import GameSystemRequirements, GameRequirements

def get_requirements(game_name: str) -> GameRequirements:
    """
    Obtém os requisitos do jogo especificado.

    Args:
        game_name: Nome do jogo para análise

    Returns:
        GameRequirements se encontrado, None caso contrário
    """
    with GameSystemRequirements() as scraper:
        return scraper.get_game_requirements(game_name)
