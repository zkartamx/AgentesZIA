#!/usr/bin/env python3
"""
Ejemplos de uso del sistema de agentes
"""

from agent_creator import Agent

# Ejemplo 1: Crear un agente tutor de matemáticas
print("=" * 60)
print("EJEMPLO 1: Math Tutor Agent")
print("=" * 60)

math_tutor = Agent(
    name="Math Tutor",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples"
)

print(f"\nAgente creado: {math_tutor}")
print("\nPregunta: Can you help me solve this equation: 2x + 5 = 13?")
response = math_tutor.chat("Can you help me solve this equation: 2x + 5 = 13?")
print(f"\nRespuesta:\n{response}")

# Ejemplo 2: Crear un agente de traducción
print("\n" + "=" * 60)
print("EJEMPLO 2: Translation Agent")
print("=" * 60)

translator = Agent(
    name="Translator",
    instructions="You are a professional translator. Translate text accurately while preserving tone and context. Always specify the source and target languages."
)

print(f"\nAgente creado: {translator}")
print("\nPregunta: Translate 'Hello, how are you?' to Spanish")
response = translator.chat("Translate 'Hello, how are you?' to Spanish")
print(f"\nRespuesta:\n{response}")

# Ejemplo 3: Crear un agente de análisis de datos
print("\n" + "=" * 60)
print("EJEMPLO 3: Data Analyst Agent")
print("=" * 60)

data_analyst = Agent(
    name="Data Analyst",
    instructions="You are a data analyst expert. Help users understand data, create analysis plans, and interpret results. Provide clear explanations and suggest visualization approaches."
)

print(f"\nAgente creado: {data_analyst}")
print("\nPregunta: What's the best way to analyze customer churn data?")
response = data_analyst.chat("What's the best way to analyze customer churn data?")
print(f"\nRespuesta:\n{response}")

# Ejemplo 4: Guardar un agente
print("\n" + "=" * 60)
print("EJEMPLO 4: Guardar y Cargar Agente")
print("=" * 60)

# Crear un agente personalizado
fitness_coach = Agent(
    name="Fitness Coach",
    instructions="You are a certified fitness coach. Provide workout advice, nutrition tips, and motivation. Always prioritize safety and proper form."
)

# Guardar el agente
fitness_coach.save_agent("fitness_coach.json")
print("\n✓ Agente guardado en 'fitness_coach.json'")

# Cargar el agente
loaded_agent = Agent.load_agent("fitness_coach.json")
print(f"✓ Agente cargado: {loaded_agent}")

print("\nPregunta: What's a good beginner workout routine?")
response = loaded_agent.chat("What's a good beginner workout routine?")
print(f"\nRespuesta:\n{response}")

# Ejemplo 5: Modo streaming
print("\n" + "=" * 60)
print("EJEMPLO 5: Streaming Mode")
print("=" * 60)

storyteller = Agent(
    name="Storyteller",
    instructions="You are a creative storyteller. Create engaging, imaginative stories with vivid descriptions."
)

print(f"\nAgente creado: {storyteller}")
print("\nPregunta (streaming): Tell me a short story about a robot learning to paint")
print("\nRespuesta (streaming):")
for chunk in storyteller.chat_stream("Tell me a short story about a robot learning to paint"):
    print(chunk, end="", flush=True)
print("\n")

print("\n" + "=" * 60)
print("Ejemplos completados!")
print("=" * 60)
