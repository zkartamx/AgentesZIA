# DSPy Integrado en Agent Manager

## ✅ DSPy Ahora Está Integrado Automáticamente

**DSPy se activa automáticamente** cuando cargas o creas un agente con herramientas.

## 🎯 Cómo Funciona

### Al Cargar un Agente

```bash
python agent_manager.py
# Opción 3: Cargar agente guardado
# Selecciona "Investigador web"
```

**Salida:**
```
✓ Agente 'Investigador web' cargado!
🤖 DSPy activado para mejor uso de herramientas
```

DSPy se activa automáticamente porque el agente tiene herramientas configuradas.

### Al Crear un Agente

```bash
python agent_manager.py
# Opción 1: Crear agente personalizado
# Agregar herramientas: s
```

**Salida:**
```
✓ Agente 'Mi Agente' creado exitosamente!
✓ Herramientas configuradas: 2
🤖 DSPy activado para mejor uso de herramientas
```

## 🔍 Qué Hace DSPy

DSPy analiza cada pregunta del usuario y decide inteligentemente:
- ✅ Si debe usar una herramienta
- ✅ Cuál herramienta usar
- ✅ Por qué usar esa herramienta

**Sin DSPy:**
```
Usuario: Busca el precio de Bitcoin
Agente: No tengo acceso a herramientas... ❌
```

**Con DSPy:**
```
Usuario: Busca el precio de Bitcoin
DSPy: [Decide usar web_search]
Agente: El precio actual de Bitcoin es $118,640 ✅
```

## 🎛️ Modo Debug

Si quieres ver las decisiones de DSPy, activa el modo debug:

```python
from agent_creator import Agent
from dspy_agent import DSPyAgent

agent = Agent.load_agent("agents/investigador_web.json")
dspy_agent = DSPyAgent(agent, debug=True)  # ← Debug activado

response = dspy_agent.chat("Busca el precio de Bitcoin")
```

**Salida con debug:**
```
🤖 DSPy Decision:
   Should use tool: True
   Tool: web_search
   Reasoning: Usuario pide buscar precio actual, requiere web_search
```

## 📋 Cuándo Se Activa DSPy

| Situación | DSPy Activado | Razón |
|-----------|---------------|-------|
| Agente con herramientas | ✅ Sí | Necesita decidir cuándo usarlas |
| Agente sin herramientas | ❌ No | No hay herramientas que decidir |
| Crear agente con tools | ✅ Sí | Automático |
| Cargar agente con tools | ✅ Sí | Automático |

## 🚀 Ejemplos de Uso

### Ejemplo 1: Investigador Web

```bash
python agent_manager.py
# Opción 3: Cargar agente guardado
# Selecciona "Investigador web"
```

```
Tú: Busca las mejores canciones de 2024
```

**DSPy decide:** Usar web_search  
**Resultado:** Lista de canciones actualizadas ✅

### Ejemplo 2: Buscar y Notificar

```
Tú: Busca el precio de Bitcoin y envíamelo por Telegram
```

**DSPy decide:**
1. Primero: Usar web_search (obtener precio)
2. Segundo: Usar send_telegram_message (enviar)

**Resultado:** Precio buscado y enviado ✅

## ⚙️ Configuración

DSPy se configura automáticamente con:
- **Modelo:** GLM-4.6 (Z.AI)
- **Ejemplos:** 13 casos de entrenamiento
- **API:** Z.AI (usa tu ZAI_API_KEY)

No necesitas configurar nada, funciona automáticamente.

## 📊 Precisión

DSPy ha sido evaluado con 13 ejemplos:

```
🎯 Precisión (Herramienta): 100.0%
🎯 Precisión (Decisión): 100.0%

✅ EXCELENTE - DSPy está funcionando muy bien
```

Ver evaluación completa: `python dspy_evaluator.py`

## 🔧 Solución de Problemas

### DSPy No Se Activa

**Problema:** No ves el mensaje "🤖 DSPy activado"

**Causa:** El agente no tiene herramientas configuradas

**Solución:**
```bash
python agent_manager.py
# Opción 5: Gestionar herramientas de agentes
# Agrega web_search o telegram
```

### Error al Cargar Agente

**Problema:** Error al cargar agente con DSPy

**Solución:**
1. Verifica que `dspy-ai` esté instalado: `pip install -U dspy-ai`
2. Verifica que `ZAI_API_KEY` esté en `.env`
3. Ejecuta `python fix_agents.py` para arreglar agentes

### Agente Aún No Usa Herramientas

**Problema:** Incluso con DSPy, el agente no usa herramientas

**Solución:**
1. Verifica que web_search tenga `enable: "True"`
2. Ejecuta `python fix_agents.py`
3. Verifica con `python dspy_evaluator.py`

## 📚 Archivos Relacionados

- **`agent_manager.py`** - Integración de DSPy
- **`dspy_agent.py`** - Implementación de DSPy
- **`dspy_examples.py`** - 13 ejemplos de entrenamiento
- **`dspy_evaluator.py`** - Sistema de evaluación
- **`GUIA_DSPY.md`** - Guía completa de DSPy

## ✅ Resumen

1. **DSPy se activa automáticamente** cuando cargas/creas agentes con herramientas
2. **No necesitas configurar nada** - funciona out-of-the-box
3. **Mejora las decisiones** - el agente usa herramientas correctamente
4. **100% de precisión** - evaluado con 13 casos de prueba
5. **Modo silencioso** - no muestra decisiones (usa `debug=True` si quieres verlas)

**Ahora todos tus agentes con herramientas usan DSPy automáticamente!** 🎉
