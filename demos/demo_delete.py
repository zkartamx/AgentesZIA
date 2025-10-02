#!/usr/bin/env python3
"""
Demo de eliminación de agentes
Muestra cómo crear, listar y eliminar agentes
"""

from agent_creator import Agent
from pathlib import Path
import json

def main():
    print("=" * 60)
    print("  DEMO: Gestión de Agentes (Crear, Listar, Eliminar)")
    print("=" * 60)
    
    # Crear directorio de prueba
    test_dir = Path("demo_agents")
    test_dir.mkdir(exist_ok=True)
    
    print("\n📝 PASO 1: Crear algunos agentes de prueba")
    print("-" * 60)
    
    # Crear agentes de prueba
    agents_to_create = [
        {
            "name": "Test Math Tutor",
            "instructions": "You help with math problems",
            "filename": "test_math.json"
        },
        {
            "name": "Test Writer",
            "instructions": "You help write stories",
            "filename": "test_writer.json"
        },
        {
            "name": "Test Coder",
            "instructions": "You help with coding",
            "filename": "test_coder.json"
        }
    ]
    
    for agent_data in agents_to_create:
        agent = Agent(
            name=agent_data["name"],
            instructions=agent_data["instructions"]
        )
        filepath = test_dir / agent_data["filename"]
        agent.save_agent(str(filepath))
    
    print("\n✓ 3 agentes creados")
    
    print("\n📋 PASO 2: Listar agentes guardados")
    print("-" * 60)
    
    agent_files = list(test_dir.glob("*.json"))
    for i, agent_file in enumerate(agent_files, 1):
        with open(agent_file, 'r') as f:
            config = json.load(f)
        print(f"{i}. {config['name']} ({agent_file.name})")
    
    print("\n🗑️  PASO 3: Eliminar un agente específico")
    print("-" * 60)
    
    # Eliminar el segundo agente
    if len(agent_files) >= 2:
        agent_to_delete = agent_files[1]
        with open(agent_to_delete, 'r') as f:
            config = json.load(f)
        
        print(f"\nEliminando: {config['name']}")
        Agent.delete_agent(str(agent_to_delete))
    
    print("\n📋 PASO 4: Listar agentes después de eliminar")
    print("-" * 60)
    
    agent_files = list(test_dir.glob("*.json"))
    if agent_files:
        for i, agent_file in enumerate(agent_files, 1):
            with open(agent_file, 'r') as f:
                config = json.load(f)
            print(f"{i}. {config['name']} ({agent_file.name})")
    else:
        print("No hay agentes guardados")
    
    print("\n🗑️  PASO 5: Eliminar todos los agentes restantes")
    print("-" * 60)
    
    count = 0
    for agent_file in agent_files:
        agent_file.unlink()
        count += 1
    
    print(f"✓ {count} agente(s) eliminado(s)")
    
    # Limpiar directorio de prueba
    test_dir.rmdir()
    
    print("\n" + "=" * 60)
    print("  Demo completado!")
    print("=" * 60)
    print("\nAhora puedes usar 'python agent_manager.py' y seleccionar")
    print("la opción 5 para eliminar agentes guardados.")

if __name__ == "__main__":
    main()
