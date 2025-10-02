from zai import ZaiClient
from dotenv import load_dotenv
import os
import json
from debug_config import DebugConfig, debug_print

load_dotenv()

class Agent:
    """Clase para crear y gestionar agentes personalizados con Z.AI"""
    
    def __init__(self, name: str, instructions: str, model: str = "glm-4.6", tools: list = None):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.tools = tools or []  # Lista de herramientas disponibles
        self.conversation_history = []
        self.client = ZaiClient(api_key=os.getenv("ZAI_API_KEY"))
        
        # Generar instrucciones completas con información de herramientas
        full_instructions = self._build_instructions_with_tools(instructions)
        
        # Debug: Mostrar instrucciones
        if DebugConfig.show_instructions:
            debug_print("=== INSTRUCCIONES COMPLETAS ===")
            debug_print(full_instructions)
            debug_print("=" * 70)
        
        # Inicializar con las instrucciones del sistema
        self.conversation_history.append({
            "role": "system",
            "content": full_instructions
        })
    
    def _build_instructions_with_tools(self, base_instructions: str) -> str:
        """Construye instrucciones completas incluyendo información de herramientas"""
        if not self.tools:
            return base_instructions
        
        tools_info = "\n\n=== HERRAMIENTAS DISPONIBLES ===\n"
        tools_info += "Tienes acceso a las siguientes herramientas:\n\n"
        
        for tool in self.tools:
            tool_type = tool.get('type', 'unknown')
            
            if tool_type == 'web_search':
                tools_info += "• WEB SEARCH: Puedes buscar información actualizada en internet.\n"
                tools_info += "  Úsala cuando necesites datos actuales, noticias, precios, o información que cambia frecuentemente.\n\n"
            
            elif tool_type == 'function' and 'function' in tool:
                func = tool['function']
                func_name = func.get('name', 'unknown')
                func_desc = func.get('description', 'Sin descripción')
                tools_info += f"• {func_name.upper()}: {func_desc}\n"
                tools_info += f"  Úsala cuando el usuario te lo solicite explícitamente.\n\n"
            
            elif tool_type == 'code_interpreter':
                tools_info += "• CODE INTERPRETER: Puedes ejecutar código Python.\n"
                tools_info += "  Úsala para cálculos complejos, análisis de datos, o cuando necesites programar.\n\n"
            
            elif tool_type == 'drawing_tool':
                tools_info += "• DRAWING TOOL: Puedes generar imágenes.\n"
                tools_info += "  Úsala cuando te pidan crear visualizaciones o imágenes.\n\n"
            
            elif tool_type == 'function':
                func_name = tool.get('function', {}).get('name', '')
                if 'selenium' in func_name:
                    if func_name == 'selenium_navigate':
                        tools_info += "• SELENIUM NAVIGATE: Navega a páginas web.\n"
                    elif func_name == 'selenium_get_text':
                        tools_info += "• SELENIUM GET TEXT: Extrae TODO el texto de la página actual.\n"
                        tools_info += "  IMPORTANTE: Úsala SIEMPRE después de navegar para obtener el contenido.\n"
                    elif func_name == 'selenium_find_text':
                        tools_info += "• SELENIUM FIND TEXT: Busca elementos específicos en la página.\n"
                    elif func_name == 'selenium_screenshot':
                        tools_info += "• SELENIUM SCREENSHOT: Toma capturas de pantalla.\n"
                elif func_name == 'send_telegram_message':
                    tools_info += "• SEND_TELEGRAM_MESSAGE: Envía mensajes por Telegram.\n"
                    tools_info += "  Úsala cuando el usuario te lo solicite explícitamente.\n"
                elif 'task_' in func_name:
                    if func_name == 'task_list':
                        tools_info += f"• TASK_LIST: Lista TUS tareas asignadas (pendientes y completadas).\n"
                        tools_info += f"  ⚠️ IMPORTANTE: Úsala PRIMERO cuando el usuario diga 'realiza tus tareas'.\n"
                        tools_info += f"  💡 TIP: Pasa agent_name='{self.name}' para ver SOLO tus tareas.\n"
                    elif func_name == 'task_add':
                        tools_info += "• TASK_ADD: Agrega una nueva tarea.\n"
                    elif func_name == 'task_complete':
                        tools_info += "• TASK_COMPLETE: Marca una tarea como completada.\n"
                        tools_info += "  Úsala DESPUÉS de completar cada tarea.\n"
                    elif func_name == 'task_delete':
                        tools_info += "• TASK_DELETE: Elimina una tarea.\n"
                tools_info += "\n"
        
        tools_info += "IMPORTANTE: Usa las herramientas apropiadas según la tarea. Si no estás seguro, pregunta al usuario."
        
        return base_instructions + tools_info
    
    def chat(self, message: str, temperature: float = 0.7, max_tokens: int = 2000, use_tools: bool = None, max_tool_iterations: int = 5, timeout: int = 60) -> str:
        """
        Envía un mensaje al agente y obtiene una respuesta
        
        Args:
            message: El mensaje del usuario
            temperature: Controla la aleatoriedad (0.0 - 1.0)
            max_tokens: Número máximo de tokens en la respuesta
            use_tools: Si es True, usa las herramientas configuradas. Si es None, usa automáticamente si hay herramientas.
            max_tool_iterations: Máximo número de iteraciones de tool calls (default: 5)
            
        Returns:
            La respuesta del agente
        """
        # Debug: Mostrar mensaje del usuario
        debug_print(f"Usuario: {message}", "show_tool_calls")
        
        # Agregar mensaje del usuario al historial
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # Determinar si usar herramientas
        should_use_tools = use_tools if use_tools is not None else len(self.tools) > 0
        
        try:
            iteration = 0
            while iteration < max_tool_iterations:
                iteration += 1
                
                # Crear solicitud de chat
                request_params = {
                    "model": self.model,
                    "messages": self.conversation_history,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                
                # Agregar herramientas si están disponibles
                if should_use_tools and self.tools:
                    request_params["tools"] = self.tools
                
                # Intentar con timeout y reintentos
                max_retries = 2
                for retry in range(max_retries):
                    try:
                        response = self.client.chat.completions.create(**request_params)
                        response_message = response.choices[0].message
                        finish_reason = response.choices[0].finish_reason
                        break  # Éxito, salir del loop
                    except Exception as e:
                        if retry < max_retries - 1:
                            if DebugConfig.show_retries:
                                print(f"\n⚠️  Reintentando... ({retry + 1}/{max_retries})")
                            continue
                        else:
                            raise  # Último intento falló, propagar error
                
                # Agregar respuesta del asistente al historial
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response_message.content,
                    "tool_calls": getattr(response_message, 'tool_calls', None)
                })
                
                # Si no hay tool calls, devolver la respuesta
                if finish_reason != 'tool_calls' or not hasattr(response_message, 'tool_calls'):
                    return response_message.content or "Sin respuesta"
                
                # Procesar tool calls
                tool_calls = response_message.tool_calls
                if not tool_calls:
                    return response_message.content or "Sin respuesta"
                
                # Ejecutar cada tool call
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Debug: Mostrar tool call
                    if DebugConfig.show_tool_calls:
                        debug_print(f"🔧 Ejecutando: {function_name}")
                        debug_print(f"   Argumentos: {function_args}")
                    
                    # Ejecutar la función
                    function_response = self._execute_tool(function_name, function_args)
                    
                    # Debug: Mostrar resultado
                    if DebugConfig.show_tool_calls:
                        debug_print(f"   Resultado: {function_response}")
                    
                    # Agregar resultado al historial
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps(function_response, ensure_ascii=False)
                    })
                
                # Continuar el loop para obtener la respuesta final del agente
            
            return "Se alcanzó el límite máximo de iteraciones de herramientas"
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _execute_tool(self, function_name: str, arguments: dict) -> dict:
        """
        Ejecuta una herramienta/función
        
        Args:
            function_name: Nombre de la función a ejecutar
            arguments: Argumentos de la función
            
        Returns:
            Resultado de la ejecución
        """
        try:
            # Telegram
            if function_name == 'send_telegram_message':
                from telegram_handler import send_telegram_message
                return send_telegram_message(
                    message=arguments.get('message'),
                    parse_mode=arguments.get('parse_mode')
                )
            
            # Selenium - Navegación
            elif function_name == 'selenium_navigate':
                from selenium_handler import selenium_navigate
                return selenium_navigate(arguments.get('url'))
            
            # Selenium - Obtener texto
            elif function_name == 'selenium_get_text':
                from selenium_handler import selenium_get_text
                return selenium_get_text()
            
            # Selenium - Buscar elemento
            elif function_name == 'selenium_find_text':
                from selenium_handler import selenium_find_text
                return selenium_find_text(
                    arguments.get('selector'),
                    arguments.get('by', 'css')
                )
            
            # Selenium - Captura de pantalla
            elif function_name == 'selenium_screenshot':
                from selenium_handler import selenium_screenshot
                return selenium_screenshot(arguments.get('filename', 'screenshot.png'))
            
            # Tareas - Agregar
            elif function_name == 'task_add':
                from task_manager import task_add
                return task_add(arguments.get('description'))
            
            # Tareas - Completar
            elif function_name == 'task_complete':
                from task_manager import task_complete
                return task_complete(arguments.get('task_id'))
            
            # Tareas - Listar
            elif function_name == 'task_list':
                from task_manager import task_list
                # Pasar el nombre del agente si está disponible
                agent_name = arguments.get('agent_name', self.name)
                return task_list(agent_name=agent_name)
            
            # Tareas - Eliminar
            elif function_name == 'task_delete':
                from task_manager import task_delete
                return task_delete(arguments.get('task_id'))
            
            # Web Search - Z.AI maneja esto automáticamente
            # No necesitamos ejecutarlo manualmente
            elif function_name == 'web_search':
                return {
                    'success': True,
                    'message': 'Web search ejecutado por Z.AI',
                    'note': 'Los resultados se incluyen automáticamente en la respuesta'
                }
            
            # Agregar más funciones aquí según sea necesario
            else:
                return {
                    'success': False,
                    'error': f'Función desconocida: {function_name}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error ejecutando {function_name}: {str(e)}'
            }
    
    def chat_stream(self, message: str, temperature: float = 0.7, max_tokens: int = 2000, use_tools: bool = None):
        """
        Envía un mensaje al agente y obtiene una respuesta en streaming
        
        Args:
            message: El mensaje del usuario
            temperature: Controla la aleatoriedad (0.0 - 1.0)
            max_tokens: Número máximo de tokens en la respuesta
            use_tools: Si es True, usa las herramientas configuradas. Si es None, usa automáticamente si hay herramientas.
            
        Yields:
            Fragmentos de la respuesta del agente
        """
        # Debug: Mostrar mensaje del usuario
        debug_print(f"[STREAM] Usuario: {message}", "show_tool_calls")
        
        # Agregar mensaje del usuario al historial
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # Determinar si usar herramientas
        should_use_tools = use_tools if use_tools is not None else len(self.tools) > 0
        
        try:
            # Crear solicitud de chat en streaming
            request_params = {
                "model": self.model,
                "messages": self.conversation_history,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True
            }
            
            # Agregar herramientas si están disponibles
            if should_use_tools and self.tools:
                request_params["tools"] = self.tools
            
            response = self.client.chat.completions.create(**request_params)
            
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            # Agregar respuesta completa al historial
            self.conversation_history.append({
                "role": "assistant",
                "content": full_response
            })
            
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def reset_conversation(self):
        """Reinicia la conversación manteniendo las instrucciones del sistema"""
        self.conversation_history = [{
            "role": "system",
            "content": self.instructions
        }]
    
    def get_history(self) -> list:
        """Obtiene el historial completo de la conversación"""
        return self.conversation_history
    
    def add_tool(self, tool: dict):
        """Agrega una herramienta al agente"""
        self.tools.append(tool)
        # Actualizar instrucciones del sistema
        self._update_system_instructions()
    
    def remove_tool(self, tool_type: str):
        """Remueve una herramienta por tipo"""
        self.tools = [t for t in self.tools if t.get('type') != tool_type]
        # Actualizar instrucciones del sistema
        self._update_system_instructions()
    
    def clear_tools(self):
        """Limpia todas las herramientas"""
        self.tools = []
        # Actualizar instrucciones del sistema
        self._update_system_instructions()
    
    def _update_system_instructions(self):
        """Actualiza las instrucciones del sistema cuando cambian las herramientas"""
        full_instructions = self._build_instructions_with_tools(self.instructions)
        # Actualizar el primer mensaje del historial (system prompt)
        if self.conversation_history and self.conversation_history[0]['role'] == 'system':
            self.conversation_history[0]['content'] = full_instructions
    
    def get_tools(self) -> list:
        """Obtiene la lista de herramientas configuradas"""
        return self.tools
    
    def save_agent(self, filename: str):
        """Guarda la configuración del agente en un archivo JSON"""
        agent_config = {
            "name": self.name,
            "instructions": self.instructions,
            "model": self.model,
            "tools": self.tools
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(agent_config, f, indent=2, ensure_ascii=False)
        print(f"Agente guardado en: {filename}")
    
    @classmethod
    def load_agent(cls, filename: str):
        """Carga un agente desde un archivo JSON"""
        with open(filename, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return cls(
            name=config["name"],
            instructions=config["instructions"],
            model=config.get("model", "glm-4.6"),
            tools=config.get("tools", [])
        )
    
    @staticmethod
    def delete_agent(filename: str):
        """Elimina un archivo de agente guardado"""
        import os
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Agente eliminado: {filename}")
            return True
        else:
            print(f"Archivo no encontrado: {filename}")
            return False
    
    def __repr__(self):
        return f"Agent(name='{self.name}', model='{self.model}')"


# Función auxiliar para crear agentes predefinidos
def create_math_tutor():
    """Crea un agente tutor de matemáticas"""
    return Agent(
        name="Math Tutor",
        instructions="You provide help with math problems. Explain your reasoning at each step and include examples"
    )

def create_code_reviewer():
    """Crea un agente revisor de código"""
    return Agent(
        name="Code Reviewer",
        instructions="You are an expert code reviewer. Analyze code for bugs, performance issues, and best practices. Provide constructive feedback with examples."
    )

def create_creative_writer():
    """Crea un agente escritor creativo"""
    return Agent(
        name="Creative Writer",
        instructions="You are a creative writer. Help users craft engaging stories, poems, and creative content. Be imaginative and descriptive."
    )


if __name__ == "__main__":
    # Ejemplo de uso
    print("=== Ejemplo de Creación de Agente ===\n")
    
    # Crear un agente tutor de matemáticas
    math_tutor = Agent(
        name="Math Tutor",
        instructions="You provide help with math problems. Explain your reasoning at each step and include examples"
    )
    
    print(f"Agente creado: {math_tutor}\n")
    
    # Hacer una pregunta
    question = "Can you help me solve this equation: 2x + 5 = 13?"
    print(f"Usuario: {question}\n")
    
    response = math_tutor.chat(question)
    print(f"{math_tutor.name}: {response}\n")
    
    # Seguimiento
    followup = "Can you show me another example?"
    print(f"Usuario: {followup}\n")
    
    response = math_tutor.chat(followup)
    print(f"{math_tutor.name}: {response}\n")
    
    # Guardar el agente
    math_tutor.save_agent("math_tutor_agent.json")
