from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from typing import Dict, Optional
import logging
import time

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

@dataclass
class GameRequirements:
    """Requisitos do jogo."""
    minimum: Dict[str, str]
    recommended: Dict[str, str]
    source_url: str
    price: Optional[str] = None
    title: Optional[str] = None

class GameSystemRequirements:
    """Sistema automatizado de análise de requisitos de jogos."""

    def __init__(self):
        self.driver = None
        print("\n=== Iniciando Sistema de Análise de Requisitos ===")
        logger.info("Inicializando sistema de análise")

    def __enter__(self):
        print("\n>> Preparando ambiente de análise...")
        
        # Configura ambiente virtual
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        
        # Inicializa sistema
        logger.info("Configurando subsistemas")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=chrome_options
        )
        print("✓ Ambiente preparado com sucesso")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            print("\n>> Finalizando processo...")
            self.driver.quit()
            print("✓ Sistema encerrado com sucesso")
            logger.info("Processo finalizado")

    def get_game_requirements(self, game_name: str) -> Optional[GameRequirements]:
        """
        Analisa e extrai requisitos técnicos do jogo especificado.
        
        Args:
            game_name: Nome do jogo para análise
            
        Returns:
            GameRequirements se encontrado, None caso contrário
        """
        try:
            print(f"\n=== Iniciando análise técnica: {game_name} ===")
            logger.info(f"Iniciando análise para: {game_name}")
            
            # Fase 1: Inicialização e preparação
            print("\n>> Fase 1: Preparação da análise...")
            self.driver.get("https://store.steampowered.com/search/")
            time.sleep(2)
            logger.info("Fase 1 concluída: Ambiente preparado")

            # Fase 2: Localização e acesso
            print(">> Fase 2: Localizando especificações...")
            search_box = self.driver.find_element(By.ID, "store_nav_search_term")
            search_box.send_keys(game_name)
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)
            logger.info("Fase 2 concluída: Especificações localizadas")

            # Fase 3: Extração de dados primários
            print(">> Fase 3: Processando dados primários...")
            first_result = self.driver.find_element(By.CLASS_NAME, "search_result_row")
            game_url = first_result.get_attribute("href")
            first_result.click()
            time.sleep(3)
            logger.info("Fase 3 concluída: Dados primários obtidos")

            # Fase 4: Validação de acesso
            try:
                age_gate = self.driver.find_elements(By.ID, "ageYear")
                if age_gate:
                    print(">> Aplicando protocolo de validação...")
                    self.driver.find_element(By.ID, "ageYear").send_keys("1990")
                    self.driver.find_element(By.CLASS_NAME, "btnv6_blue_hoverfade").click()
                    time.sleep(2)
                    logger.info("Protocolo de validação concluído")
            except:
                pass

            # Fase 5: Coleta de metadados
            print("\n>> Fase 5: Coletando metadados...")
            title = self.driver.find_element(By.ID, "appHubAppName").text
            logger.info("Metadados básicos obtidos")

            # Fase 6: Análise econômica
            try:
                discounted_price = self.driver.find_element(By.CLASS_NAME, "discount_final_price").text
                original_price = self.driver.find_element(By.CLASS_NAME, "discount_original_price").text
                price = f"{discounted_price} (Original: {original_price})"
                logger.info("Análise econômica: Preço promocional detectado")
            except:
                try:
                    price = self.driver.find_element(By.CLASS_NAME, "game_purchase_price").text
                    if not price or "Free" in price:
                        price = "Free"
                    logger.info("Análise econômica: Preço padrão detectado")
                except:
                    price = "TBD"
                    logger.warning("Análise econômica inconclusiva")

            # Fase 7: Análise técnica detalhada
            print(">> Fase 7: Analisando requisitos técnicos...")
            min_reqs = {}
            rec_reqs = {}

            try:
                sys_req = self.driver.find_element(By.CLASS_NAME, "sysreq_contents")
                
                # Análise de requisitos mínimos
                try:
                    print("  > Processando especificações mínimas...")
                    min_section = sys_req.find_element(By.CSS_SELECTOR, "div.game_area_sys_req_leftCol")
                    min_reqs = self._parse_requirements_section(min_section)
                    logger.info("Especificações mínimas processadas")
                except:
                    try:
                        print("  > Processando especificações unificadas...")
                        full_section = sys_req.find_element(By.CSS_SELECTOR, "div.game_area_sys_req_full")
                        min_reqs = self._parse_requirements_section(full_section)
                        logger.info("Especificações unificadas processadas")
                    except:
                        min_reqs = {"status": "Não disponível"}
                        logger.warning("Especificações mínimas indisponíveis")

                # Análise de requisitos recomendados
                try:
                    print("  > Processando especificações recomendadas...")
                    rec_section = sys_req.find_element(By.CSS_SELECTOR, "div.game_area_sys_req_rightCol")
                    rec_reqs = self._parse_requirements_section(rec_section)
                    logger.info("Especificações recomendadas processadas")
                except:
                    rec_reqs = {"status": "Não disponível"}
                    logger.warning("Especificações recomendadas indisponíveis")

            except Exception as e:
                logger.error(f"Falha na análise técnica: {str(e)}")
                min_reqs = {"status": "Não disponível"}
                rec_reqs = {"status": "Não disponível"}
                print("✗ Falha na análise de requisitos técnicos")

            print("\n✓ Análise técnica concluída com sucesso!")
            return GameRequirements(
                minimum=min_reqs,
                recommended=rec_reqs,
                source_url=game_url,
                price=price,
                title=title
            )

        except Exception as e:
            error_msg = f"Falha no processo de análise: {str(e)}"
            logger.error(error_msg)
            print(f"\n✗ {error_msg}")
            return None

    def _parse_requirements_section(self, section) -> Dict[str, str]:
        """
        Processa e estrutura as especificações técnicas.
        
        Args:
            section: Seção contendo especificações
            
        Returns:
            Dicionário com especificações processadas
        """
        requirements = {}
        
        try:
            text = section.text
            lines = text.split('\n')
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    requirements[key.strip()] = value.strip()
            
            if not requirements:
                requirements["raw"] = text.strip()
            
            return requirements
            
        except Exception as e:
            logger.error(f"Erro no processamento: {str(e)}")
            return {"status": "Não disponível"}
