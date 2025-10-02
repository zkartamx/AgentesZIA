# Solución: Agente No Usa Web Search

## 🐛 Problema

El agente dice "No tengo acceso a herramientas de búsqueda web" aunque tiene `web_search` configurada.

```
Usuario: Busca las mejores canciones de 2025
Agente: No tengo acceso a herramientas de búsqueda web en este momento...
```

## 🔍 Causas

### 1. Configuración Antigua de Web Search
**Problema:** El agente tiene configuración antigua sin `enable` y `search_engine`.

**Solución:** Ejecutar `python fix_agents.py` para actualizar todos los agentes.

### 2. Instrucciones Débiles
**Problema:** Las instrucciones no mencionan explícitamente el uso de web_search.

**Antes:**
```json
{
  "instructions": "eres un investigador web que utiliza la herramienta de busqueda."
}
```

**Después:**
```json
{
  "instructions": "Eres un investigador web experto. SIEMPRE usa la herramienta web_search para buscar información actualizada. Cuando el usuario te pida buscar algo o necesites datos actuales, usa web_search sin dudar."
}
```

### 3. Instrucciones Automáticas No Se Cargan
**Problema:** Cuando cargas un agente guardado, las instrucciones sobre herramientas no se regeneran.

**Solución:** Ya implementada en `agent_creator.py` - se generan automáticamente al cargar.

## ✅ Soluciones Aplicadas

### 1. Arreglar Agentes Existentes

```bash
python fix_agents.py
```

Esto actualiza:
- ✅ Configuración de web_search al formato correcto
- ✅ Mejora las instrucciones para mencionar web_search

### 2. Crear Nuevos Agentes Correctamente

```python
from agent_creator import Agent
from tools import create_web_search_tool

agent = Agent(
    name="Investigador",
    instructions="""
    Eres un investigador experto.
    
    IMPORTANTE: SIEMPRE usa web_search cuando:
    - El usuario pida buscar información
    - Necesites datos actuales (precios, noticias, etc.)
    - La información pueda haber cambiado recientemente
    
    NO dudes en usar web_search. Es tu herramienta principal.
    """,
    tools=[create_web_search_tool()]
)
```

### 3. Usar DSPy (Recomendado)

DSPy ayuda al agente a decidir mejor cuándo usar herramientas:

```python
from dspy_agent import create_dspy_agent
from tools import create_web_search_tool

agent = create_dspy_agent(
    name="Investigador",
    instructions="Eres un investigador",
    tools=[create_web_search_tool()]
)

# DSPy decide automáticamente usar web_search
response = agent.chat("Busca las mejores canciones de 2024")
```

## 🎯 Mejores Prácticas

### ✅ Instrucciones Fuertes

```python
instructions = """
Eres un investigador web experto.

HERRAMIENTAS DISPONIBLES:
- web_search: ÚSALA SIEMPRE para información actualizada

REGLAS:
1. Si el usuario dice "busca", usa web_search
2. Si necesitas precios/noticias/datos actuales, usa web_search
3. NO digas "no tengo acceso" - SÍ tienes web_search
4. Usa web_search primero, pregunta después
"""
```

### ❌ Instrucciones Débiles

```python
instructions = "eres un investigador web"  # Muy vago
```

## 🧪 Verificar que Funciona

### Test Rápido

```bash
python agent_manager.py
# Opción 3: Cargar agente guardado
# Selecciona "Investigador web"
# Prueba: "Busca el precio de Bitcoin"
```

**Resultado esperado:**
- ✅ El agente usa web_search
- ✅ Devuelve precio actualizado
- ✅ NO dice "no tengo acceso"

### Test con DSPy

```bash
python dspy_agent.py
```

**Resultado esperado:**
```
🤖 DSPy Decision:
   Should use tool: True
   Tool: web_search
   Reasoning: Usuario pide buscar información actualizada...
```

## 📋 Checklist de Solución

- [ ] Ejecutar `python fix_agents.py`
- [ ] Verificar que web_search tenga `enable: "True"`
- [ ] Mejorar instrucciones del agente
- [ ] Probar con "Busca el precio de Bitcoin"
- [ ] Verificar que NO diga "no tengo acceso"
- [ ] Considerar usar DSPy para mejores decisiones

## 🔧 Comandos Útiles

```bash
# 1. Arreglar todos los agentes
python fix_agents.py

# 2. Verificar configuración de un agente
cat agents/investigador_web.json

# 3. Probar con DSPy
python dspy_agent.py

# 4. Evaluar DSPy
python dspy_evaluator.py
```

## ✅ Resumen

**Problema:** Agente no usa web_search  
**Causa:** Configuración antigua + instrucciones débiles  
**Solución:** `python fix_agents.py` + instrucciones fuertes + DSPy  
**Resultado:** Agente usa web_search correctamente ✅
