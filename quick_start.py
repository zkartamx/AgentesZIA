#!/usr/bin/env python3
"""
Quick Start - Guía rápida para empezar a usar agentes
"""

from agent_creator import Agent

def main():
    print("=" * 70)
    print("  QUICK START - Sistema de Agentes Z.AI")
    print("=" * 70)
    
    print("\n📚 PASO 1: Crear un agente")
    print("-" * 70)
    print("""
    from agent_creator import Agent

    agent = Agent(
        name="Math Tutor",
        instructions="You provide help with math problems. Explain your reasoning at each step and include examples"
    )
    """)
    
    # Crear el agente
    agent = Agent(
        name="Math Tutor",
        instructions="You provide help with math problems. Explain your reasoning at each step and include examples"
    )
    print(f"✓ Agente creado: {agent}\n")
    
    print("💬 PASO 2: Chatear con el agente")
    print("-" * 70)
    
    question = "What is 15% of 80?"
    print(f"\nPregunta: {question}")
    print("\nRespuesta:")
    response = agent.chat(question)
    print(response)
    
    print("\n" + "=" * 70)
    print("  OPCIONES ADICIONALES")
    print("=" * 70)
    
    print("\n🔄 Modo Streaming (respuestas en tiempo real):")
    print("-" * 70)
    print("""
    for chunk in agent.chat_stream("Tu pregunta"):
        print(chunk, end="", flush=True)
    """)
    
    print("\n💾 Guardar agente:")
    print("-" * 70)
    print("""
    agent.save_agent("mi_agente.json")
    """)
    
    print("\n📂 Cargar agente:")
    print("-" * 70)
    print("""
    loaded_agent = Agent.load_agent("mi_agente.json")
    """)
    
    print("\n🔄 Reiniciar conversación:")
    print("-" * 70)
    print("""
    agent.reset_conversation()
    """)
    
    print("\n📜 Ver historial:")
    print("-" * 70)
    print("""
    history = agent.get_history()
    for msg in history:
        print(f"{msg['role']}: {msg['content']}")
    """)
    
    print("\n" + "=" * 70)
    print("  PRÓXIMOS PASOS")
    print("=" * 70)
    print("""
    1. Ejecuta 'python agent_manager.py' para usar el sistema interactivo
    2. Ejecuta 'python example_agents.py' para ver más ejemplos
    3. Lee 'README.md' para documentación completa
    
    ¡Empieza a crear tus propios agentes personalizados!
    """)

if __name__ == "__main__":
    main()
