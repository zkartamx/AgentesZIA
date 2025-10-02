#!/usr/bin/env python3
"""
Demo: Gestionar Herramientas de Agentes
Muestra cómo agregar, remover y gestionar herramientas de agentes guardados
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_creator import Agent
from tools import create_web_search_tool, create_telegram_tool, create_code_interpreter_tool
from pathlib import Path

def demo_add_tools():
    """Demo de agregar herramientas a un agente existente"""
    print("=" * 70)
    print("  DEMO: Agregar Herramientas a Agente Existente")
    print("=" * 70)
    
    # Crear un agente simple sin herramientas
    print("\n1. Creando agente sin herramientas...")
    agent = Agent(
        name="Asistente Básico",
        instructions="Eres un asistente útil"
    )
    
    print(f"✓ Agente creado: {agent}")
    print(f"✓ Herramientas iniciales: {len(agent.get_tools())}\n")
    
    # Guardar el agente
    test_file = "test_agent_tools.json"
    agent.save_agent(test_file)
    print(f"✓ Agente guardado en: {test_file}\n")
    
    # Cargar el agente
    print("2. Cargando agente desde archivo...")
    loaded_agent = Agent.load_agent(test_file)
    print(f"✓ Agente cargado: {loaded_agent}")
    print(f"✓ Herramientas: {len(loaded_agent.get_tools())}\n")
    
    # Agregar herramientas
    print("3. Agregando herramientas...")
    loaded_agent.add_tool(create_web_search_tool())
    print("✓ Web Search agregada")
    
    loaded_agent.add_tool(create_telegram_tool())
    print("✓ Telegram agregada")
    
    print(f"\n✓ Total de herramientas ahora: {len(loaded_agent.get_tools())}")
    print("  Herramientas:")
    for tool in loaded_agent.get_tools():
        print(f"  - {tool['type']}")
    
    # Guardar cambios
    print("\n4. Guardando cambios...")
    loaded_agent.save_agent(test_file)
    print(f"✓ Cambios guardados en: {test_file}\n")
    
    # Verificar que se guardaron
    print("5. Verificando que se guardaron...")
    verified_agent = Agent.load_agent(test_file)
    print(f"✓ Agente recargado: {verified_agent}")
    print(f"✓ Herramientas restauradas: {len(verified_agent.get_tools())}")
    for tool in verified_agent.get_tools():
        print(f"  - {tool['type']}")
    
    # Limpiar
    os.remove(test_file)
    print(f"\n✓ Archivo de prueba eliminado\n")
    
    print("=" * 70)


def demo_remove_tools():
    """Demo de remover herramientas de un agente"""
    print("=" * 70)
    print("  DEMO: Remover Herramientas de Agente")
    print("=" * 70)
    
    # Crear agente con múltiples herramientas
    print("\n1. Creando agente con múltiples herramientas...")
    agent = Agent(
        name="Agente Completo",
        instructions="Eres un asistente versátil",
        tools=[
            create_web_search_tool(),
            create_telegram_tool(),
            create_code_interpreter_tool()
        ]
    )
    
    print(f"✓ Agente creado: {agent}")
    print(f"✓ Herramientas: {len(agent.get_tools())}")
    for tool in agent.get_tools():
        print(f"  - {tool['type']}")
    
    # Guardar
    test_file = "test_agent_remove.json"
    agent.save_agent(test_file)
    print(f"\n✓ Agente guardado en: {test_file}\n")
    
    # Cargar y remover una herramienta
    print("2. Removiendo herramienta 'telegram'...")
    loaded_agent = Agent.load_agent(test_file)
    loaded_agent.remove_tool('telegram')
    
    print(f"✓ Herramienta removida")
    print(f"✓ Herramientas restantes: {len(loaded_agent.get_tools())}")
    for tool in loaded_agent.get_tools():
        print(f"  - {tool['type']}")
    
    # Guardar cambios
    print("\n3. Guardando cambios...")
    loaded_agent.save_agent(test_file)
    print(f"✓ Cambios guardados\n")
    
    # Verificar
    print("4. Verificando cambios...")
    verified_agent = Agent.load_agent(test_file)
    print(f"✓ Herramientas después de recargar: {len(verified_agent.get_tools())}")
    for tool in verified_agent.get_tools():
        print(f"  - {tool['type']}")
    
    # Limpiar
    os.remove(test_file)
    print(f"\n✓ Archivo de prueba eliminado\n")
    
    print("=" * 70)


def demo_clear_tools():
    """Demo de limpiar todas las herramientas"""
    print("=" * 70)
    print("  DEMO: Limpiar Todas las Herramientas")
    print("=" * 70)
    
    # Crear agente con herramientas
    print("\n1. Creando agente con herramientas...")
    agent = Agent(
        name="Agente con Tools",
        instructions="Eres un asistente",
        tools=[
            create_web_search_tool(),
            create_telegram_tool()
        ]
    )
    
    print(f"✓ Agente creado con {len(agent.get_tools())} herramientas\n")
    
    # Limpiar herramientas
    print("2. Limpiando todas las herramientas...")
    agent.clear_tools()
    
    print(f"✓ Herramientas limpiadas")
    print(f"✓ Herramientas restantes: {len(agent.get_tools())}\n")
    
    # Guardar
    test_file = "test_agent_clear.json"
    agent.save_agent(test_file)
    print(f"✓ Agente guardado sin herramientas\n")
    
    # Verificar
    print("3. Verificando...")
    loaded_agent = Agent.load_agent(test_file)
    print(f"✓ Herramientas después de cargar: {len(loaded_agent.get_tools())}")
    
    # Limpiar
    os.remove(test_file)
    print(f"✓ Archivo de prueba eliminado\n")
    
    print("=" * 70)


def main():
    print("\n" + "=" * 70)
    print("  GESTIÓN DE HERRAMIENTAS DE AGENTES")
    print("=" * 70)
    
    # Demo 1: Agregar herramientas
    demo_add_tools()
    
    print("\n")
    
    # Demo 2: Remover herramientas
    demo_remove_tools()
    
    print("\n")
    
    # Demo 3: Limpiar herramientas
    demo_clear_tools()
    
    print("\n" + "=" * 70)
    print("  Demos completados!")
    print("=" * 70)
    print("\n💡 Ahora puedes usar la opción 5 del menú principal para")
    print("   gestionar herramientas de tus agentes guardados:")
    print("\n   python agent_manager.py")
    print("   → Opción 5: Gestionar herramientas de agentes")


if __name__ == "__main__":
    main()
