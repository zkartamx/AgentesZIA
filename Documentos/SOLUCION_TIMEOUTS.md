# Solución: Request Timeout

## ⚠️ Error: Request timed out

### Síntoma
```
Error: Request timed out.
```

### Causas Comunes

1. **API de Z.AI sobrecargada** - Demasiadas peticiones
2. **Herramientas lentas** - Web search o Selenium tardan mucho
3. **Conexión lenta** - Problemas de red
4. **DSPy procesando** - Decisión de herramientas toma tiempo

## ✅ Soluciones

### 1. Sistema de Reintentos (Ya Implementado)

El sistema ahora reintenta automáticamente 2 veces:

```python
# Ya está en agent_creator.py
max_retries = 2
for retry in range(max_retries):
    try:
        response = self.client.chat.completions.create(**request_params)
        break
    except Exception as e:
        if retry < max_retries - 1:
            print(f"\n⚠️  Reintentando... ({retry + 1}/{max_retries})")
            continue
```

### 2. Reducir Complejidad

**Opción A: Sin DSPy**

Si DSPy causa timeouts, desactívalo temporalmente:

```python
from agent_creator import Agent  # Sin DSPyAgent

agent = Agent(
    name="Simple Agent",
    instructions="...",
    tools=[...]
)

# Usar directamente sin DSPy
response = agent.chat("Tu pregunta")
```

**Opción B: Menos Herramientas**

```python
# ❌ Muchas herramientas
tools = [web_search, selenium, telegram, code, drawing]

# ✅ Solo las necesarias
tools = [web_search]
```

### 3. Aumentar Timeout

```python
# En agent_creator.py, puedes aumentar el timeout
response = agent.chat(
    "Tu pregunta",
    timeout=120  # 2 minutos en lugar de 60 segundos
)
```

### 4. Simplificar Instrucciones

```python
# ❌ Instrucciones muy largas
instructions = """
Eres un agente super complejo que hace mil cosas...
[500 líneas de instrucciones]
"""

# ✅ Instrucciones concisas
instructions = "Eres un investigador. Usa web_search para información actualizada."
```

### 5. Usar Modo Streaming

El modo streaming es más rápido:

```python
# En lugar de chat()
for chunk in agent.chat_stream("Tu pregunta"):
    print(chunk, end='', flush=True)
```

### 6. Verificar Conexión

```bash
# Test de conexión a Z.AI
curl -I https://api.z.ai

# Verificar latencia
ping api.z.ai
```

## 🔧 Configuración Recomendada

### Para Evitar Timeouts

```python
from agent_creator import Agent
from tools import create_web_search_tool

agent = Agent(
    name="Investigador",
    instructions="Eres un investigador. SIEMPRE usa web_search para información actualizada.",
    tools=[create_web_search_tool()],
    model="glm-4.6"  # Modelo más rápido
)

# Chat con configuración optimizada
response = agent.chat(
    message="Tu pregunta",
    temperature=0.7,
    max_tokens=1000,  # Menos tokens = más rápido
    timeout=90  # Timeout más largo
)
```

## 📊 Comparación de Velocidad

| Configuración | Tiempo Aprox. | Recomendado Para |
|---------------|---------------|------------------|
| Sin herramientas | ~2-5s | Conversación simple |
| Web Search | ~5-10s | Búsquedas |
| Selenium | ~10-20s | Scraping |
| DSPy + Tools | ~10-15s | Decisiones complejas |
| Múltiples tools | ~15-30s | Automatización completa |

## 🚨 Si Persiste el Error

### Opción 1: Modo Degradado

```python
try:
    response = agent.chat("Tu pregunta")
except Exception as e:
    if "timeout" in str(e).lower():
        # Reintentar sin herramientas
        agent_simple = Agent(
            name=agent.name,
            instructions=agent.instructions,
            tools=[]  # Sin herramientas
        )
        response = agent_simple.chat("Tu pregunta")
```

### Opción 2: Caché de Respuestas

```python
import json
from pathlib import Path

def chat_with_cache(agent, message):
    cache_file = Path("cache.json")
    
    # Cargar caché
    cache = {}
    if cache_file.exists():
        cache = json.loads(cache_file.read_text())
    
    # Verificar si está en caché
    if message in cache:
        return cache[message]
    
    # Obtener respuesta
    try:
        response = agent.chat(message)
        cache[message] = response
        cache_file.write_text(json.dumps(cache, indent=2))
        return response
    except Exception as e:
        return f"Error: {e}"
```

### Opción 3: Dividir en Pasos

```python
# ❌ Todo en una pregunta
"Busca el precio de Bitcoin, analiza la tendencia y envíamelo por Telegram"

# ✅ Paso a paso
response1 = agent.chat("Busca el precio de Bitcoin")
response2 = agent.chat("Analiza la tendencia")
response3 = agent.chat("Envíame el resumen por Telegram")
```

## 🔍 Debugging

### Ver Qué Está Tardando

```python
import time

start = time.time()
response = agent.chat("Tu pregunta")
elapsed = time.time() - start

print(f"Tiempo: {elapsed:.2f}s")
```

### Logs Detallados

```python
import logging

logging.basicConfig(level=logging.DEBUG)

# Ahora verás logs detallados
response = agent.chat("Tu pregunta")
```

## ⚡ Optimizaciones Aplicadas

### 1. Reintentos Automáticos
- 2 intentos por defecto
- Mensaje de reintento visible

### 2. Warning de DSPy Eliminado
- Cambio de `forward()` a `__call__()`
- Menos overhead

### 3. Timeout Configurable
- Default: 60 segundos
- Ajustable por llamada

## 📝 Checklist de Solución

- [ ] Verificar conexión a internet
- [ ] Reducir número de herramientas
- [ ] Simplificar instrucciones
- [ ] Aumentar timeout
- [ ] Probar sin DSPy
- [ ] Usar modo streaming
- [ ] Dividir en pasos más pequeños
- [ ] Verificar logs de error

## 🆘 Soporte

Si el problema persiste:

1. **Verifica el estado de Z.AI**: https://status.z.ai
2. **Revisa los logs**: Busca errores específicos
3. **Prueba con modelo más simple**: Cambia a modelo básico
4. **Contacta soporte**: support@z.ai

## ✅ Resumen

**Problema:** Request timeout  
**Causa:** API lenta, herramientas complejas, o DSPy  
**Solución:** Reintentos automáticos (ya implementado) + optimizaciones  
**Prevención:** Menos herramientas, instrucciones simples, timeout mayor
