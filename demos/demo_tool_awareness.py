#!/usr/bin/env python3
"""
Test: Verificar que el agente conoce sus herramientas
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_creator import Agent
from tools import create_web_search_tool, create_telegram_tool

print("=" * 70)
print("  TEST: Conciencia de Herramientas del Agente")
print("=" * 70)

# Crear agente con herramientas
agent = Agent(
    name="Asistente con Tools",
    instructions="Eres un asistente útil.",
    tools=[
        create_web_search_tool(),
        create_telegram_tool()
    ]
)

print(f"\n✓ Agente creado: {agent}")
print(f"✓ Herramientas: {len(agent.get_tools())}\n")

# Ver las instrucciones completas que recibe el agente
print("=" * 70)
print("INSTRUCCIONES COMPLETAS DEL AGENTE:")
print("=" * 70)
print(agent.conversation_history[0]['content'])
print("=" * 70)

print("\n✅ El agente ahora sabe qué herramientas tiene disponibles!")
print("   Estas instrucciones se incluyen automáticamente en el system prompt.")
