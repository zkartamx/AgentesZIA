# Guía: Evaluación de DSPy

## 🎯 ¿Cómo Evaluar que DSPy Funciona Correctamente?

### Sistema de Evaluación Automática

Hemos implementado un evaluador que verifica que DSPy tome las decisiones correctas comparando con ejemplos conocidos.

## 🚀 Ejecutar Evaluación

```bash
python dspy_evaluator.py
```

## 📊 Qué Evalúa

### 1. **Precisión de Herramienta**
Verifica que DSPy elija la herramienta correcta:
- ✅ "¿Precio de Bitcoin?" → `web_search` ✓
- ✅ "Envíame un mensaje" → `send_telegram_message` ✓
- ✅ "¿Qué es Python?" → `none` (no usar herramienta) ✓

### 2. **Precisión de Decisión**
Verifica que DSPy decida correctamente cuándo usar o no usar herramientas:
- ✅ Usar herramienta cuando es necesario
- ✅ NO usar herramienta cuando no es necesario

## 📈 Métricas

### Resultado Actual:
```
📊 Métricas Generales:
   Total de ejemplos: 13
   Herramientas correctas: 13/13
   Decisiones correctas: 13/13

   🎯 Precisión (Herramienta): 100.0%
   🎯 Precisión (Decisión): 100.0%

✅ EXCELENTE - DSPy está funcionando muy bien
```

### Interpretación:

| Precisión | Evaluación | Acción |
|-----------|------------|--------|
| **90-100%** | ✅ Excelente | DSPy funciona perfectamente |
| **70-89%** | ⚠️ Bueno | Funciona pero puede mejorar |
| **<70%** | ❌ Necesita mejora | Revisar ejemplos o configuración |

## 🔍 Evaluación Detallada

### Ver Todos los Casos

El evaluador prueba cada ejemplo y muestra:
```
[1/13] Evaluando: ¿Cuál es el precio actual de Bitcoin?...
    ✅ Correcto
    
[4/13] Evaluando: ¿Qué es Python?...
    ✅ Correcto (decidió NO usar herramienta)
```

### Ver Errores

Si hay errores, se muestran así:
```
❌ Errores (2):

   Query: ¿Cuál es el precio de Bitcoin?
   Esperado: web_search
   Obtenido: none
   
   Query: Envíame un mensaje
   Esperado: send_telegram_message
   Obtenido: web_search
```

## 🧪 Tipos de Evaluación

### 1. Evaluación Completa (Por Defecto)

```python
from dspy_evaluator import DSPyEvaluator

evaluator = DSPyEvaluator()
metrics = evaluator.evaluate_all()
evaluator.print_report(metrics)
```

### 2. Evaluación por Categoría

```python
evaluator.evaluate_by_category()
```

Evalúa cada tipo de herramienta por separado:
- Web Search
- Telegram
- Code Interpreter
- Múltiples herramientas

### 3. Test con Agente Real

Prueba con un agente real (sin ejecutar para no consumir créditos):

```python
from dspy_evaluator import test_live_agent

test_live_agent()
```

## 📝 Agregar Tus Propios Tests

### En `dspy_examples.py`:

```python
# Agregar nuevo ejemplo
my_test = dspy.Example(
    user_query="Tu pregunta de prueba",
    available_tools="web_search: Busca información",
    conversation_context="Sin contexto previo",
    should_use_tool="yes",  # o "no"
    tool_name="web_search",  # o "none"
    reasoning="Por qué debe usar esta herramienta"
).with_inputs("user_query", "available_tools", "conversation_context")

# Agregar a la lista
WEB_SEARCH_EXAMPLES.append(my_test)
```

### Ejecutar evaluación de nuevo:

```bash
python dspy_evaluator.py
```

## 🎯 Casos de Prueba Incluidos

### Web Search (5 casos):
1. ✅ Precio actual de Bitcoin → Usar
2. ✅ Noticias de hoy → Usar
3. ✅ "Busca información..." → Usar
4. ❌ "¿Qué es Python?" → NO usar
5. ❌ "Explica blockchain" → NO usar

### Telegram (3 casos):
1. ✅ "Envíame un mensaje" → Usar
2. ✅ "Notifícame" → Usar
3. ✅ "Envíame eso por mensaje" → Usar

### Code Interpreter (3 casos):
1. ✅ Factorial de 100 → Usar
2. ✅ Analizar datos → Usar
3. ❌ "2+2" → NO usar

### Multi-herramienta (2 casos):
1. ✅ "Busca y envíame" → Primero web_search
2. ✅ "Investiga y notifica" → Primero web_search

## 🔧 Solución de Problemas

### Precisión Baja

**Problema:** Precisión < 70%

**Soluciones:**
1. Revisar que ZAI_API_KEY esté configurada
2. Verificar que DSPy esté configurado correctamente
3. Agregar más ejemplos de entrenamiento
4. Mejorar las descripciones de herramientas

### Errores en Ejemplos Específicos

**Problema:** Algunos ejemplos fallan consistentemente

**Soluciones:**
1. Revisar el razonamiento en el ejemplo
2. Hacer la descripción de la herramienta más clara
3. Agregar ejemplos similares para reforzar el patrón

### DSPy No Mejora con Ejemplos

**Problema:** Misma precisión con o sin ejemplos

**Soluciones:**
1. Verificar que `use_examples=True` en ToolExecutor
2. Confirmar que los ejemplos se cargaron: ver mensaje "✓ X ejemplos cargados"
3. Revisar que los ejemplos sean relevantes

## 📊 Monitoreo Continuo

### Evaluar Regularmente

Ejecuta la evaluación después de:
- ✅ Agregar nuevos ejemplos
- ✅ Cambiar descripciones de herramientas
- ✅ Modificar instrucciones de agentes
- ✅ Actualizar DSPy

### Benchmark

Guarda los resultados para comparar:

```bash
python dspy_evaluator.py > evaluation_results.txt
```

## ✅ Checklist de Evaluación

- [ ] Ejecutar `python dspy_evaluator.py`
- [ ] Verificar precisión ≥ 90%
- [ ] Revisar que no haya errores
- [ ] Probar con casos reales
- [ ] Documentar resultados
- [ ] Agregar nuevos casos si es necesario

## 🎓 Mejores Prácticas

### 1. Evaluar Antes de Producción
Siempre ejecuta la evaluación antes de usar DSPy en producción.

### 2. Mantener Ejemplos Actualizados
Agrega ejemplos para nuevos casos de uso que encuentres.

### 3. Monitorear en Producción
Registra las decisiones de DSPy en producción para detectar problemas.

### 4. Iterar y Mejorar
Usa los errores para crear nuevos ejemplos de entrenamiento.

## 📚 Recursos

- **Evaluador**: `dspy_evaluator.py`
- **Ejemplos**: `dspy_examples.py`
- **Documentación DSPy**: https://dspy-docs.vercel.app/

## ✅ Resumen

```bash
# 1. Ejecutar evaluación
python dspy_evaluator.py

# 2. Ver resultados
# Precisión: 100.0% ✅

# 3. Si hay errores, revisar y agregar ejemplos

# 4. Re-evaluar
python dspy_evaluator.py
```

**DSPy está funcionando al 100% con los 13 ejemplos de entrenamiento.** 🎉
