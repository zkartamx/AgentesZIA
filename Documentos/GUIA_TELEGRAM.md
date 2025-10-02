# Guía: Integración con Telegram

## 🤖 Configuración del Bot de Telegram

### Paso 1: Crear un Bot

1. Abre Telegram y busca **@BotFather**
2. Envía el comando `/newbot`
3. Sigue las instrucciones:
   - Elige un nombre para tu bot (ej: "Mi Agente IA")
   - Elige un username (debe terminar en 'bot', ej: "mi_agente_ia_bot")
4. **Guarda el token** que te proporciona (se ve así: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Paso 2: Obtener tu Chat ID

1. Busca **@userinfobot** en Telegram
2. Inicia una conversación
3. El bot te dará tu **Chat ID** (un número como `123456789`)

### Paso 3: Configurar Variables de Entorno

Agrega estas líneas a tu archivo `.env`:

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=tu_token_aqui
TELEGRAM_CHAT_ID=tu_chat_id_aqui
```

**Ejemplo:**
```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=987654321
```

---

## 🚀 Uso Básico

### Opción 1: Envío Manual

```python
from telegram_handler import send_telegram_message

# Enviar mensaje simple
result = send_telegram_message("Hola desde Python!")

# Enviar con formato Markdown
result = send_telegram_message(
    message="*Negrita* y _cursiva_",
    parse_mode="Markdown"
)

# Enviar con formato HTML
result = send_telegram_message(
    message="<b>Negrita</b> y <i>cursiva</i>",
    parse_mode="HTML"
)
```

### Opción 2: Con Agente

```python
from agent_creator import Agent
from tools import create_telegram_tool

# Crear agente con herramienta de Telegram
agent = Agent(
    name="Notificador",
    instructions="Puedes enviar mensajes a Telegram cuando te lo pidan",
    tools=[create_telegram_tool()]
)

# Usar el agente
response = agent.chat("Envía un mensaje a Telegram diciendo que todo está bien")
```

---

## 📋 Ejemplos Prácticos

### Ejemplo 1: Notificador de Tareas

```python
from agent_creator import Agent
from tools import create_telegram_tool

notifier = Agent(
    name="Task Notifier",
    instructions="""
    Eres un asistente que notifica el estado de tareas.
    Cuando una tarea se complete, envía un mensaje a Telegram.
    """,
    tools=[create_telegram_tool()]
)

# Simular completar una tarea
notifier.chat("La tarea 'Backup de base de datos' se completó exitosamente")
```

### Ejemplo 2: Monitor de Precios

```python
from agent_creator import Agent
from tools import create_web_search_tool, create_telegram_tool

monitor = Agent(
    name="Price Monitor",
    instructions="""
    Eres un monitor de precios.
    Busca el precio actual y si es importante, notifica a Telegram.
    """,
    tools=[
        create_web_search_tool(),
        create_telegram_tool()
    ]
)

# Monitorear precio
monitor.chat("Busca el precio de Bitcoin y notifícame si está por encima de $100,000")
```

### Ejemplo 3: Alertas de Noticias

```python
from agent_creator import Agent
from tools import create_web_search_tool, create_telegram_tool

news_bot = Agent(
    name="News Alert",
    instructions="""
    Eres un bot de noticias.
    Busca noticias importantes y envía resúmenes a Telegram.
    """,
    tools=[
        create_web_search_tool(
            search_recency_filter="oneDay",
            count=5
        ),
        create_telegram_tool()
    ]
)

# Buscar noticias
news_bot.chat("Busca las noticias más importantes de hoy sobre IA y envíame un resumen")
```

---

## 🎨 Formato de Mensajes

### Markdown

```python
message = """
*Título en Negrita*

_Texto en cursiva_

`Código inline`

[Link](https://example.com)

• Lista
• De
• Items
"""

send_telegram_message(message, parse_mode="Markdown")
```

### HTML

```python
message = """
<b>Título en Negrita</b>

<i>Texto en cursiva</i>

<code>Código inline</code>

<a href="https://example.com">Link</a>

• Lista
• De  
• Items
"""

send_telegram_message(message, parse_mode="HTML")
```

---

## 🔧 Funciones Disponibles

### `send_telegram_message(message, parse_mode=None)`

Envía un mensaje a través del bot de Telegram.

**Parámetros:**
- `message` (str): El mensaje a enviar
- `parse_mode` (str, opcional): 'Markdown' o 'HTML'

**Retorna:**
```python
{
    'success': True/False,
    'message': 'Descripción',
    'response': {...}  # Respuesta de la API de Telegram
}
```

### `create_telegram_tool()`

Crea una herramienta de Telegram para usar con agentes.

**Retorna:**
Diccionario con la configuración de la herramienta en formato Z.AI.

---

## 🧪 Probar la Configuración

### Test Manual

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar test
python telegram_handler.py
```

### Test con Demo

```bash
python demos/demo_telegram.py
```

---

## ⚠️ Notas Importantes

### Seguridad

1. **Nunca compartas tu bot token** - Es como una contraseña
2. **No versiones el archivo .env** - Ya está en .gitignore
3. **Usa variables de entorno** - No hardcodees tokens en el código

### Límites de Telegram

- **Mensajes por segundo**: 30 mensajes/segundo
- **Mensajes a un chat**: 1 mensaje/segundo
- **Longitud del mensaje**: Máximo 4096 caracteres

### Solución de Problemas

**Error: "Unauthorized"**
- Verifica que el token sea correcto
- Asegúrate de que el bot no haya sido eliminado

**Error: "Chat not found"**
- Verifica el Chat ID
- Asegúrate de haber iniciado una conversación con el bot primero

**Error: "Bad Request: message text is empty"**
- El mensaje no puede estar vacío
- Verifica que estés enviando contenido

---

## 📚 Recursos

- **API de Telegram**: https://core.telegram.org/bots/api
- **BotFather**: https://t.me/BotFather
- **Documentación de Bots**: https://core.telegram.org/bots

---

## 🎯 Casos de Uso

### 1. Sistema de Alertas
```python
# Alertas de servidor, errores, etc.
send_telegram_message("🚨 Error crítico en el servidor!")
```

### 2. Reportes Automáticos
```python
# Reportes diarios, semanales
send_telegram_message("📊 Reporte diario: 100 usuarios activos")
```

### 3. Notificaciones de Tareas
```python
# Cuando se completan tareas largas
send_telegram_message("✅ Backup completado exitosamente")
```

### 4. Monitor de Precios
```python
# Alertas de cambios de precio
send_telegram_message("💰 BTC alcanzó $120,000!")
```

### 5. Bot de Noticias
```python
# Resúmenes de noticias
send_telegram_message("📰 Noticias del día: ...")
```

---

## 🔮 Próximas Mejoras

- [ ] Soporte para enviar imágenes
- [ ] Soporte para enviar archivos
- [ ] Botones interactivos
- [ ] Responder a mensajes específicos
- [ ] Grupos y canales
- [ ] Comandos personalizados

---

## ✅ Checklist de Configuración

- [ ] Crear bot con @BotFather
- [ ] Obtener bot token
- [ ] Obtener chat ID con @userinfobot
- [ ] Agregar variables a .env
- [ ] Ejecutar test: `python telegram_handler.py`
- [ ] Verificar que llegue el mensaje
- [ ] Probar con agente: `python demos/demo_telegram.py`
