#!/usr/bin/env python3
"""
Test de la herramienta Web Search
Verifica que la búsqueda web funcione correctamente
"""

from agent_creator import Agent
from tools import create_web_search_tool
from utils import LoadingIndicator

def test_web_search():
    print("=" * 70)
    print("  TEST: Herramienta Web Search")
    print("=" * 70)
    
    # Crear agente con web search
    print("\n1. Creando agente con herramienta de búsqueda web...")
    agent = Agent(
        name="Investigador de Prueba",
        instructions="""
        Eres un investigador. Usa la herramienta de búsqueda web para 
        encontrar información actualizada. Siempre menciona que usaste 
        búsqueda web y resume lo que encontraste.
        """,
        tools=[create_web_search_tool()]
    )
    
    print(f"✓ Agente creado: {agent}")
    print(f"✓ Herramientas configuradas: {len(agent.get_tools())}")
    
    # Mostrar configuración de la herramienta
    print("\n2. Configuración de la herramienta:")
    for tool in agent.get_tools():
        print(f"   Tipo: {tool['type']}")
        print(f"   Config: {tool.get('web_search', {})}")
    
    # Hacer una pregunta que REQUIERE búsqueda web
    print("\n3. Haciendo pregunta que requiere información actualizada...")
    question = "What is the current weather in Tokyo today?"
    print(f"\n   Pregunta: {question}")
    print("\n   Esperando respuesta...\n")
    
    loader = LoadingIndicator("Buscando en la web")
    loader.start()
    
    try:
        response = agent.chat(question)
    finally:
        loader.stop()
    
    print(f"\n{agent.name}:")
    print("-" * 70)
    print(response)
    print("-" * 70)
    
    # Verificar si la respuesta indica uso de web search
    print("\n4. Verificación:")
    
    indicators = [
        "search" in response.lower(),
        "found" in response.lower(),
        "according to" in response.lower(),
        "based on" in response.lower(),
        len(response) > 100  # Respuesta sustancial
    ]
    
    if any(indicators):
        print("✅ La herramienta parece estar funcionando")
        print("   La respuesta indica que se usó búsqueda web")
    else:
        print("⚠️  No está claro si se usó la herramienta")
        print("   La respuesta no menciona búsqueda explícitamente")
    
    # Segunda prueba con tema más específico
    print("\n" + "=" * 70)
    print("  SEGUNDA PRUEBA: Tema específico y actual")
    print("=" * 70)
    
    question2 = "What are the latest news about artificial intelligence in December 2024?"
    print(f"\n   Pregunta: {question2}")
    print("\n   Esperando respuesta...\n")
    
    loader = LoadingIndicator("Buscando información actualizada")
    loader.start()
    
    try:
        response2 = agent.chat(question2)
    finally:
        loader.stop()
    
    print(f"\n{agent.name}:")
    print("-" * 70)
    print(response2)
    print("-" * 70)
    
    print("\n" + "=" * 70)
    print("  RESUMEN DEL TEST")
    print("=" * 70)
    print("\n✓ Test completado")
    print("\nCómo saber si funcionó:")
    print("1. La respuesta debe tener información específica y detallada")
    print("2. Puede mencionar fuentes o datos actualizados")
    print("3. La respuesta es más completa que sin la herramienta")
    print("\nNota: La herramienta se usa automáticamente cuando el agente")
    print("      determina que necesita información actualizada.")

if __name__ == "__main__":
    try:
        test_web_search()
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        print("\nPosibles causas:")
        print("- Sin saldo en la cuenta Z.AI")
        print("- API key inválida")
        print("- Problema de conexión")
