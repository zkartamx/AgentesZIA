#!/usr/bin/env python3
"""
Demo: Agente con Selenium completo (todas las funciones)
Muestra cómo create_selenium_tool() ahora incluye TODAS las capacidades
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_creator import Agent
from tools import create_selenium_tool

print("=" * 70)
print("  DEMO: Selenium Completo")
print("=" * 70)

# Crear agente con Selenium (ahora incluye TODAS las funciones)
agent = Agent(
    name="Web Scraper Pro",
    instructions="""
    Eres un experto en web scraping.
    
    FLUJO CORRECTO:
    1. Navega con selenium_navigate
    2. Extrae contenido con selenium_get_text
    3. Si necesitas algo específico, usa selenium_find_text
    4. Toma capturas con selenium_screenshot si es útil
    """,
    tools=create_selenium_tool()  # ← Ahora incluye TODAS las funciones
)

print(f"\n✓ Agente creado: {agent.name}")
print(f"✓ Herramientas: {len(agent.get_tools())}")

print("\n=== Herramientas Incluidas ===")
for i, tool in enumerate(agent.get_tools(), 1):
    if tool['type'] == 'function':
        print(f"{i}. {tool['function']['name']}")
        print(f"   {tool['function']['description']}")

print("\n" + "=" * 70)
print("  ¡Ahora create_selenium_tool() incluye TODO!")
print("=" * 70)

print("\nAntes:")
print("  create_selenium_tool() → Solo navegación")

print("\nAhora:")
print("  create_selenium_tool() → 4 funciones completas:")
print("    1. selenium_navigate - Navegar")
print("    2. selenium_get_text - Extraer texto")
print("    3. selenium_find_text - Buscar elementos")
print("    4. selenium_screenshot - Tomar capturas")

print("\n" + "=" * 70)
print("  Uso:")
print("=" * 70)
print("""
from agent_creator import Agent
from tools import create_selenium_tool

# Simplemente usa create_selenium_tool()
agent = Agent(
    name="Scraper",
    instructions="...",
    tools=create_selenium_tool()  # ← Incluye TODAS las funciones
)

# El agente ahora puede:
agent.chat("Navega a example.com")
agent.chat("Extrae todo el texto")
agent.chat("Busca el elemento h1")
agent.chat("Toma una captura")
""")

print("=" * 70)
