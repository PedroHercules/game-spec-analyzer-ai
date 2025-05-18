from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

class BrowserScraper:
    """Base class para scrapers que usam navegador."""

    def __init__(self, headless: bool = True):
        """
        Inicializa o scraper.
        
        Args:
            headless: Se True, executa o navegador sem interface gráfica
        """
        self.options = Options()
        if headless:
            self.options.add_argument('--headless')
            
        # Configurações para evitar detecção
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = None

    def __enter__(self):
        """Configuração do contexto."""
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.options
        )
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Limpeza do contexto."""
        if self.driver:
            self.driver.quit()

    def _random_wait(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """Espera um tempo aleatório para simular comportamento humano."""
        time.sleep(random.uniform(min_seconds, max_seconds))

    def navigate(self, url: str):
        """
        Navega para uma URL.
        
        Args:
            url: URL para navegar
        """
        self.driver.get(url)
        self._random_wait()

    def find_element(self, by: By, value: str, timeout: int = 10):
        """
        Encontra um elemento na página com espera.
        
        Args:
            by: Método de busca (By.ID, By.CLASS_NAME, etc)
            value: Valor para buscar
            timeout: Tempo máximo de espera em segundos
            
        Returns:
            Elemento encontrado
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def find_elements(self, by: By, value: str, timeout: int = 10):
        """
        Encontra múltiplos elementos na página com espera.
        
        Args:
            by: Método de busca (By.ID, By.CLASS_NAME, etc)
            value: Valor para buscar
            timeout: Tempo máximo de espera em segundos
            
        Returns:
            Lista de elementos encontrados
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((by, value))
        )

    def get_text(self, element) -> str:
        """
        Obtém o texto de um elemento de forma segura.
        
        Args:
            element: Elemento web
            
        Returns:
            Texto do elemento ou string vazia
        """
        try:
            return element.text.strip()
        except:
            return ""

    def get_attribute(self, element, attribute: str) -> str:
        """
        Obtém um atributo de um elemento de forma segura.
        
        Args:
            element: Elemento web
            attribute: Nome do atributo
            
        Returns:
            Valor do atributo ou string vazia
        """
        try:
            return element.get_attribute(attribute).strip()
        except:
            return ""
