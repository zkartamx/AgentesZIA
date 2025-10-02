# Guía: Herramientas (Tools) para Agentes

## 🔧 ¿Qué son las Herramientas?

Las herramientas (tools) son capacidades especiales que puedes dar a tus agentes para que puedan realizar tareas más allá de solo generar texto. Por ejemplo:
- **Web Search**: Buscar información actualizada en internet
- **Code Interpreter**: Ejecutar código Python
- **Drawing Tool**: Generar imágenes

---

## 📋 Herramientas Disponibles

### 1. Web Search (Búsqueda Web)
Permite al agente buscar información actualizada en internet.

**Cuándo usarla:**
- Preguntas sobre eventos actuales
- Información que cambia frecuentemente
- Datos específicos que necesitan verificación

**Ejemplo:**
```python
from agent_creator import Agent
from tools import create_web_search_tool

agent = Agent(
    name="Investigador",
    instructions="Eres un investigador. Usa búsqueda web para encontrar información precisa.",
    tools=[create_web_search_tool()]
)

response = agent.chat("What are the latest AI developments in 2024?")
```

### 2. Code Interpreter (Intérprete de Código)
Permite al agente ejecutar código Python.

**Cuándo usarla:**
- Cálculos complejos
- Análisis de datos
- Generación de gráficos
- Procesamiento de archivos

**Ejemplo:**
```python
from tools import create_code_interpreter_tool

agent = Agent(
    name="Programador",
    instructions="Eres un experto en Python. Puedes ejecutar código.",
    tools=[create_code_interpreter_tool()]
)

response = agent.chat("Calculate the factorial of 20")
```

### 3. Drawing Tool (Herramienta de Dibujo)
Permite al agente generar imágenes.

**Cuándo usarla:**
- Crear ilustraciones
- Generar diagramas
- Visualizaciones creativas

**Ejemplo:**
```python
from tools import create_drawing_tool

agent = Agent(
    name="Artista",
    instructions="Eres un artista digital. Puedes crear imágenes.",
    tools=[create_drawing_tool()]
)

response = agent.chat("Draw a sunset over mountains")
```

### 4. Custom Function (Función Personalizada)
Define tus propias funciones personalizadas.

**Ejemplo:**
```python
from tools import create_function_tool

weather_tool = create_function_tool(
    name="get_weather",
    description="Get the current weather in a location",
    parameters={
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit"
            }
        },
        "required": ["location"]
    }
)

agent = Agent(
    name="Weather Assistant",
    instructions="You provide weather information",
    tools=[weather_tool]
)
```

---

## 🎯 Cómo Usar Herramientas

### Método 1: Al Crear el Agente
```python
from agent_creator import Agent
from tools import create_web_search_tool

agent = Agent(
    name="Mi Agente",
    instructions="...",
    tools=[create_web_search_tool()]  # ← Aquí
)
```

### Método 2: Agregar Después
```python
agent = Agent(name="Mi Agente", instructions="...")

# Agregar herramienta
agent.add_tool(create_web_search_tool())
```

### Método 3: Múltiples Herramientas
```python
from tools import create_web_search_tool, create_code_interpreter_tool

agent = Agent(
    name="Super Agente",
    instructions="...",
    tools=[
        create_web_search_tool(),
        create_code_interpreter_tool()
    ]
)
```

---

## 🔄 Gestión de Herramientas

### Ver Herramientas Configuradas
```python
tools = agent.get_tools()
print(f"Herramientas: {len(tools)}")
for tool in tools:
    print(f"- {tool['type']}")
```

### Agregar Herramienta
```python
agent.add_tool(create_web_search_tool())
```

### Remover Herramienta
```python
agent.remove_tool('web_search')  # Por tipo
```

### Limpiar Todas las Herramientas
```python
agent.clear_tools()
```

---

## 💾 Persistencia

Las herramientas se guardan y cargan automáticamente:

```python
# Crear agente con herramientas
agent = Agent(
    name="Investigador",
    instructions="...",
    tools=[create_web_search_tool()]
)

# Guardar (incluye herramientas)
agent.save_agent("investigador.json")

# Cargar (restaura herramientas)
loaded = Agent.load_agent("investigador.json")
print(f"Herramientas restauradas: {len(loaded.get_tools())}")
```

---

## 🎨 Desde el Menú Interactivo

```bash
python agent_manager.py
```

1. Selecciona "1. Crear agente personalizado"
2. Ingresa nombre e instrucciones
3. Cuando pregunte "¿Agregar herramientas al agente? (s/n)": escribe **s**
4. Selecciona las herramientas por número (ej: 1,2)

---

## 📊 Ejemplos Prácticos

### Ejemplo 1: Investigador con Web Search
```python
from agent_creator import Agent
from tools import create_web_search_tool

researcher = Agent(
    name="Investigador Científico",
    instructions="""
    Eres un investigador científico experto.
    Usa búsqueda web para encontrar información actualizada.
    Siempre cita tus fuentes.
    """,
    tools=[create_web_search_tool()]
)

# Pregunta que requiere información actualizada
response = researcher.chat("What are the latest breakthroughs in quantum computing?")
print(response)
```

### Ejemplo 2: Analista de Datos con Code Interpreter
```python
from tools import create_code_interpreter_tool

analyst = Agent(
    name="Analista de Datos",
    instructions="""
    Eres un analista de datos experto en Python.
    Puedes ejecutar código para análisis y visualizaciones.
    Explica tu código claramente.
    """,
    tools=[create_code_interpreter_tool()]
)

response = analyst.chat("""
Analyze this data and create a visualization:
Sales: [100, 150, 200, 180, 220, 250]
Months: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
""")
```

### Ejemplo 3: Asistente Versátil con Múltiples Herramientas
```python
from tools import create_web_search_tool, create_code_interpreter_tool

assistant = Agent(
    name="Asistente Versátil",
    instructions="""
    Eres un asistente versátil que puede:
    - Buscar información en la web
    - Ejecutar código Python
    Elige la herramienta apropiada según la tarea.
    """,
    tools=[
        create_web_search_tool(),
        create_code_interpreter_tool()
    ]
)

# Esta pregunta puede usar ambas herramientas
response = assistant.chat("""
Find the current population of Japan and calculate 
what percentage it represents of the world population.
""")
```

---

## ⚙️ Configuración Avanzada

### Web Search con Query Específica
```python
from tools import create_web_search_tool

tool = create_web_search_tool(
    search_query="artificial intelligence 2024",
    enable_search_result=True
)
```

### Drawing Tool con Configuración
```python
from tools import create_drawing_tool

tool = create_drawing_tool(enable_generation=True)
```

---

## 🔍 Ver Herramientas en Chat

Cuando chateas con un agente que tiene herramientas:

```
=== Chat con Investigador ===
🔧 Herramientas: 1 configurada(s)
   - web_search

Escribe 'tools' para ver detalles de las herramientas
```

Comando **tools** muestra información detallada:
```
Tú: tools

=== Herramientas del Agente ===
1. Tipo: web_search
   Configuración: {'search_result': True}
```

---

## 💡 Mejores Prácticas

### 1. Instrucciones Claras
```python
# ❌ Mal
agent = Agent(
    name="Agent",
    instructions="You help users",
    tools=[create_web_search_tool()]
)

# ✅ Bien
agent = Agent(
    name="Research Agent",
    instructions="""
    You are a research assistant.
    Use web search to find accurate, up-to-date information.
    Always cite your sources and verify facts.
    """,
    tools=[create_web_search_tool()]
)
```

### 2. Herramientas Apropiadas
```python
# Para información actualizada → Web Search
# Para cálculos/código → Code Interpreter
# Para imágenes → Drawing Tool
```

### 3. Combinar Herramientas Estratégicamente
```python
# Agente que puede investigar Y analizar datos
data_researcher = Agent(
    name="Data Researcher",
    instructions="Research data online and analyze it with code",
    tools=[
        create_web_search_tool(),
        create_code_interpreter_tool()
    ]
)
```

---

## 🐛 Solución de Problemas

### Error: "Insufficient balance"
- Las herramientas consumen créditos adicionales
- Verifica tu saldo en https://z.ai/model-api

### Herramienta no se usa
- Asegúrate de que las instrucciones mencionen el uso de herramientas
- Verifica que la herramienta esté configurada: `agent.get_tools()`

### Herramientas no se guardan
- Usa `agent.save_agent()` después de configurar herramientas
- Verifica el archivo JSON generado

---

## 📚 Recursos

- **Demo completo**: `python demo_tools.py`
- **Herramientas disponibles**: `python tools.py`
- **Documentación Z.AI**: https://docs.z.ai/

---

## 🎯 Resumen Rápido

| Herramienta | Uso | Función |
|-------------|-----|---------|
| `create_web_search_tool()` | Información actualizada | Busca en internet |
| `create_code_interpreter_tool()` | Cálculos/código | Ejecuta Python |
| `create_drawing_tool()` | Imágenes | Genera visuales |
| `create_function_tool()` | Personalizado | Tu función |

**Comando rápido:**
```python
from agent_creator import Agent
from tools import create_web_search_tool

agent = Agent(
    name="Mi Agente",
    instructions="...",
    tools=[create_web_search_tool()]
)
```
