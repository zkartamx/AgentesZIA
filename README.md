# Sistema de Agentes con Z.AI

Sistema completo para crear, gestionar y chatear con agentes de IA personalizados usando la API de Z.AI.

## 🚀 Inicio Rápido

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd Antes_OpenAI

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar API Key
echo "ZAI_API_KEY=tu_api_key_aqui" > .env

# 5. Ejecutar
python agent_manager.py
```

## 📚 Documentación

**Toda la documentación está en la carpeta [`Documentos/`](Documentos/)**

### 📖 Documentos Principales

- **[Documentos/INDEX.md](Documentos/INDEX.md)** - 📑 Índice completo de documentación
- **[Documentos/README.md](Documentos/README.md)** - 📘 Documentación principal
- **[Documentos/RESUMEN_FUNCIONALIDADES.md](Documentos/RESUMEN_FUNCIONALIDADES.md)** - ✨ Resumen de funcionalidades

### 🔧 Guías de Herramientas

- **[Documentos/GUIA_HERRAMIENTAS.md](Documentos/GUIA_HERRAMIENTAS.md)** - Todas las herramientas
- **[Documentos/GUIA_TELEGRAM.md](Documentos/GUIA_TELEGRAM.md)** - Integración con Telegram

### 🤖 DSPy (Optimización)

- **[Documentos/GUIA_DSPY.md](Documentos/GUIA_DSPY.md)** - Guía de DSPy
- **[Documentos/DSPY_INTEGRADO.md](Documentos/DSPY_INTEGRADO.md)** - DSPy integrado
- **[Documentos/GUIA_EVALUACION_DSPY.md](Documentos/GUIA_EVALUACION_DSPY.md)** - Evaluación

### 🐛 Solución de Problemas

- **[Documentos/SOLUCION_WEB_SEARCH.md](Documentos/SOLUCION_WEB_SEARCH.md)** - Web Search no funciona

## ✨ Características

- ✅ **Agentes Personalizados** - Crea agentes con instrucciones específicas
- ✅ **Herramientas Integradas** - Web Search, Telegram, Code Interpreter, Drawing Tool
- ✅ **DSPy Automático** - Optimización inteligente de decisiones
- ✅ **Gestión Completa** - Crear, guardar, cargar, eliminar agentes
- ✅ **Modo Streaming** - Respuestas en tiempo real
- ✅ **Persistencia** - Guarda agentes en JSON

## 🎯 Uso Básico

### Opción 1: Interfaz Interactiva

```bash
python agent_manager.py
```

### Opción 2: Uso Programático

```python
from agent_creator import Agent
from tools import create_web_search_tool

# Crear agente
agent = Agent(
    name="Investigador",
    instructions="Eres un investigador experto",
    tools=[create_web_search_tool()]
)

# Chatear
response = agent.chat("¿Cuál es el precio de Bitcoin?")
print(response)
```

## 📁 Estructura del Proyecto

```
Antes_OpenAI/
├── agent_creator.py       # Clase Agent principal
├── agent_manager.py       # Sistema de gestión interactivo
├── tools.py              # Módulo de herramientas
├── dspy_agent.py         # Integración DSPy
├── telegram_handler.py   # Manejador de Telegram
├── utils.py              # Utilidades
├── requirements.txt      # Dependencias
├── .env                  # API Keys (no versionar)
├── Documentos/           # 📚 Toda la documentación
│   ├── INDEX.md         # Índice de documentación
│   ├── README.md        # Documentación principal
│   ├── GUIA_*.md        # Guías específicas
│   └── ...
├── demos/                # Demos y pruebas
│   ├── demo_tools.py
│   ├── demo_telegram.py
│   └── ...
└── agents/               # Agentes guardados
    └── *.json
```

## 🔑 Configuración

### 1. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con tus credenciales
nano .env  # o usa tu editor preferido
```

### 2. API Key de Z.AI (Requerido)

1. Obtén tu API key en https://z.ai
2. Agrégala a `.env`:
   ```
   ZAI_API_KEY=tu_api_key_aqui
   ```

### 3. Telegram (Opcional)

Solo si vas a usar la herramienta de Telegram:

1. Crea un bot con @BotFather en Telegram
2. Obtén tu Chat ID con @userinfobot
3. Agrégalos a `.env`:
   ```
   TELEGRAM_BOT_TOKEN=tu_token_aqui
   TELEGRAM_CHAT_ID=tu_chat_id_aqui
   ```

Ver [Documentos/GUIA_TELEGRAM.md](Documentos/GUIA_TELEGRAM.md) para más detalles.

### ⚠️ Seguridad

**NUNCA subas el archivo `.env` a GitHub** - contiene información sensible.

- ✅ `.env.example` - Plantilla (SÍ subir)
- ❌ `.env` - Tus credenciales (NO subir)

Ver [Documentos/SEGURIDAD_GITHUB.md](Documentos/SEGURIDAD_GITHUB.md) para más información.

## 🛠️ Herramientas Disponibles

| Herramienta | Descripción | Guía |
|-------------|-------------|------|
| **Web Search** | Busca información en internet | [Guía](Documentos/GUIA_HERRAMIENTAS.md#web-search) |
| **Telegram** | Envía mensajes a Telegram | [Guía](Documentos/GUIA_TELEGRAM.md) |
| **Code Interpreter** | Ejecuta código Python | [Guía](Documentos/GUIA_HERRAMIENTAS.md#code-interpreter) |
| **Drawing Tool** | Genera imágenes | [Guía](Documentos/GUIA_HERRAMIENTAS.md#drawing-tool) |

## 🤖 DSPy - Optimización Automática

DSPy se activa automáticamente cuando cargas agentes con herramientas:

```bash
python agent_manager.py
# Opción 3: Cargar agente guardado
# ✓ Agente cargado!
# 🤖 DSPy activado para mejor uso de herramientas
```

**Precisión:** 100% en 13 casos de prueba ✅

Ver [Documentos/DSPY_INTEGRADO.md](Documentos/DSPY_INTEGRADO.md)

## 📊 Ejemplos

### Investigador Web

```python
from agent_creator import Agent
from tools import create_web_search_tool

agent = Agent(
    name="Investigador",
    instructions="Eres un investigador experto. Usa web_search para información actualizada.",
    tools=[create_web_search_tool()]
)

response = agent.chat("¿Cuáles son las noticias de hoy?")
```

### Notificador Telegram

```python
from tools import create_telegram_tool

agent = Agent(
    name="Notificador",
    instructions="Envías notificaciones importantes",
    tools=[create_telegram_tool()]
)

agent.chat("Envíame un mensaje de prueba")
```

### Multi-herramienta

```python
from tools import create_web_search_tool, create_telegram_tool

agent = Agent(
    name="Monitor",
    instructions="Monitoreas precios y notificas",
    tools=[
        create_web_search_tool(),
        create_telegram_tool()
    ]
)

agent.chat("Busca el precio de Bitcoin y envíamelo por Telegram")
```

## 🧪 Demos

```bash
# Ver todas las demos
ls demos/

# Ejecutar demo de herramientas
python demos/demo_tools.py

# Ejecutar demo de Telegram
python demos/demo_telegram.py

# Evaluar DSPy
python dspy_evaluator.py
```

## 📈 Roadmap

- [x] Sistema básico de agentes
- [x] Herramientas (Web Search, Code, Drawing)
- [x] Integración con Telegram
- [x] DSPy para optimización
- [x] Sistema de evaluación
- [ ] Más herramientas (Email, Calendar, etc.)
- [ ] UI Web
- [ ] API REST

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 🔗 Enlaces

- **Documentación Completa:** [Documentos/INDEX.md](Documentos/INDEX.md)
- **Z.AI API:** https://z.ai
- **DSPy:** https://github.com/stanfordnlp/dspy

## ⭐ Agradecimientos

- Z.AI por la API
- DSPy por el framework de optimización
- La comunidad de Python

---

**📚 Para más información, consulta la [documentación completa](Documentos/INDEX.md)**
