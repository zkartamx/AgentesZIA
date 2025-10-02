"""
Manejador de Selenium para automatización web
Permite a los agentes interactuar con navegadores web
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json


class SeleniumBrowser:
    """Clase para manejar operaciones de Selenium"""
    
    def __init__(self, headless: bool = True):
        """
        Inicializa el navegador
        
        Args:
            headless: Si True, ejecuta sin interfaz gráfica
        """
        self.headless = headless
        self.driver = None
    
    def start_browser(self):
        """Inicia el navegador Chrome"""
        if self.driver:
            return
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
    
    def close_browser(self):
        """Cierra el navegador"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def navigate_to(self, url: str) -> dict:
        """
        Navega a una URL
        
        Args:
            url: URL a visitar
            
        Returns:
            Resultado de la navegación
        """
        try:
            if not self.driver:
                self.start_browser()
            
            self.driver.get(url)
            time.sleep(2)  # Esperar a que cargue
            
            return {
                'success': True,
                'url': self.driver.current_url,
                'title': self.driver.title,
                'message': f'Navegado a: {self.driver.title}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_page_text(self) -> dict:
        """
        Obtiene el texto visible de la página
        
        Returns:
            Texto de la página
        """
        try:
            if not self.driver:
                return {'success': False, 'error': 'Navegador no iniciado'}
            
            text = self.driver.find_element(By.TAG_NAME, 'body').text
            
            return {
                'success': True,
                'text': text[:5000],  # Limitar a 5000 caracteres
                'length': len(text),
                'truncated': len(text) > 5000
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def find_element_text(self, selector: str, by: str = 'css') -> dict:
        """
        Encuentra un elemento y obtiene su texto
        
        Args:
            selector: Selector del elemento
            by: Tipo de selector ('css', 'xpath', 'id', 'class')
            
        Returns:
            Texto del elemento
        """
        try:
            if not self.driver:
                return {'success': False, 'error': 'Navegador no iniciado'}
            
            by_type = {
                'css': By.CSS_SELECTOR,
                'xpath': By.XPATH,
                'id': By.ID,
                'class': By.CLASS_NAME
            }.get(by, By.CSS_SELECTOR)
            
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((by_type, selector))
            )
            
            return {
                'success': True,
                'text': element.text,
                'tag': element.tag_name
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def click_element(self, selector: str, by: str = 'css') -> dict:
        """
        Hace clic en un elemento
        
        Args:
            selector: Selector del elemento
            by: Tipo de selector
            
        Returns:
            Resultado del clic
        """
        try:
            if not self.driver:
                return {'success': False, 'error': 'Navegador no iniciado'}
            
            by_type = {
                'css': By.CSS_SELECTOR,
                'xpath': By.XPATH,
                'id': By.ID,
                'class': By.CLASS_NAME
            }.get(by, By.CSS_SELECTOR)
            
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((by_type, selector))
            )
            element.click()
            time.sleep(1)
            
            return {
                'success': True,
                'message': 'Elemento clickeado',
                'current_url': self.driver.current_url
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def fill_input(self, selector: str, text: str, by: str = 'css') -> dict:
        """
        Llena un campo de entrada
        
        Args:
            selector: Selector del campo
            text: Texto a ingresar
            by: Tipo de selector
            
        Returns:
            Resultado de la operación
        """
        try:
            if not self.driver:
                return {'success': False, 'error': 'Navegador no iniciado'}
            
            by_type = {
                'css': By.CSS_SELECTOR,
                'xpath': By.XPATH,
                'id': By.ID,
                'class': By.CLASS_NAME
            }.get(by, By.CSS_SELECTOR)
            
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((by_type, selector))
            )
            element.clear()
            element.send_keys(text)
            
            return {
                'success': True,
                'message': f'Texto ingresado en {selector}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def take_screenshot(self, filename: str = 'screenshot.png') -> dict:
        """
        Toma una captura de pantalla
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            Resultado de la captura
        """
        try:
            if not self.driver:
                return {'success': False, 'error': 'Navegador no iniciado'}
            
            self.driver.save_screenshot(filename)
            
            return {
                'success': True,
                'filename': filename,
                'message': f'Captura guardada en {filename}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Instancia global del navegador
_browser = None


def get_browser(headless: bool = True) -> SeleniumBrowser:
    """Obtiene o crea la instancia del navegador"""
    global _browser
    if _browser is None:
        _browser = SeleniumBrowser(headless=headless)
    return _browser


def selenium_navigate(url: str) -> dict:
    """Navega a una URL"""
    browser = get_browser()
    return browser.navigate_to(url)


def selenium_get_text() -> dict:
    """Obtiene el texto de la página actual"""
    browser = get_browser()
    return browser.get_page_text()


def selenium_find_text(selector: str, by: str = 'css') -> dict:
    """Encuentra y obtiene texto de un elemento"""
    browser = get_browser()
    return browser.find_element_text(selector, by)


def selenium_click(selector: str, by: str = 'css') -> dict:
    """Hace clic en un elemento"""
    browser = get_browser()
    return browser.click_element(selector, by)


def selenium_fill(selector: str, text: str, by: str = 'css') -> dict:
    """Llena un campo de entrada"""
    browser = get_browser()
    return browser.fill_input(selector, text, by)


def selenium_screenshot(filename: str = 'screenshot.png') -> dict:
    """Toma una captura de pantalla"""
    browser = get_browser()
    return browser.take_screenshot(filename)


def selenium_close() -> dict:
    """Cierra el navegador"""
    global _browser
    if _browser:
        _browser.close_browser()
        _browser = None
        return {'success': True, 'message': 'Navegador cerrado'}
    return {'success': True, 'message': 'Navegador ya estaba cerrado'}


def handle_selenium_call(function_name: str, arguments: dict) -> dict:
    """
    Maneja las llamadas a funciones de Selenium
    
    Args:
        function_name: Nombre de la función
        arguments: Argumentos de la función
        
    Returns:
        Resultado de la función
    """
    if function_name == 'selenium_navigate':
        return selenium_navigate(arguments.get('url'))
    
    elif function_name == 'selenium_get_text':
        return selenium_get_text()
    
    elif function_name == 'selenium_find_text':
        return selenium_find_text(
            arguments.get('selector'),
            arguments.get('by', 'css')
        )
    
    elif function_name == 'selenium_click':
        return selenium_click(
            arguments.get('selector'),
            arguments.get('by', 'css')
        )
    
    elif function_name == 'selenium_fill':
        return selenium_fill(
            arguments.get('selector'),
            arguments.get('text'),
            arguments.get('by', 'css')
        )
    
    elif function_name == 'selenium_screenshot':
        return selenium_screenshot(arguments.get('filename', 'screenshot.png'))
    
    elif function_name == 'selenium_close':
        return selenium_close()
    
    else:
        return {
            'success': False,
            'error': f'Función desconocida: {function_name}'
        }


if __name__ == "__main__":
    print("=" * 70)
    print("  TEST: Selenium Handler")
    print("=" * 70)
    
    # Test básico
    print("\n1. Navegando a Google...")
    result = selenium_navigate("https://www.google.com")
    print(f"   {result}")
    
    print("\n2. Obteniendo texto de la página...")
    result = selenium_get_text()
    if result['success']:
        print(f"   Texto obtenido: {len(result['text'])} caracteres")
        print(f"   Primeros 200: {result['text'][:200]}...")
    
    print("\n3. Cerrando navegador...")
    result = selenium_close()
    print(f"   {result}")
    
    print("\n" + "=" * 70)
    print("  Test completado!")
    print("=" * 70)
