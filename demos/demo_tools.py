#!/usr/bin/env python3
"""
Demo de Agentes con Herramientas (Tools)
Muestra cómo crear agentes que usan herramientas como web search
"""

from agent_creator import Agent
from tools import create_web_search_tool, create_code_interpreter_tool, print_available_tools
from utils import LoadingIndicator

def demo_web_search():
    """Demo de agente con búsqueda web"""
    print("=" * 70)
    print("  DEMO 1: Agente con Web Search")
    print("=" * 70)
    
    # Crear herramienta de búsqueda web
    web_search_tool = create_web_search_tool()
    
    # Crear agente investigador con herramienta de búsqueda
    researcher = Agent(
        name="Investigador Web",
        instructions="Eres un investigador experto. Usa búsqueda web para encontrar información actualizada y precisa. Cita tus fuentes.",
        tools=[web_search_tool]
    )
    
    print(f"\n✓ Agente creado: {researcher}")
    print(f"✓ Herramientas: {len(researcher.get_tools())} configurada(s)")
    print(f"  - Web Search: Habilitada\n")
    
    # Hacer una pregunta que requiere búsqueda web
    question = "What are the latest developments in artificial intelligence in 2024?"
    print(f"Pregunta: {question}\n")
    
    loader = LoadingIndicator(f"{researcher.name} buscando")
    loader.start()
    
    try:
        response = researcher.chat(question)
    finally:
        loader.stop()
    
    print(f"{researcher.name}:\n{response}\n")


def demo_code_interpreter():
    """Demo de agente con intérprete de código"""
    print("=" * 70)
    print("  DEMO 2: Agente con Code Interpreter")
    print("=" * 70)
    
    # Crear herramienta de intérprete de código
    code_tool = create_code_interpreter_tool()
    
    # Crear agente programador con herramienta de código
    coder = Agent(
        name="Programador Python",
        instructions="Eres un experto en Python. Puedes ejecutar código para resolver problemas. Explica tu código claramente.",
        tools=[code_tool]
    )
    
    print(f"\n✓ Agente creado: {coder}")
    print(f"✓ Herramientas: {len(coder.get_tools())} configurada(s)")
    print(f"  - Code Interpreter: Habilitada\n")
    
    # Hacer una pregunta que requiere código
    question = "Calculate the factorial of 10 and show me the code"
    print(f"Pregunta: {question}\n")
    
    loader = LoadingIndicator(f"{coder.name} programando")
    loader.start()
    
    try:
        response = coder.chat(question)
    finally:
        loader.stop()
    
    print(f"{coder.name}:\n{response}\n")


def demo_multiple_tools():
    """Demo de agente con múltiples herramientas"""
    print("=" * 70)
    print("  DEMO 3: Agente con Múltiples Herramientas")
    print("=" * 70)
    
    # Crear múltiples herramientas
    web_search = create_web_search_tool()
    code_interpreter = create_code_interpreter_tool()
    
    # Crear agente con múltiples herramientas
    super_agent = Agent(
        name="Super Asistente",
        instructions="Eres un asistente versátil. Puedes buscar información en la web y ejecutar código Python. Usa las herramientas apropiadas según la tarea.",
        tools=[web_search, code_interpreter]
    )
    
    print(f"\n✓ Agente creado: {super_agent}")
    print(f"✓ Herramientas: {len(super_agent.get_tools())} configurada(s)")
    print(f"  - Web Search: Habilitada")
    print(f"  - Code Interpreter: Habilitada\n")
    
    # Hacer una pregunta que puede usar ambas herramientas
    question = "Find the current population of Tokyo and calculate what 10% of that number is"
    print(f"Pregunta: {question}\n")
    
    loader = LoadingIndicator(f"{super_agent.name} trabajando")
    loader.start()
    
    try:
        response = super_agent.chat(question)
    finally:
        loader.stop()
    
    print(f"{super_agent.name}:\n{response}\n")


def demo_add_remove_tools():
    """Demo de agregar y remover herramientas dinámicamente"""
    print("=" * 70)
    print("  DEMO 4: Gestión Dinámica de Herramientas")
    print("=" * 70)
    
    # Crear agente sin herramientas
    agent = Agent(
        name="Agente Flexible",
        instructions="Eres un asistente adaptable."
    )
    
    print(f"\n✓ Agente creado: {agent}")
    print(f"✓ Herramientas iniciales: {len(agent.get_tools())}\n")
    
    # Agregar herramienta de búsqueda web
    print("➕ Agregando Web Search...")
    agent.add_tool(create_web_search_tool())
    print(f"✓ Herramientas ahora: {len(agent.get_tools())}")
    print(f"  Tipos: {[t['type'] for t in agent.get_tools()]}\n")
    
    # Agregar herramienta de código
    print("➕ Agregando Code Interpreter...")
    agent.add_tool(create_code_interpreter_tool())
    print(f"✓ Herramientas ahora: {len(agent.get_tools())}")
    print(f"  Tipos: {[t['type'] for t in agent.get_tools()]}\n")
    
    # Remover herramienta de búsqueda web
    print("➖ Removiendo Web Search...")
    agent.remove_tool('web_search')
    print(f"✓ Herramientas ahora: {len(agent.get_tools())}")
    print(f"  Tipos: {[t['type'] for t in agent.get_tools()]}\n")
    
    # Limpiar todas las herramientas
    print("🗑️  Limpiando todas las herramientas...")
    agent.clear_tools()
    print(f"✓ Herramientas ahora: {len(agent.get_tools())}\n")


def demo_save_load_with_tools():
    """Demo de guardar y cargar agentes con herramientas"""
    print("=" * 70)
    print("  DEMO 5: Guardar y Cargar Agentes con Herramientas")
    print("=" * 70)
    
    # Crear agente con herramientas
    researcher = Agent(
        name="Investigador Científico",
        instructions="Eres un investigador científico. Usa búsqueda web para información actualizada.",
        tools=[create_web_search_tool()]
    )
    
    print(f"\n✓ Agente creado: {researcher}")
    print(f"✓ Herramientas: {len(researcher.get_tools())}\n")
    
    # Guardar agente
    filename = "researcher_with_tools.json"
    print(f"💾 Guardando agente en '{filename}'...")
    researcher.save_agent(filename)
    
    # Cargar agente
    print(f"\n📂 Cargando agente desde '{filename}'...")
    loaded_agent = Agent.load_agent(filename)
    
    print(f"✓ Agente cargado: {loaded_agent}")
    print(f"✓ Herramientas restauradas: {len(loaded_agent.get_tools())}")
    print(f"  Tipos: {[t['type'] for t in loaded_agent.get_tools()]}\n")
    
    # Limpiar archivo de prueba
    import os
    os.remove(filename)
    print(f"🗑️  Archivo de prueba eliminado\n")


def main():
    print("\n" + "=" * 70)
    print("  SISTEMA DE HERRAMIENTAS PARA AGENTES Z.AI")
    print("=" * 70)
    
    # Mostrar herramientas disponibles
    print_available_tools()
    
    print("\n" + "=" * 70)
    print("  DEMOSTRACIONES")
    print("=" * 70)
    
    # Ejecutar demos
    try:
        print("\n⚠️  Nota: Estas demos requieren saldo en tu cuenta Z.AI\n")
        
        # Demo 1: Web Search
        demo_web_search()
        
        # Demo 2: Code Interpreter
        # demo_code_interpreter()  # Descomenta si quieres probar
        
        # Demo 3: Múltiples herramientas
        # demo_multiple_tools()  # Descomenta si quieres probar
        
        # Demo 4: Gestión dinámica
        demo_add_remove_tools()
        
        # Demo 5: Guardar/Cargar
        demo_save_load_with_tools()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Asegúrate de tener saldo en tu cuenta Z.AI")
    
    print("\n" + "=" * 70)
    print("  Demos completados!")
    print("=" * 70)
    print("\nAhora puedes crear tus propios agentes con herramientas:")
    print("  from agent_creator import Agent")
    print("  from tools import create_web_search_tool")
    print("")
    print("  agent = Agent(")
    print("      name='Mi Agente',")
    print("      instructions='...',")
    print("      tools=[create_web_search_tool()]")
    print("  )")


if __name__ == "__main__":
    main()
