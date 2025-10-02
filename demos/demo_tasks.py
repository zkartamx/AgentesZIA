#!/usr/bin/env python3
"""
Demo: Sistema de Tareas para Agentes
Muestra cómo los agentes pueden gestionar tareas automáticamente
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_creator import Agent
from tools import create_task_tools

print("=" * 70)
print("  DEMO: Sistema de Tareas")
print("=" * 70)

# Crear agente con gestión de tareas
agent = Agent(
    name="Asistente Personal",
    instructions="""
    Eres un asistente personal que gestiona tareas.
    
    REGLAS:
    - Cuando el usuario te pida hacer algo, PRIMERO agrégalo como tarea
    - Cuando completes una tarea, MÁRCALA como completada
    - Usa task_list para mostrar el progreso
    
    FLUJO:
    1. Usuario pide algo → task_add
    2. Haces la tarea
    3. Marcas como completada → task_complete
    """,
    tools=create_task_tools()
)

print(f"\n✓ Agente creado: {agent.name}")
print(f"✓ Herramientas: {len(agent.get_tools())}")

print("\n=== Herramientas de Tareas ===")
for i, tool in enumerate(agent.get_tools(), 1):
    print(f"{i}. {tool['function']['name']}")
    print(f"   {tool['function']['description']}")

print("\n" + "=" * 70)
print("  Ejemplo de Uso")
print("=" * 70)

print("""
# El agente puede:

1. Agregar tareas:
   Usuario: "Recuérdame buscar el precio de Bitcoin"
   Agente: [Usa task_add] → "✓ Tarea #1 agregada"

2. Listar tareas:
   Usuario: "¿Qué tareas tengo?"
   Agente: [Usa task_list] → Muestra lista completa

3. Completar tareas:
   Usuario: "Ya busqué el precio"
   Agente: [Usa task_complete] → "✅ Tarea #1 completada"

4. Eliminar tareas:
   Usuario: "Cancela la tarea 2"
   Agente: [Usa task_delete] → "Tarea #2 eliminada"
""")

print("=" * 70)
print("  Prueba Manual")
print("=" * 70)

# Demo manual
from task_manager import TaskManager

manager = TaskManager()

print("\n1. Agregando tareas...")
manager.add_task("Investigar precio de Bitcoin")
manager.add_task("Enviar reporte por Telegram")
manager.add_task("Tomar captura de ejemplo.com")

print("\n2. Estado actual:")
manager.print_tasks(show_completed=False)

print("\n3. Completando tarea #1...")
manager.complete_task(1)

print("\n4. Estado actualizado:")
manager.print_tasks()

print("\n" + "=" * 70)
print("  ✅ Sistema de Tareas Listo!")
print("=" * 70)
