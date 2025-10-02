# Guía: Selenium Web Automation

## 🌐 ¿Qué es Selenium?

Selenium es una herramienta que permite a los agentes **automatizar navegadores web**:
- Visitar páginas web
- Extraer información (web scraping)
- Interactuar con elementos (clicks, formularios)
- Tomar capturas de pantalla

## 📦 Instalación

Selenium ya está incluido en `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Requisitos:**
- Chrome instalado en el sistema
- Python 3.13+

## 🚀 Uso Básico

### Opción 1: Con Agente

```python
from agent_creator import Agent
from tools import create_selenium_tool

# Crear agente con Selenium
agent = Agent(
    name="Web Scraper",
    instructions="Puedes navegar páginas web y extraer información",
    tools=[create_selenium_tool()]
)

# Usar el agente
response = agent.chat("Visita https://www.example.com y dime qué ves")
```

### Opción 2: Uso Manual

```python
from selenium_handler import selenium_navigate, selenium_get_text, selenium_close

# Navegar a una página
result = selenium_navigate("https://www.example.com")
print(result['title'])  # "Example Domain"

# Obtener texto
result = selenium_get_text()
print(result['text'])

# Cerrar navegador
selenium_close()
```

## 🔧 Funciones Disponibles

### 1. `selenium_navigate(url)`

Navega a una URL.

```python
result = selenium_navigate("https://www.google.com")
# {
#     'success': True,
#     'url': 'https://www.google.com',
#     'title': 'Google',
#     'message': 'Navegado a: Google'
# }
```

### 2. `selenium_get_text()`

Obtiene todo el texto visible de la página.

```python
result = selenium_get_text()
# {
#     'success': True,
#     'text': 'Contenido de la página...',
#     'length': 5000,
#     'truncated': False
# }
```

### 3. `selenium_find_text(selector, by='css')`

Encuentra un elemento y obtiene su texto.

```python
result = selenium_find_text('h1', by='css')
# {
#     'success': True,
#     'text': 'Título de la página',
#     'tag': 'h1'
# }
```

**Tipos de selectores:**
- `'css'` - Selector CSS (default)
- `'xpath'` - XPath
- `'id'` - Por ID
- `'class'` - Por clase

### 4. `selenium_click(selector, by='css')`

Hace clic en un elemento.

```python
result = selenium_click('#submit-button', by='id')
# {
#     'success': True,
#     'message': 'Elemento clickeado',
#     'current_url': 'https://...'
# }
```

### 5. `selenium_fill(selector, text, by='css')`

Llena un campo de entrada.

```python
result = selenium_fill('#search', 'Python', by='id')
# {
#     'success': True,
#     'message': 'Texto ingresado en #search'
# }
```

### 6. `selenium_screenshot(filename)`

Toma una captura de pantalla.

```python
result = selenium_screenshot('captura.png')
# {
#     'success': True,
#     'filename': 'captura.png',
#     'message': 'Captura guardada en captura.png'
# }
```

### 7. `selenium_close()`

Cierra el navegador.

```python
result = selenium_close()
# {
#     'success': True,
#     'message': 'Navegador cerrado'
# }
```

## 📋 Ejemplos Prácticos

### Ejemplo 1: Web Scraping Básico

```python
from agent_creator import Agent
from tools import create_selenium_tool

agent = Agent(
    name="Scraper",
    instructions="Extrae información de páginas web",
    tools=[create_selenium_tool()]
)

response = agent.chat("Visita https://news.ycombinator.com y dime los títulos principales")
```

### Ejemplo 2: Buscar en Google

```python
agent = Agent(
    name="Google Searcher",
    instructions="""
    Puedes buscar en Google usando Selenium.
    1. Navega a google.com
    2. Llena el campo de búsqueda
    3. Haz clic en buscar
    4. Extrae los resultados
    """,
    tools=[create_selenium_tool()]
)

response = agent.chat("Busca 'Python tutorials' en Google")
```

### Ejemplo 3: Monitoreo de Precios

```python
agent = Agent(
    name="Price Monitor",
    instructions="Monitorea precios en sitios web",
    tools=[create_selenium_tool()]
)

response = agent.chat("Visita Amazon y busca el precio del iPhone 15")
```

### Ejemplo 4: Automatización de Formularios

```python
agent = Agent(
    name="Form Filler",
    instructions="""
    Puedes llenar formularios web.
    Usa selenium_fill para campos de entrada.
    Usa selenium_click para botones.
    """,
    tools=[create_selenium_tool()]
)

response = agent.chat("Llena el formulario de contacto en example.com")
```

## 🎯 Casos de Uso

### 1. **Web Scraping**
- Extraer información de sitios web
- Monitorear cambios en páginas
- Recopilar datos para análisis

### 2. **Automatización de Tareas**
- Llenar formularios automáticamente
- Hacer clicks en secuencia
- Navegar por múltiples páginas

### 3. **Testing**
- Probar flujos de usuario
- Verificar que elementos existan
- Tomar capturas de pantalla

### 4. **Monitoreo**
- Vigilar precios
- Detectar cambios en contenido
- Alertas automáticas

## ⚙️ Configuración Avanzada

### Modo Headless vs Visual

Por defecto, Selenium se ejecuta en modo **headless** (sin interfaz gráfica):

```python
from selenium_handler import SeleniumBrowser

# Modo headless (default)
browser = SeleniumBrowser(headless=True)

# Modo visual (ver el navegador)
browser = SeleniumBrowser(headless=False)
```

### Selectores CSS Comunes

```python
# Por ID
selenium_find_text('#mi-id', by='id')

# Por clase
selenium_find_text('.mi-clase', by='class')

# Por tag
selenium_find_text('h1', by='css')

# Selector complejo
selenium_find_text('div.container > h1', by='css')
```

### XPath

```python
# XPath básico
selenium_find_text('//h1', by='xpath')

# XPath con condiciones
selenium_find_text('//div[@class="title"]', by='xpath')
```

## 🐛 Solución de Problemas

### Error: Chrome no encontrado

**Problema:** `selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH`

**Solución:** Instala Chrome:
- **Mac:** `brew install --cask google-chrome`
- **Linux:** `sudo apt-get install google-chrome-stable`
- **Windows:** Descarga desde https://www.google.com/chrome/

### Error: Elemento no encontrado

**Problema:** `NoSuchElementException`

**Soluciones:**
1. Verifica el selector
2. Espera a que la página cargue
3. Usa selectores más específicos

### Navegador no cierra

**Problema:** El navegador queda abierto

**Solución:**
```python
from selenium_handler import selenium_close

# Siempre cierra al terminar
selenium_close()
```

## 📊 Comparación con Web Search

| Característica | Web Search | Selenium |
|----------------|------------|----------|
| **Velocidad** | ⚡ Rápido | 🐢 Más lento |
| **Contenido** | Texto indexado | Todo (JS, imágenes, etc.) |
| **Interacción** | ❌ No | ✅ Sí (clicks, formularios) |
| **Capturas** | ❌ No | ✅ Sí |
| **Costo** | Consume créditos Z.AI | Gratis (local) |
| **Uso** | Búsquedas generales | Scraping específico |

**Cuándo usar cada uno:**
- **Web Search:** Búsquedas rápidas, información general
- **Selenium:** Scraping detallado, automatización, interacción

## 🔒 Consideraciones Éticas

### ⚠️ Importante

1. **Respeta robots.txt**
   ```python
   # Verifica robots.txt antes de scrapear
   selenium_navigate("https://example.com/robots.txt")
   ```

2. **No sobrecargues servidores**
   - Agrega delays entre requests
   - No hagas scraping masivo

3. **Respeta términos de servicio**
   - Lee los términos del sitio
   - Algunos sitios prohíben scraping

4. **Datos personales**
   - No extraigas información personal
   - Cumple con GDPR/leyes locales

## 🧪 Testing

```bash
# Test básico
python demos/demo_selenium.py

# Test manual
python selenium_handler.py
```

## 📝 Mejores Prácticas

### 1. Siempre Cierra el Navegador

```python
try:
    selenium_navigate("https://example.com")
    result = selenium_get_text()
finally:
    selenium_close()  # ← Importante
```

### 2. Maneja Errores

```python
result = selenium_navigate("https://example.com")
if not result['success']:
    print(f"Error: {result['error']}")
```

### 3. Usa Selectores Específicos

```python
# ❌ Vago
selenium_find_text('div')

# ✅ Específico
selenium_find_text('div.product-title')
```

### 4. Agrega Delays

```python
import time

selenium_navigate("https://example.com")
time.sleep(2)  # Esperar a que cargue
selenium_get_text()
```

## 🔮 Próximas Mejoras

- [ ] Soporte para Firefox
- [ ] Manejo de cookies
- [ ] Scroll automático
- [ ] Espera inteligente de elementos
- [ ] Proxy support
- [ ] Capturas de elementos específicos

## ✅ Checklist de Uso

- [ ] Chrome instalado
- [ ] Selenium instalado (`pip install -r requirements.txt`)
- [ ] Crear agente con `create_selenium_tool()`
- [ ] Probar con `demos/demo_selenium.py`
- [ ] Cerrar navegador con `selenium_close()`

## 📚 Recursos

- **Selenium Docs:** https://www.selenium.dev/documentation/
- **CSS Selectors:** https://www.w3schools.com/cssref/css_selectors.php
- **XPath Tutorial:** https://www.w3schools.com/xml/xpath_intro.asp

---

**Selenium está listo para automatizar navegadores web!** 🌐🤖
