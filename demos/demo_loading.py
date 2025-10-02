#!/usr/bin/env python3
"""
Demo del indicador de carga
Muestra cómo se ve el spinner mientras el agente procesa
"""

from agent_creator import Agent
from utils import LoadingIndicator
import time

def main():
    print("=" * 60)
    print("  DEMO: Indicador de Carga")
    print("=" * 60)
    
    # Crear un agente
    agent = Agent(
        name="Math Tutor",
        instructions="You provide help with math problems. Explain your reasoning at each step and include examples"
    )
    
    print(f"\n✓ Agente creado: {agent}\n")
    
    # Simular una pregunta con indicador de carga
    question = "What is 25% of 200?"
    print(f"Tú: {question}\n")
    
    # Mostrar indicador mientras procesa
    loader = LoadingIndicator(f"{agent.name} pensando")
    loader.start()
    
    try:
        response = agent.chat(question)
    finally:
        loader.stop()
    
    print(f"{agent.name}: {response}\n")
    
    # Segunda pregunta
    question2 = "Can you show me the steps?"
    print(f"Tú: {question2}\n")
    
    loader = LoadingIndicator(f"{agent.name} pensando")
    loader.start()
    
    try:
        response2 = agent.chat(question2)
    finally:
        loader.stop()
    
    print(f"{agent.name}: {response2}\n")
    
    print("=" * 60)
    print("  Demo completado!")
    print("=" * 60)
    print("\nAhora cuando uses 'python agent_manager.py' verás este")
    print("indicador de carga animado mientras el agente procesa.")

if __name__ == "__main__":
    main()
