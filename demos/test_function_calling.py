#!/usr/bin/env python3
"""
Test: Function Calling con Telegram
Verifica que el agente puede ejecutar herramientas correctamente
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_creator import Agent
from tools import create_telegram_tool
from utils import LoadingIndicator

print("=" * 70)
print("  TEST: Function Calling - Telegram")
print("=" * 70)

# Verificar configuración de Telegram
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

if not bot_token or not chat_id:
    print("\n⚠️  Telegram no configurado")
    print("Configura TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID en .env")
    exit(1)

# Crear agente con Telegram
agent = Agent(
    name="Notificador",
    instructions="""
    Eres un asistente que puede enviar mensajes a Telegram.
    Cuando el usuario te pida enviar un mensaje, usa la función send_telegram_message.
    """,
    tools=[create_telegram_tool()]
)

print(f"\n✓ Agente creado: {agent}")
print(f"✓ Herramientas: {len(agent.get_tools())}\n")

# Test: Enviar mensaje
request = "Envía un mensaje a Telegram que diga: 🎉 Function calling funciona correctamente!"
print(f"Usuario: {request}\n")

loader = LoadingIndicator("Procesando y enviando")
loader.start()

try:
    response = agent.chat(request)
finally:
    loader.stop()

print(f"\nAgente: {response}\n")

print("=" * 70)
print("\n✅ Si recibiste el mensaje en Telegram, ¡function calling funciona!")
print("❌ Si no recibiste nada, revisa los logs arriba")
