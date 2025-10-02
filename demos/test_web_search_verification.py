#!/usr/bin/env python3
"""
Verificación de Web Search - Comparación con datos reales
"""

from agent_creator import Agent
from tools import create_web_search_tool
from utils import LoadingIndicator
import requests
import json

print("=" * 70)
print("  VERIFICACIÓN: Web Search vs Datos Reales")
print("=" * 70)

# Obtener precio real de Bitcoin
print("\n1. Obteniendo precio REAL de Bitcoin desde API de Coinbase...")
try:
    response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot")
    real_price = float(response.json()['data']['amount'])
    print(f"   ✓ Precio REAL: ${real_price:,.2f} USD")
except Exception as e:
    print(f"   ❌ Error obteniendo precio real: {e}")
    real_price = None

# Crear agente CON web search
print("\n2. Preguntando al agente CON Web Search...")
agent_with_search = Agent(
    name="Con Web Search",
    instructions="Usa web search para obtener el precio ACTUAL de Bitcoin. Sé específico con el número.",
    tools=[create_web_search_tool()]
)

loader = LoadingIndicator("Consultando con Web Search")
loader.start()
try:
    response_with = agent_with_search.chat("What is the current price of Bitcoin in USD? Give me just the number.")
finally:
    loader.stop()

print(f"\n   Respuesta CON Web Search:")
print(f"   {response_with[:200]}...")

# Crear agente SIN web search
print("\n3. Preguntando al agente SIN Web Search (solo conocimiento)...")
agent_without_search = Agent(
    name="Sin Web Search",
    instructions="Responde con tu conocimiento base."
)

loader = LoadingIndicator("Consultando sin Web Search")
loader.start()
try:
    response_without = agent_without_search.chat("What is the current price of Bitcoin in USD? Give me just the number.")
finally:
    loader.stop()

print(f"\n   Respuesta SIN Web Search:")
print(f"   {response_without[:200]}...")

print("\n" + "=" * 70)
print("  ANÁLISIS")
print("=" * 70)

if real_price:
    print(f"\n✓ Precio REAL (API Coinbase): ${real_price:,.2f} USD")
    print(f"\n⚠️  Comparación:")
    print(f"   - Con Web Search: {response_with[:100]}")
    print(f"   - Sin Web Search: {response_without[:100]}")
    
    print("\n💡 Observación:")
    print("   Si ambas respuestas son similares y diferentes del precio real,")
    print("   es posible que:")
    print("   1. La herramienta no esté funcionando correctamente")
    print("   2. El modelo esté ignorando los resultados de búsqueda")
    print("   3. Z.AI tenga una implementación diferente de web_search")

print("\n" + "=" * 70)
