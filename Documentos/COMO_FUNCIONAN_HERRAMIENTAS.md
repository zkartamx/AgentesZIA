# Cómo Funcionan las Herramientas en los Agentes

## 🤔 ¿Cómo Sabe el Agente Qué Herramientas Tiene?

### Sistema Automático de Instrucciones

Cuando creas un agente con herramientas, el sistema **automáticamente** agrega información sobre las herramientas disponibles a las instrucciones del agente.

## 📋 Ejemplo

### Código:
```python
from agent_creator import Agent
from tools import create_web_search_tool, create_telegram_tool

agent = Agent(
    name="Asistente",
    instructions="Eres un asistente útil.",
    tools=[
        create_web_search_tool(),
        create_telegram_tool()
    ]
)
```

### Lo que recibe el agente internamente:
```
Eres un asistente útil.

=== HERRAMIENTAS DISPONIBLES ===
Tienes acceso a las siguientes herramientas:

• WEB SEARCH: Puedes buscar información actualizada en internet.
  Úsala cuando necesites datos actuales, noticias, precios, o información que cambia frecuentemente.

• SEND_TELEGRAM_MESSAGE: Envía un mensaje a través de un bot de Telegram
  Úsala cuando el usuario te lo solicite explícitamente.

IMPORTANTE: Usa las herramientas apropiadas según la tarea. Si no estás seguro, pregunta al usuario.
```

## 🔄 Actualización Automática

Cuando agregas o quitas herramientas, las instrucciones se actualizan automáticamente:

```python
# Crear agente sin herramientas
agent = Agent(name="Test", instructions="Eres útil")

# Agregar herramienta
agent.add_tool(create_web_search_tool())
# ✅ Las instrucciones se actualizan automáticamente

# Remover herramienta
agent.remove_tool('web_search')
# ✅ Las instrucciones se actualizan automáticamente
```

## 🎯 Cómo Decide el Agente Usar una Herramienta

El agente decide usar una herramienta basándose en:

### 1. **Las instrucciones del sistema**
```python
Agent(
    name="Investigador",
    instructions="Eres un investigador. SIEMPRE usa web search para obtener información actualizada.",
    tools=[create_web_search_tool()]
)
```

### 2. **La pregunta del usuario**
```python
# Pregunta que sugiere usar web search
"¿Cuál es el precio actual de Bitcoin?"

# Pregunta que sugiere usar Telegram
"Envíame un mensaje a Telegram con el resumen"
```

### 3. **La descripción de la herramienta**
Cada herramienta tiene una descripción que ayuda al modelo a decidir:
```python
{
    'type': 'function',
    'function': {
        'name': 'send_telegram_message',
        'description': 'Envía un mensaje a través de un bot de Telegram',  # ← Esto ayuda
        'parameters': {...}
    }
}
```

## 💡 Mejores Prácticas

### ✅ Buenas Instrucciones

```python
Agent(
    name="Monitor de Precios",
    instructions="""
    Eres un monitor de precios de criptomonedas.
    
    SIEMPRE usa web search para obtener precios actuales.
    Si el precio es importante, envía una notificación a Telegram.
    """,
    tools=[
        create_web_search_tool(),
        create_telegram_tool()
    ]
)
```

### ❌ Instrucciones Vagas

```python
Agent(
    name="Asistente",
    instructions="Eres útil",  # ← Muy vago
    tools=[create_web_search_tool()]
)
```

## 🔍 Verificar las Instrucciones

Puedes ver las instrucciones completas que recibe el agente:

```python
agent = Agent(
    name="Test",
    instructions="Eres útil",
    tools=[create_web_search_tool()]
)

# Ver las instrucciones completas
print(agent.conversation_history[0]['content'])
```

## 📊 Flujo Completo

```
1. Creas el agente con herramientas
   ↓
2. Sistema genera instrucciones automáticas
   ↓
3. Usuario hace una pregunta
   ↓
4. Agente analiza:
   - Sus instrucciones (incluyendo info de herramientas)
   - La pregunta del usuario
   - Las descripciones de herramientas
   ↓
5. Agente decide si usar herramientas
   ↓
6. Si decide usar una herramienta:
   - Z.AI ejecuta la herramienta
   - Devuelve los resultados al agente
   - Agente formula la respuesta final
```

## ⚙️ Configuración Técnica

### Web Search
```python
create_web_search_tool(
    count=5,                           # Número de resultados
    search_recency_filter="oneWeek",   # Filtro de tiempo
    content_size="high"                # Tamaño del contenido
)
```

### Telegram
```python
create_telegram_tool()
# Requiere: TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID en .env
```

### Code Interpreter
```python
create_code_interpreter_tool()
# Permite ejecutar código Python
```

## 🐛 Solución de Problemas

### Problema: El agente no usa las herramientas

**Soluciones:**
1. **Instrucciones más explícitas**
   ```python
   instructions="SIEMPRE usa web search para información actualizada"
   ```

2. **Preguntas más claras**
   ```python
   # ❌ Vago
   "Dime sobre Bitcoin"
   
   # ✅ Claro
   "Busca el precio actual de Bitcoin"
   ```

3. **Verificar que las herramientas estén configuradas**
   ```python
   print(f"Herramientas: {agent.get_tools()}")
   ```

### Problema: Herramientas duplicadas

Si ves múltiples "function", usa el comando `tools` en el chat:
```
Tú: tools

=== Herramientas del Agente ===

1. Tipo: web_search
   Motor: search-prime

2. Tipo: function
   Nombre: send_telegram_message
   Descripción: Envía un mensaje a Telegram
```

## 📚 Recursos

- `demos/test_tool_awareness.py` - Ver cómo el agente conoce sus herramientas
- `GUIA_HERRAMIENTAS.md` - Guía completa de herramientas
- `GUIA_TELEGRAM.md` - Guía de Telegram
- Documentación Z.AI: https://docs.z.ai/

## ✅ Resumen

1. ✅ El agente **SÍ sabe** qué herramientas tiene (automáticamente)
2. ✅ Las instrucciones se actualizan cuando agregas/quitas herramientas
3. ✅ El agente decide cuándo usar cada herramienta
4. ✅ Instrucciones claras = Mejor uso de herramientas
