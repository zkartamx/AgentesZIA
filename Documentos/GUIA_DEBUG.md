# Guía: Sistema de Debug

## 🐛 Activar Debug

### Opción 1: Desde el Menú

```bash
python agent_manager.py
# Opción 7: Configurar Debug
# Selecciona nivel: 1 (Básico), 2 (Detallado), 3 (Verbose)
```

### Opción 2: Variable de Entorno

```bash
# Activar debug básico
export DEBUG_LEVEL=1
python agent_manager.py

# O en una línea
DEBUG_LEVEL=1 python agent_manager.py
```

### Opción 3: En Código

```python
from debug_config import DebugConfig, DebugLevel

# Activar debug básico
DebugConfig.set_level(DebugLevel.BASIC)

# Usar agente normalmente
agent.chat("Tu pregunta")
```

## 📊 Niveles de Debug

### 0. NONE (Desactivado)
Sin mensajes de debug.

### 1. BASIC (Básico)
Muestra:
- ✅ Decisiones de DSPy
- ✅ Tool calls ejecutados
- ✅ Reintentos

**Ejemplo:**
```
🤖 DSPy Decision:
   Should use tool: True
   Tool: web_search
   Reasoning: Usuario pide información actualizada

[DEBUG] 🔧 Ejecutando: web_search
[DEBUG]    Argumentos: {'query': 'Bitcoin price'}
[DEBUG]    Resultado: {'success': True, ...}
```

### 2. DETAILED (Detallado)
Todo lo de BASIC +
- ✅ Historial de conversación

**Ejemplo:**
```
[DEBUG] === HISTORIAL ===
[DEBUG] system: Eres un investigador...
[DEBUG] user: Busca el precio de Bitcoin
[DEBUG] assistant: El precio actual es...
```

### 3. VERBOSE (Todo)
Todo lo de DETAILED +
- ✅ Instrucciones completas
- ✅ Llamadas a API

**Ejemplo:**
```
[DEBUG] === INSTRUCCIONES COMPLETAS ===
Eres un investigador web experto...

=== HERRAMIENTAS DISPONIBLES ===
• WEB SEARCH: Puedes buscar...
```

## 🎯 Casos de Uso

### Ver por qué no usa herramientas

```bash
DEBUG_LEVEL=1 python agent_manager.py
```

Verás:
```
🤖 DSPy Decision:
   Should use tool: False
   Tool: none
   Reasoning: Pregunta conceptual, no requiere búsqueda
```

### Debugear timeouts

```bash
DEBUG_LEVEL=1 python agent_manager.py
```

Verás los reintentos:
```
⚠️  Reintentando... (1/2)
```

### Ver qué herramientas se ejecutan

```bash
DEBUG_LEVEL=1 python agent_manager.py
```

Verás:
```
[DEBUG] 🔧 Ejecutando: web_search
[DEBUG]    Argumentos: {'query': 'Bitcoin'}
[DEBUG]    Resultado: {'success': True}
```

## 🔧 Configuración Avanzada

### Flags Individuales

```python
from debug_config import DebugConfig

# Activar solo DSPy decisions
DebugConfig.show_dspy_decisions = True
DebugConfig.show_tool_calls = False
DebugConfig.show_history = False
```

### En .env

```bash
# Agregar a .env
DEBUG_LEVEL=1
```

Luego:
```python
from debug_config import DebugConfig

# Se configura automáticamente desde .env
DebugConfig.from_env()
```

## 📝 Ejemplo Completo

```python
from agent_creator import Agent
from tools import create_web_search_tool
from debug_config import DebugConfig, DebugLevel

# Activar debug
DebugConfig.set_level(DebugLevel.BASIC)

# Crear agente
agent = Agent(
    name="Investigador",
    instructions="Eres un investigador",
    tools=[create_web_search_tool()]
)

# Chatear (verás debug info)
response = agent.chat("Busca el precio de Bitcoin")

# Ver estado de debug
DebugConfig.print_status()
```

## 🎨 Output Esperado

### Con DEBUG_LEVEL=1 (BASIC)

```
🐛 DEBUG: BASIC

=== Menú Principal ===
...

Usuario: Busca el precio de Bitcoin

🤖 DSPy Decision:
   Should use tool: True
   Tool: web_search
   Reasoning: Usuario pide precio actual, requiere web_search

[DEBUG] Usuario: Busca el precio de Bitcoin
[DEBUG] 🔧 Ejecutando: web_search
[DEBUG]    Argumentos: {'query': 'Bitcoin price'}
[DEBUG]    Resultado: {'success': True}

Agente: El precio actual de Bitcoin es...
```

### Con DEBUG_LEVEL=0 (NONE)

```
=== Menú Principal ===
...

Usuario: Busca el precio de Bitcoin

Agente: El precio actual de Bitcoin es...
```

## ⚡ Tips

1. **Usa BASIC para uso normal** - Suficiente para ver qué pasa
2. **Usa DETAILED para debugging** - Cuando algo no funciona
3. **Usa VERBOSE solo si necesitas todo** - Mucha información
4. **Desactiva en producción** - DEBUG_LEVEL=0

## 🔍 Troubleshooting

### No veo mensajes de debug

```python
# Verificar nivel
from debug_config import DebugConfig
DebugConfig.print_status()
```

### Demasiados mensajes

```python
# Bajar nivel
DebugConfig.set_level(DebugLevel.BASIC)
```

### Solo quiero ver DSPy

```python
DebugConfig.show_dspy_decisions = True
DebugConfig.show_tool_calls = False
DebugConfig.show_history = False
```

## ✅ Resumen

**Activar:** `DEBUG_LEVEL=1 python agent_manager.py`  
**Niveles:** 0=OFF, 1=BASIC, 2=DETAILED, 3=VERBOSE  
**Uso:** Ver decisiones de DSPy y tool calls  
**Desactivar:** `DEBUG_LEVEL=0` o Opción 7 → 0
