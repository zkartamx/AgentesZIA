# Guía: Agentes con DSPy

## 🎯 ¿Qué es DSPy?

DSPy es un framework que mejora la toma de decisiones de los agentes mediante **programación declarativa** y **optimización automática**.

### Beneficios:
- ✅ **Mejor decisión de herramientas** - El agente decide más inteligentemente cuándo usar cada herramienta
- ✅ **Razonamiento explícito** - Puedes ver por qué el agente eligió usar una herramienta
- ✅ **Optimización automática** - DSPy puede mejorar las decisiones con el tiempo
- ✅ **Entrenado con ejemplos** - 13 ejemplos predefinidos para casos comunes

## 📚 Ejemplos de Entrenamiento

DSPy viene con **13 ejemplos** que enseñan al agente cuándo usar cada herramienta:

### Web Search (5 ejemplos):
- ✅ "¿Cuál es el precio actual de Bitcoin?" → Usar web_search
- ✅ "¿Qué pasó hoy en las noticias?" → Usar web_search
- ✅ "Busca información sobre IA" → Usar web_search
- ❌ "¿Qué es Python?" → NO usar (conocimiento general)
- ❌ "Explícame blockchain" → NO usar (concepto básico)

### Telegram (3 ejemplos):
- ✅ "Envíame un mensaje a Telegram" → Usar telegram
- ✅ "Notifícame cuando termines" → Usar telegram
- ✅ "¿Puedes enviarme eso por mensaje?" → Usar telegram

### Code Interpreter (3 ejemplos):
- ✅ "Calcula el factorial de 100" → Usar code
- ✅ "Analiza estos datos y crea un gráfico" → Usar code
- ❌ "¿Cuánto es 2+2?" → NO usar (cálculo simple)

### Múltiples Herramientas (2 ejemplos):
- ✅ "Busca Bitcoin y envíamelo" → Primero web_search, luego telegram
- ✅ "Investiga noticias y notifícame" → Primero web_search, luego telegram

**Ver todos los ejemplos:**
```bash
python dspy_examples.py
```

## 📦 Instalación

```bash
pip install -U dspy-ai
```

## 🚀 Uso Básico

### Opción 1: Crear Agente DSPy

```python
from dspy_agent import create_dspy_agent
from tools import create_web_search_tool, create_telegram_tool

# Crear agente mejorado con DSPy
agent = create_dspy_agent(
    name="Asistente Inteligente",
    instructions="Eres un asistente útil",
    tools=[
        create_web_search_tool(),
        create_telegram_tool()
    ]
)

# Usar normalmente
response = agent.chat("¿Cuál es el precio de Bitcoin?")
```

### Opción 2: Envolver Agente Existente

```python
from agent_creator import Agent
from dspy_agent import DSPyAgent
from tools import create_web_search_tool

# Crear agente normal
base_agent = Agent(
    name="Mi Agente",
    instructions="...",
    tools=[create_web_search_tool()]
)

# Envolver con DSPy
dspy_agent = DSPyAgent(base_agent)

# Ahora tiene mejor toma de decisiones
response = dspy_agent.chat("Busca información sobre IA")
```

## 🔍 Cómo Funciona

### Sin DSPy:
```
Usuario: "¿Cuál es el precio de Bitcoin?"
  ↓
Agente: Decide basándose solo en las instrucciones
  ↓
Puede o no usar web_search correctamente
```

### Con DSPy:
```
Usuario: "¿Cuál es el precio de Bitcoin?"
  ↓
DSPy analiza:
  - La pregunta del usuario
  - Las herramientas disponibles
  - El contexto de la conversación
  ↓
DSPy decide: "Usar web_search porque necesita datos actuales"
  ↓
Agente ejecuta web_search
  ↓
Respuesta con datos actualizados
```

## 📊 Ejemplo de Salida

```
🤖 DSPy Decision:
   Should use tool: True
   Tool: web_search
   Reasoning: El usuario está preguntando por el precio actual de Bitcoin.
              Esta es una información que cambia constantemente y requiere
              datos en tiempo real. La herramienta `web_search` es perfecta
              para esta tarea.
```

## 💡 Casos de Uso

### 1. Investigación con Web Search

```python
agent = create_dspy_agent(
    name="Investigador",
    instructions="Investiga temas usando web search",
    tools=[create_web_search_tool()]
)

# DSPy decidirá automáticamente usar web_search
response = agent.chat("¿Qué pasó hoy en el mundo?")
```

### 2. Notificaciones Inteligentes

```python
agent = create_dspy_agent(
    name="Monitor",
    instructions="Monitorea precios y notifica cambios importantes",
    tools=[
        create_web_search_tool(),
        create_telegram_tool()
    ]
)

# DSPy decidirá:
# 1. Usar web_search para obtener el precio
# 2. Usar telegram si el precio es importante
response = agent.chat("Monitorea el precio de Bitcoin y notifícame si supera $120,000")
```

### 3. Análisis con Código

```python
from tools import create_code_interpreter_tool

agent = create_dspy_agent(
    name="Analista",
    instructions="Analiza datos con código Python",
    tools=[create_code_interpreter_tool()]
)

# DSPy decidirá usar code_interpreter para cálculos
response = agent.chat("Calcula el factorial de 100")
```

## ⚙️ Configuración Avanzada

### Personalizar Decisiones

```python
from dspy_agent import DSPyAgent, ToolExecutor

class CustomToolExecutor(ToolExecutor):
    def forward(self, user_query, available_tools, context=""):
        # Tu lógica personalizada aquí
        decision = super().forward(user_query, available_tools, context)
        
        # Modificar decisión si es necesario
        if "urgente" in user_query.lower():
            decision['should_use_tool'] = True
            decision['tool_name'] = 'send_telegram_message'
        
        return decision

# Usar tu ejecutor personalizado
agent = DSPyAgent(base_agent)
agent.tool_executor = CustomToolExecutor()
```

## 🔧 Integración con Agent Manager

Puedes usar DSPy desde el menú interactivo modificando el código:

```python
# En agent_manager.py
from dspy_agent import DSPyAgent

# Cuando cargas un agente
agent = Agent.load_agent(str(agents[idx]))

# Envolver con DSPy
dspy_agent = DSPyAgent(agent)

# Usar normalmente
self.chat_with_agent(dspy_agent)
```

## 📈 Ventajas vs Desventajas

### ✅ Ventajas:
- Mejor toma de decisiones sobre herramientas
- Razonamiento explícito y transparente
- Fácil de integrar con agentes existentes
- Optimizable con ejemplos

### ⚠️ Desventajas:
- Requiere una llamada adicional al LLM (más lento)
- Consume más tokens
- Configuración inicial más compleja

## 🎯 Cuándo Usar DSPy

### Usa DSPy cuando:
- ✅ El agente tiene múltiples herramientas
- ✅ Necesitas decisiones más inteligentes
- ✅ Quieres ver el razonamiento del agente
- ✅ El costo extra de tokens no es problema

### No uses DSPy cuando:
- ❌ Solo tienes una herramienta simple
- ❌ La velocidad es crítica
- ❌ Quieres minimizar costos
- ❌ Las instrucciones simples funcionan bien

## 🐛 Solución de Problemas

### Error: "LLM Provider NOT provided"
```python
# Asegúrate de que ZAI_API_KEY esté en .env
# DSPy se configura automáticamente
```

### DSPy no mejora las decisiones
```python
# Verifica que las instrucciones sean claras
# Proporciona más contexto en las descripciones de herramientas
```

### Muy lento
```python
# DSPy hace una llamada extra al LLM
# Considera usar solo para casos complejos
```

## 📚 Recursos

- **Documentación DSPy**: https://dspy-docs.vercel.app/
- **GitHub**: https://github.com/stanfordnlp/dspy
- **Ejemplos**: `demos/` en este proyecto

## ✅ Resumen Rápido

```python
# 1. Instalar
pip install -U dspy-ai

# 2. Crear agente
from dspy_agent import create_dspy_agent
from tools import create_web_search_tool

agent = create_dspy_agent(
    name="Mi Agente",
    instructions="...",
    tools=[create_web_search_tool()]
)

# 3. Usar
response = agent.chat("Tu pregunta")

# 4. Ver decisión de DSPy en la salida
# 🤖 DSPy Decision: ...
```

DSPy hace que tus agentes sean más inteligentes en decidir cuándo y cómo usar sus herramientas. 🚀
