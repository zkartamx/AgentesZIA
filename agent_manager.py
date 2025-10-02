#!/usr/bin/env python3
"""
Sistema de Gestión de Agentes
Permite crear, guardar, cargar y chatear con agentes personalizados
"""

from agent_creator import Agent, create_math_tutor, create_code_reviewer, create_creative_writer
from utils import LoadingIndicator
from tools import create_web_search_tool, create_code_interpreter_tool, get_available_tools
from dspy_agent import DSPyAgent
from debug_config import DebugConfig, DebugLevel
import os
import json
from pathlib import Path


class AgentManager:
    """Gestor de agentes para crear y administrar múltiples agentes"""
    
    def __init__(self, agents_dir: str = "agents"):
        self.agents_dir = Path(agents_dir)
        self.agents_dir.mkdir(exist_ok=True)
        self.current_agent = None
    
    def create_custom_agent(self):
        """Interfaz para crear un agente personalizado"""
        print("\n=== Crear Nuevo Agente ===")
        name = input("Nombre del agente: ").strip()
        print("\nInstrucciones del agente (describe su rol y comportamiento):")
        instructions = input("> ").strip()
        
        model = input("\nModelo (presiona Enter para usar 'glm-4.6'): ").strip()
        if not model:
            model = "glm-4.6"
        
        # Preguntar si desea agregar herramientas
        tools = []
        add_tools = input("\n¿Agregar herramientas al agente? (s/n): ").lower()
        if add_tools == 's':
            tools = self._configure_tools()
        
        base_agent = Agent(name=name, instructions=instructions, model=model, tools=tools)
        print(f"\n✓ Agente '{name}' creado exitosamente!")
        if tools:
            print(f"✓ Herramientas configuradas: {len(tools)}")
        
        # Preguntar si desea guardarlo
        save = input("\n¿Guardar este agente? (s/n): ").lower()
        if save == 's':
            filename = f"{name.lower().replace(' ', '_')}.json"
            filepath = self.agents_dir / filename
            base_agent.save_agent(str(filepath))
        
        # Envolver con DSPy si tiene herramientas
        if tools:
            print("🤖 DSPy activado para mejor uso de herramientas")
            return DSPyAgent(base_agent)
        
        return base_agent
    
    def _configure_tools(self):
        """Interfaz para configurar herramientas"""
        tools = []
        available_tools = get_available_tools()
        
        print("\n=== Herramientas Disponibles ===")
        tool_list = list(available_tools.items())
        for i, (key, info) in enumerate(tool_list, 1):
            print(f"{i}. {info['name']} - {info['description']}")
        
        print("\nSelecciona herramientas (números separados por comas, ej: 1,2)")
        print("O presiona Enter para no agregar herramientas")
        selection = input("> ").strip()
        
        if not selection:
            return tools
        
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            for idx in indices:
                if 0 <= idx < len(tool_list):
                    key, info = tool_list[idx]
                    if key == 'function':
                        print(f"\n⚠️  La herramienta 'function' requiere configuración personalizada")
                        print("Saltando por ahora...")
                        continue
                    tool = info['function']()
                    tools.append(tool)
                    print(f"✓ Agregada: {info['name']}")
        except ValueError:
            print("Entrada inválida. No se agregaron herramientas.")
        
        return tools
    
    def create_predefined_agent(self):
        """Crear un agente predefinido"""
        print("\n=== Agentes Predefinidos ===")
        print("1. Math Tutor - Tutor de matemáticas")
        print("2. Code Reviewer - Revisor de código")
        print("3. Creative Writer - Escritor creativo")
        
        choice = input("\nSelecciona un agente (1-3): ").strip()
        
        agents_map = {
            '1': create_math_tutor,
            '2': create_code_reviewer,
            '3': create_creative_writer
        }
        
        if choice in agents_map:
            agent = agents_map[choice]()
            print(f"\n✓ Agente '{agent.name}' creado!")
            return agent
        else:
            print("Opción inválida")
            return None
    
    def list_saved_agents(self):
        """Lista todos los agentes guardados"""
        agents = list(self.agents_dir.glob("*.json"))
        if not agents:
            print("\nNo hay agentes guardados.")
            return []
        
        print("\n=== Agentes Guardados ===")
        for i, agent_file in enumerate(agents, 1):
            with open(agent_file, 'r') as f:
                config = json.load(f)
            print(f"{i}. {config['name']} ({agent_file.name})")
        
        return agents
    
    def load_saved_agent(self):
        """Cargar un agente guardado"""
        agents = self.list_saved_agents()
        if not agents:
            return None
        
        choice = input("\nSelecciona un agente (número): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(agents):
                # Cargar agente base
                base_agent = Agent.load_agent(str(agents[idx]))
                
                # Envolver con DSPy si tiene herramientas
                if base_agent.get_tools():
                    print(f"\n✓ Agente '{base_agent.name}' cargado!")
                    print("🤖 DSPy activado para mejor uso de herramientas")
                    return DSPyAgent(base_agent)
                else:
                    print(f"\n✓ Agente '{base_agent.name}' cargado!")
                    return base_agent
            else:
                print("Número inválido")
                return None
        except ValueError:
            print("Entrada inválida")
            return None
    
    def manage_agent_tools(self):
        """Gestionar herramientas de un agente guardado"""
        agents = self.list_saved_agents()
        if not agents:
            return
        
        choice = input("\nSelecciona un agente (número): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(agents):
                agent_file = agents[idx]
                agent = Agent.load_agent(str(agent_file))
                
                print(f"\n=== Gestionar Herramientas: {agent.name} ===")
                print(f"Herramientas actuales: {len(agent.get_tools())}")
                
                if agent.get_tools():
                    print("\nHerramientas configuradas:")
                    for i, tool in enumerate(agent.get_tools(), 1):
                        tool_type = tool.get('type', 'unknown')
                        if tool_type == 'function' and 'function' in tool:
                            func_name = tool['function'].get('name', 'unknown')
                            print(f"  {i}. {tool_type} ({func_name})")
                        else:
                            print(f"  {i}. {tool_type}")
                
                print("\nOpciones:")
                print("1. Agregar herramientas")
                print("2. Remover herramientas")
                print("3. Limpiar todas las herramientas")
                print("4. Volver")
                
                option = input("\nSelecciona una opción: ").strip()
                
                if option == '1':
                    # Agregar herramientas
                    new_tools = self._configure_tools()
                    for tool in new_tools:
                        agent.add_tool(tool)
                    print(f"\n✓ {len(new_tools)} herramienta(s) agregada(s)")
                    
                    # Guardar cambios
                    agent.save_agent(str(agent_file))
                    print(f"✓ Cambios guardados en {agent_file.name}")
                
                elif option == '2':
                    # Remover herramientas
                    if not agent.get_tools():
                        print("\nNo hay herramientas para remover")
                        return
                    
                    print("\nHerramientas actuales:")
                    for i, tool in enumerate(agent.get_tools(), 1):
                        tool_type = tool.get('type', 'unknown')
                        if tool_type == 'function' and 'function' in tool:
                            func_name = tool['function'].get('name', 'unknown')
                            print(f"{i}. {tool_type} ({func_name})")
                        else:
                            print(f"{i}. {tool_type}")
                    
                    remove_choice = input("\nNúmero de herramienta a remover (o 'cancelar'): ").strip()
                    if remove_choice.lower() != 'cancelar':
                        try:
                            remove_idx = int(remove_choice) - 1
                            if 0 <= remove_idx < len(agent.get_tools()):
                                tool_type = agent.get_tools()[remove_idx].get('type')
                                agent.remove_tool(tool_type)
                                print(f"\n✓ Herramienta '{tool_type}' removida")
                                
                                # Guardar cambios
                                agent.save_agent(str(agent_file))
                                print(f"✓ Cambios guardados en {agent_file.name}")
                            else:
                                print("Número inválido")
                        except ValueError:
                            print("Entrada inválida")
                
                elif option == '3':
                    # Limpiar todas
                    confirm = input("\n⚠️  ¿Limpiar TODAS las herramientas? (s/n): ").lower()
                    if confirm == 's':
                        agent.clear_tools()
                        print("\n✓ Todas las herramientas removidas")
                        
                        # Guardar cambios
                        agent.save_agent(str(agent_file))
                        print(f"✓ Cambios guardados en {agent_file.name}")
                    else:
                        print("\nOperación cancelada")
                
            else:
                print("Número inválido")
        except ValueError:
            print("Entrada inválida")
    
    def delete_saved_agents(self):
        """Eliminar agentes guardados"""
        agents = self.list_saved_agents()
        if not agents:
            return
        
        print("\nOpciones:")
        print("- Ingresa un número para eliminar ese agente")
        print("- Ingresa 'todos' para eliminar todos los agentes")
        print("- Ingresa 'cancelar' para volver")
        
        choice = input("\nSelecciona una opción: ").strip().lower()
        
        if choice == 'cancelar':
            print("\nOperación cancelada")
            return
        
        if choice == 'todos':
            confirm = input("\n⚠️  ¿Estás seguro de eliminar TODOS los agentes? (s/n): ").lower()
            if confirm == 's':
                count = 0
                for agent_file in agents:
                    agent_file.unlink()
                    count += 1
                print(f"\n✓ {count} agente(s) eliminado(s)")
            else:
                print("\nOperación cancelada")
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(agents):
                agent_file = agents[idx]
                with open(agent_file, 'r') as f:
                    config = json.load(f)
                agent_name = config['name']
                
                confirm = input(f"\n⚠️  ¿Eliminar '{agent_name}'? (s/n): ").lower()
                if confirm == 's':
                    agent_file.unlink()
                    print(f"\n✓ Agente '{agent_name}' eliminado")
                else:
                    print("\nOperación cancelada")
            else:
                print("Número inválido")
        except ValueError:
            print("Entrada inválida")
    
    def chat_with_agent(self, agent: Agent):
        """Interfaz de chat con un agente"""
        print(f"\n=== Chat con {agent.name} ===")
        
        # Mostrar herramientas si las tiene
        if agent.get_tools():
            print(f"🔧 Herramientas: {len(agent.get_tools())} configurada(s)")
            for tool in agent.get_tools():
                tool_type = tool.get('type', 'unknown')
                # Si es una función, mostrar el nombre de la función
                if tool_type == 'function' and 'function' in tool:
                    func_name = tool['function'].get('name', 'unknown')
                    print(f"   - {tool_type} ({func_name})")
                else:
                    print(f"   - {tool_type}")
        
        print("\nEscribe 'salir' para terminar la conversación")
        print("Escribe 'stream' para activar modo streaming")
        print("Escribe 'reset' para reiniciar la conversación")
        print("Escribe 'historial' para ver el historial")
        print("Escribe 'tools' para ver las herramientas\n")
        
        streaming_mode = False
        
        while True:
            user_input = input("Tú: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'salir':
                print("\n¡Hasta luego!")
                break
            
            if user_input.lower() == 'stream':
                streaming_mode = not streaming_mode
                print(f"\nModo streaming: {'activado' if streaming_mode else 'desactivado'}\n")
                continue
            
            if user_input.lower() == 'reset':
                agent.reset_conversation()
                print("\n✓ Conversación reiniciada\n")
                continue
            
            if user_input.lower() == 'historial':
                print("\n=== Historial de Conversación ===")
                for msg in agent.get_history():
                    role = msg['role'].capitalize()
                    content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
                    print(f"{role}: {content}")
                print()
                continue
            
            if user_input.lower() == 'tools':
                print("\n=== Herramientas del Agente ===")
                tools = agent.get_tools()
                if tools:
                    for i, tool in enumerate(tools, 1):
                        tool_type = tool.get('type', 'unknown')
                        print(f"\n{i}. Tipo: {tool_type}")
                        
                        if tool_type == 'web_search' and 'web_search' in tool:
                            config = tool['web_search']
                            print(f"   Motor: {config.get('search_engine', 'N/A')}")
                            print(f"   Resultados: {config.get('count', 'N/A')}")
                            print(f"   Filtro de tiempo: {config.get('search_recency_filter', 'N/A')}")
                        
                        elif tool_type == 'function' and 'function' in tool:
                            func = tool['function']
                            print(f"   Nombre: {func.get('name', 'N/A')}")
                            print(f"   Descripción: {func.get('description', 'N/A')}")
                        
                        elif tool_type == 'code_interpreter':
                            print(f"   Permite ejecutar código Python")
                        
                        elif tool_type == 'drawing_tool':
                            print(f"   Permite generar imágenes")
                else:
                    print("No hay herramientas configuradas")
                print()
                continue
            
            if streaming_mode:
                print(f"\n{agent.name}: ", end="", flush=True)
                for chunk in agent.chat_stream(user_input):
                    print(chunk, end="", flush=True)
                print("\n")
            else:
                # Mostrar indicador de carga mientras procesa
                loader = LoadingIndicator(f"{agent.name} pensando")
                loader.start()
                
                try:
                    response = agent.chat(user_input)
                finally:
                    loader.stop()
                
                print(f"{agent.name}: {response}\n")
    
    def main_menu(self):
        """Menú principal del gestor de agentes"""
        while True:
            print("\n" + "=" * 50)
            print("    SISTEMA DE GESTIÓN DE AGENTES Z.AI")
            print("=" * 50)
            
            # Mostrar estado de debug
            if DebugConfig.level != DebugLevel.NONE:
                print(f"🐛 DEBUG: {DebugConfig.level.name}")
            
            print("\n=== Menú Principal ===")
            print("1. Crear agente personalizado")
            print("2. Usar agente predefinido")
            print("3. Cargar agente guardado")
            print("4. Listar agentes guardados")
            print("5. Gestionar herramientas de agentes")
            print("6. Eliminar agentes guardados")
            print("7. Configurar Debug")
            print("8. Salir")
            
            choice = input("\nSelecciona una opción: ").strip()
            
            if choice == '1':
                agent = self.create_custom_agent()
                if agent:
                    self.current_agent = agent
                    self.chat_with_agent(agent)
            
            elif choice == '2':
                agent = self.create_predefined_agent()
                if agent:
                    self.current_agent = agent
                    self.chat_with_agent(agent)
            
            elif choice == '3':
                agent = self.load_saved_agent()
                if agent:
                    self.current_agent = agent
                    self.chat_with_agent(agent)
            
            elif choice == '4':
                self.list_saved_agents()
            
            elif choice == '5':
                self.manage_agent_tools()
            
            elif choice == '6':
                self.delete_saved_agents()
            
            elif choice == '7':
                self.configure_debug()
            
            elif choice == '8':
                print("\n¡Hasta luego!")
                break
            
            else:
                print("\nOpción inválida. Intenta de nuevo.")
    
    def configure_debug(self):
        """Configurar nivel de debug"""
        print("\n=== Configurar Debug ===")
        print("0. Desactivado (NONE)")
        print("1. Básico (decisiones DSPy + tool calls)")
        print("2. Detallado (+ historial)")
        print("3. Verbose (todo)")
        print("4. Ver estado actual")
        
        choice = input("\nSelecciona nivel: ").strip()
        
        if choice == '0':
            DebugConfig.set_level(DebugLevel.NONE)
            print("✓ Debug desactivado")
        elif choice == '1':
            DebugConfig.set_level(DebugLevel.BASIC)
            print("✓ Debug BÁSICO activado")
        elif choice == '2':
            DebugConfig.set_level(DebugLevel.DETAILED)
            print("✓ Debug DETALLADO activado")
        elif choice == '3':
            DebugConfig.set_level(DebugLevel.VERBOSE)
            print("✓ Debug VERBOSE activado")
        elif choice == '4':
            DebugConfig.print_status()
        else:
            print("Opción inválida")
    
    def run(self):
        """Ejecutar el sistema de gestión de agentes"""
        self.main_menu()


if __name__ == "__main__":
    manager = AgentManager()
    manager.run()
