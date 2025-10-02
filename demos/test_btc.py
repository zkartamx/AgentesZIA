#!/usr/bin/env python3
"""
Test: Precio de Bitcoin con Web Search
"""

from agent_creator import Agent
from tools import create_web_search_tool
from utils import LoadingIndicator

print("=" * 70)
print("  TEST: Precio de Bitcoin con Web Search")
print("=" * 70)

# Crear agente con web search
agent = Agent(
    name="Analista Cripto",
    instructions="""
    Eres un analista de criptomonedas. Usa la herramienta de búsqueda web 
    para obtener el precio actual de Bitcoin y otra información relevante 
    del mercado. Proporciona datos precisos y actualizados.
    """,
    tools=[create_web_search_tool()]
)

print(f"\n✓ Agente creado con Web Search")
print(f"✓ Herramientas: {len(agent.get_tools())}\n")

question = "¿Cuánto cuesta el precio de BTC hoy?"
print(f"Pregunta: {question}\n")

loader = LoadingIndicator("Buscando precio actual de Bitcoin")
loader.start()

try:
    response = agent.chat(question)
finally:
    loader.stop()

print(f"\n{agent.name}:")
print("=" * 70)
print(response)
print("=" * 70)
