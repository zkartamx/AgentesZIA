# Demos y Pruebas

Esta carpeta contiene todos los archivos de demostración y pruebas del sistema de agentes.

## 📋 Índice de Demos

### 🔧 Herramientas (Tools)
- **`demo_tools.py`** - Demostración completa de herramientas
  - Web Search
  - Code Interpreter
  - Gestión dinámica de herramientas
  - Guardar/cargar agentes con herramientas

### 🗑️ Gestión de Agentes
- **`demo_delete.py`** - Demostración de eliminación de agentes
  - Crear agentes de prueba
  - Listar agentes
  - Eliminar agentes individuales
  - Eliminar todos los agentes

### ⠋ Indicadores de Carga
- **`demo_loading.py`** - Demostración del indicador de carga animado
  - Spinner mientras el agente procesa
  - Feedback visual

## 🧪 Pruebas (Tests)

### Pruebas Básicas
- **`test_zai.py`** - Test básico de conexión con Z.AI API
- **`test_agent.py`** - Test inicial de agentes (legacy)

### Pruebas de Web Search
- **`test_web_search.py`** - Test completo de búsqueda web
  - Verifica que web search funcione
  - Dos pruebas diferentes
  
- **`test_web_search_verification.py`** - Verificación de precisión
  - Compara con datos reales
  - Valida resultados de búsqueda

- **`test_btc.py`** - Test específico de precio de Bitcoin
  - Usa web search para obtener precio actual
  - Valida información financiera en tiempo real

## 🚀 Cómo Ejecutar

### Ejecutar todas las demos:
```bash
# Activar entorno virtual
source venv/bin/activate

# Demos
python demos/demo_tools.py
python demos/demo_delete.py
python demos/demo_loading.py

# Tests
python demos/test_web_search.py
python demos/test_btc.py
python demos/test_web_search_verification.py
```

### Ejecutar demo específica:
```bash
source venv/bin/activate
python demos/demo_tools.py
```

## 📝 Notas

- Todas las demos requieren que el entorno virtual esté activado
- Las demos de web search requieren saldo en la cuenta Z.AI
- Los tests pueden consumir créditos de la API

## 🔗 Archivos Relacionados

Los archivos principales del sistema están en el directorio raíz:
- `agent_creator.py` - Clase Agent principal
- `agent_manager.py` - Sistema de gestión interactivo
- `tools.py` - Módulo de herramientas
- `utils.py` - Utilidades (indicador de carga, etc.)
