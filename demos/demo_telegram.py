#!/usr/bin/env python3
"""
Demo: Agente con integración de Telegram
Muestra cómo crear un agente que puede enviar mensajes a Telegram
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_creator import Agent
from tools import create_telegram_tool, create_web_search_tool
from telegram_handler import handle_function_call
from utils import LoadingIndicator
import json

def demo_telegram_notifier():
    """Demo de agente que envía notificaciones a Telegram"""
    print("=" * 70)
    print("  DEMO: Agente con Notificaciones de Telegram")
    print("=" * 70)
    
    # Verificar configuración
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("\n⚠️  Configuración requerida:")
        print("\nAgrega estas variables a tu archivo .env:")
        print("TELEGRAM_BOT_TOKEN=tu_token_aqui")
        print("TELEGRAM_CHAT_ID=tu_chat_id_aqui")
        print("\n📝 Cómo obtenerlas:")
        print("1. Bot Token: Habla con @BotFather en Telegram → /newbot")
        print("2. Chat ID: Habla con @userinfobot en Telegram")
        return
    
    # Crear agente con herramienta de Telegram
    agent = Agent(
        name="Notificador",
        instructions="""
        Eres un asistente que puede enviar notificaciones a Telegram.
        Cuando el usuario te pida enviar un mensaje, usa la función send_telegram_message.
        Sé claro y conciso en los mensajes.
        """,
        tools=[create_telegram_tool()]
    )
    
    print(f"\n✓ Agente creado: {agent}")
    print(f"✓ Herramientas: {len(agent.get_tools())}")
    print(f"  - Telegram: Configurada\n")
    
    # Ejemplo 1: Enviar mensaje simple
    print("📱 Ejemplo 1: Enviar mensaje simple")
    print("-" * 70)
    
    request = "Envía un mensaje a Telegram que diga: Hola desde el agente de IA!"
    print(f"Usuario: {request}\n")
    
    loader = LoadingIndicator("Procesando")
    loader.start()
    
    try:
        response = agent.chat(request)
    finally:
        loader.stop()
    
    print(f"Agente: {response}\n")
    
    # Verificar si hay function calls
    last_message = agent.get_history()[-1]
    if 'tool_calls' in str(last_message):
        print("✅ El agente intentó usar la función de Telegram")
        print("⚠️  Nota: En producción, necesitas implementar el manejo de tool_calls")
    
    print("\n" + "=" * 70)


def demo_telegram_with_web_search():
    """Demo de agente que busca información y la envía a Telegram"""
    print("=" * 70)
    print("  DEMO: Agente con Web Search + Telegram")
    print("=" * 70)
    
    # Verificar configuración
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("\n⚠️  Telegram no configurado. Saltando demo.")
        return
    
    # Crear agente con múltiples herramientas
    agent = Agent(
        name="Investigador Notificador",
        instructions="""
        Eres un asistente que puede:
        1. Buscar información en la web
        2. Enviar resúmenes a Telegram
        
        Cuando te pidan investigar algo y notificar, primero busca la información
        y luego envía un resumen conciso a Telegram.
        """,
        tools=[
            create_web_search_tool(),
            create_telegram_tool()
        ]
    )
    
    print(f"\n✓ Agente creado: {agent}")
    print(f"✓ Herramientas: {len(agent.get_tools())}")
    print(f"  - Web Search: Habilitada")
    print(f"  - Telegram: Habilitada\n")
    
    request = "Busca el precio actual de Bitcoin y envíame un resumen a Telegram"
    print(f"Usuario: {request}\n")
    
    loader = LoadingIndicator("Investigando y notificando")
    loader.start()
    
    try:
        response = agent.chat(request)
    finally:
        loader.stop()
    
    print(f"Agente: {response}\n")
    
    print("=" * 70)


def demo_manual_telegram():
    """Demo de envío manual a Telegram (sin agente)"""
    print("=" * 70)
    print("  DEMO: Envío Manual a Telegram")
    print("=" * 70)
    
    from telegram_handler import send_telegram_message
    
    print("\n📱 Enviando mensaje de prueba...\n")
    
    result = send_telegram_message(
        message="🤖 *Prueba desde el Sistema de Agentes*\n\n✅ El sistema está funcionando correctamente!",
        parse_mode="Markdown"
    )
    
    if result['success']:
        print("✅ Mensaje enviado exitosamente!")
        print(f"\nDetalles: {json.dumps(result['response'], indent=2)}")
    else:
        print(f"❌ Error: {result['error']}")
    
    print("\n" + "=" * 70)


def main():
    print("\n" + "=" * 70)
    print("  SISTEMA DE NOTIFICACIONES TELEGRAM")
    print("=" * 70)
    
    # Demo 1: Envío manual
    demo_manual_telegram()
    
    print("\n")
    
    # Demo 2: Agente con Telegram
    demo_telegram_notifier()
    
    print("\n")
    
    # Demo 3: Agente con Web Search + Telegram
    # demo_telegram_with_web_search()  # Descomenta si quieres probar
    
    print("\n" + "=" * 70)
    print("  Demos completados!")
    print("=" * 70)
    print("\n💡 Nota: Para usar function calls con el agente, necesitas:")
    print("   1. Procesar los tool_calls de la respuesta")
    print("   2. Ejecutar las funciones correspondientes")
    print("   3. Enviar los resultados de vuelta al agente")
    print("\n   Ver documentación de Z.AI sobre function calling")


if __name__ == "__main__":
    main()
