# 📚 Documentación del Sistema de Agentes Z.AI

Índice completo de toda la documentación del proyecto.

## 🚀 Características

- **Creación de Agentes Personalizados**: Define agentes con nombres e instrucciones específicas
- **Agentes Predefinidos**: Math Tutor, Code Reviewer, Creative Writer
- **Herramientas (Tools)**: Web Search, Code Interpreter, Drawing Tool, Telegram (NUEVO)
- **Integración con Telegram**: Envía notificaciones y mensajes desde tus agentes
- **Gestión de Conversaciones**: Historial completo con contexto
- **Modo Streaming**: Respuestas en tiempo real
- **Indicador de Carga Animado**: Spinner visual mientras el agente procesa (⠋ Pensando...)
- **Persistencia**: Guarda y carga agentes desde archivos JSON
- **Interfaz Interactiva**: Sistema de menú fácil de usar

## 📋 Requisitos

- Python 3.13+
- Cuenta en Z.AI con saldo
- API Key de Z.AI

## 🔧 Instalación

1. **Crear entorno virtual**:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Instalar dependencias**:
```bash
pip install zai-sdk python-dotenv
```

3. **Configurar API Key**:
Crea un archivo `.env` en el directorio raíz:
```
ZAI_API_KEY=tu-api-key-aqui
```

## 📖 Uso

### Opción 1: Sistema Interactivo (Recomendado)

Ejecuta el gestor de agentes interactivo:

```bash
python agent_manager.py
```

Menú disponible:
- Crear agente personalizado
- Usar agente predefinido
- Cargar agente guardado
- Listar agentes guardados
- **Gestionar herramientas de agentes** (nuevo)
- **Eliminar agentes guardados**

### Opción 2: Uso Programático

```python
from agent_creator import Agent
from tools import create_web_search_tool

# Crear un agente simple
math_tutor = Agent(
    name="Math Tutor",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples"
)

# Crear un agente con herramientas
researcher = Agent(
    name="Researcher",
    instructions="You are a researcher. Use web search to find accurate information.",
    tools=[create_web_search_tool()]
)

# Chatear con el agente
response = math_tutor.chat("Can you help me solve this equation: 2x + 5 = 13?")
print(response)

# Seguimiento (mantiene contexto)
response = math_tutor.chat("Can you show me another example?")
print(response)
```

### Opción 3: Ver Ejemplos

Ejecuta los ejemplos predefinidos:

```bash
python example_agents.py
```

## 🎯 Ejemplos de Agentes

### Math Tutor
```python
math_tutor = Agent(
    name="Math Tutor",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples"
)
```

### Code Reviewer
```python
code_reviewer = Agent(
    name="Code Reviewer",
    instructions="You are an expert code reviewer. Analyze code for bugs, performance issues, and best practices."
)
```

### Custom Agent
```python
fitness_coach = Agent(
    name="Fitness Coach",
    instructions="You are a certified fitness coach. Provide workout advice, nutrition tips, and motivation."
)
```

## 🔥 Características Avanzadas

### Herramientas (Tools)
```python
from agent_creator import Agent
from tools import create_web_search_tool, create_code_interpreter_tool

# Agente con búsqueda web
researcher = Agent(
    name="Researcher",
    instructions="You research topics using web search",
    tools=[create_web_search_tool()]
)

# Agente con múltiples herramientas
super_agent = Agent(
    name="Super Agent",
    instructions="You can search the web and run code",
    tools=[
        create_web_search_tool(),
        create_code_interpreter_tool()
    ]
)

# Agregar herramientas dinámicamente
agent.add_tool(create_web_search_tool())
agent.remove_tool('web_search')
agent.clear_tools()
```

### Modo Streaming
```python
for chunk in agent.chat_stream("Tell me a story"):
    print(chunk, end="", flush=True)
```

### Guardar, Cargar y Eliminar Agentes
```python
# Guardar (incluye herramientas)
agent.save_agent("my_agent.json")

# Cargar (restaura herramientas)
loaded_agent = Agent.load_agent("my_agent.json")

# Eliminar
Agent.delete_agent("my_agent.json")
```

### Reiniciar Conversación
```python
agent.reset_conversation()
```

### Ver Historial
```python
history = agent.get_history()
for message in history:
    print(f"{message['role']}: {message['content']}")
```

## 📁 Estructura del Proyecto

```
Antes_OpenAI/
├── .env                    # API Key (no versionar)
├── agent_creator.py        # Clase Agent principal
├── agent_manager.py        # Sistema de gestión interactivo
├── tools.py               # Módulo de herramientas (web search, etc.)
├── utils.py               # Utilidades (indicador de carga, etc.)
├── example_agents.py       # Ejemplos de uso
├── quick_start.py         # Guía rápida
├── demos/                 # Demos y pruebas
│   ├── README.md         # Documentación de demos
│   ├── demo_tools.py     # Demo de herramientas
│   ├── demo_loading.py   # Demo de indicador de carga
│   ├── demo_delete.py    # Demo de eliminación
│   ├── test_*.py         # Archivos de prueba
│   └── ...
├── agents/                # Directorio de agentes guardados
│   └── *.json            # Archivos de configuración
└── README.md             # Esta documentación
```

## 🎨 API de la Clase Agent

### Constructor
```python
Agent(name: str, instructions: str, model: str = "glm-4.6")
```

### Métodos Principales

- `chat(message: str, temperature: float = 0.7, max_tokens: int = 2000) -> str`
  - Envía un mensaje y obtiene respuesta

- `chat_stream(message: str, temperature: float = 0.7, max_tokens: int = 2000)`
  - Respuesta en streaming (generador)

- `reset_conversation()`
  - Reinicia el historial manteniendo instrucciones

- `get_history() -> list`
  - Obtiene el historial completo

- `save_agent(filename: str)`
  - Guarda configuración en JSON

- `load_agent(filename: str)` (classmethod)
  - Carga agente desde JSON

- `delete_agent(filename: str)` (staticmethod)
  - Elimina un archivo de agente guardado

## 🔍 Parámetros de Chat

- **temperature** (0.0 - 1.0): Controla la creatividad
  - 0.0: Más determinista
  - 1.0: Más creativo
  
- **max_tokens**: Límite de tokens en la respuesta

## 💡 Consejos

1. **Instrucciones claras**: Define bien el rol y comportamiento del agente
2. **Contexto**: Los agentes mantienen historial de conversación
3. **Reset cuando sea necesario**: Usa `reset_conversation()` para empezar de nuevo
4. **Guarda agentes útiles**: Usa `save_agent()` para reutilizar configuraciones
5. **Experimenta con temperature**: Ajusta según necesites creatividad o precisión

## 🐛 Solución de Problemas

### Error: "Insufficient balance"
- Recarga saldo en https://z.ai/model-api

### Error: API Key inválida
- Verifica que `.env` contenga `ZAI_API_KEY=tu-clave`
- Obtén una nueva clave en https://z.ai/manage-apikey/apikey-list

### Error: ModuleNotFoundError
- Asegúrate de activar el entorno virtual: `source venv/bin/activate`
- Instala dependencias: `pip install zai-sdk python-dotenv`

## 📚 Recursos

- [Documentación Z.AI](https://docs.z.ai/guides/develop/python/introduction)
- [Z.AI Open Platform](https://z.ai/model-api)
- [Gestión de API Keys](https://z.ai/manage-apikey/apikey-list)

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
