"""
Módulo de herramientas (tools) para agentes Z.AI
Proporciona funciones para crear herramientas predefinidas
"""

def create_web_search_tool(
    search_prompt: str = None,
    count: int = 5,
    search_recency_filter: str = "noLimit",
    search_domain_filter: str = None,
    content_size: str = "high"
) -> dict:
    """
    Crea una herramienta de búsqueda web con el formato correcto de Z.AI
    
    Args:
        search_prompt: Instrucciones sobre cómo usar los resultados de búsqueda (opcional)
        count: Número de resultados a retornar (1-50, default: 5)
        search_recency_filter: Filtro de tiempo - "oneDay", "oneWeek", "oneMonth", "oneYear", "noLimit" (default)
        search_domain_filter: Filtrar por dominio específico (ej: "www.example.com")
        content_size: Tamaño del contenido - "high", "medium", "low" (default: "high")
    
    Returns:
        Diccionario con la configuración de la herramienta
    
    Ejemplo:
        tool = create_web_search_tool()
        agent = Agent(name="Researcher", instructions="...", tools=[tool])
        
        # Con configuración personalizada
        tool = create_web_search_tool(
            search_prompt="Summarize key information from search results",
            count=10,
            search_recency_filter="oneWeek"
        )
    """
    tool = {
        'type': 'web_search',
        'web_search': {
            'enable': 'True',  # CRÍTICO: Habilita la búsqueda web
            'search_engine': 'search-prime',  # Motor de búsqueda premium de Z.AI
            'search_result': 'True',  # Incluir resultados en la respuesta
            'count': str(count),  # Número de resultados
            'search_recency_filter': search_recency_filter,  # Filtro de tiempo
            'content_size': content_size  # Tamaño del contenido
        }
    }
    
    # Agregar prompt personalizado si se proporciona
    if search_prompt:
        tool['web_search']['search_prompt'] = search_prompt
    
    # Agregar filtro de dominio si se proporciona
    if search_domain_filter:
        tool['web_search']['search_domain_filter'] = search_domain_filter
    
    return tool


def create_code_interpreter_tool() -> dict:
    """
    Crea una herramienta de intérprete de código
    Permite al agente ejecutar código Python
    
    Returns:
        Diccionario con la configuración de la herramienta
    
    Ejemplo:
        tool = create_code_interpreter_tool()
        agent = Agent(name="Coder", instructions="...", tools=[tool])
    """
    return {
        'type': 'code_interpreter'
    }


def create_drawing_tool(enable_generation: bool = True) -> dict:
    """
    Crea una herramienta de generación de imágenes/dibujos
    
    Args:
        enable_generation: Si debe habilitar la generación
    
    Returns:
        Diccionario con la configuración de la herramienta
    
    Ejemplo:
        tool = create_drawing_tool()
        agent = Agent(name="Artist", instructions="...", tools=[tool])
    """
    return {
        'type': 'drawing_tool',
        'drawing_tool': {
            'generation': enable_generation
        }
    }


def create_telegram_tool() -> dict:
    """
    Crea una herramienta para enviar mensajes a Telegram
    
    Returns:
        Diccionario con la configuración de la herramienta
    
    Ejemplo:
        tool = create_telegram_tool()
        agent = Agent(name="Notifier", instructions="...", tools=[tool])
    
    Nota:
        Requiere configurar TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID en .env
    """
    return {
        'type': 'function',
        'function': {
            'name': 'send_telegram_message',
            'description': 'Envía un mensaje a través de un bot de Telegram',
            'parameters': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'El mensaje a enviar'
                    },
                    'parse_mode': {
                        'type': 'string',
                        'enum': ['Markdown', 'HTML'],
                        'description': 'Formato del mensaje (opcional)'
                    }
                },
                'required': ['message']
            }
        }
    }


def create_function_tool(name: str, description: str, parameters: dict) -> dict:
    """
    Crea una herramienta de función personalizada
    
    Args:
        name: Nombre de la función
        description: Descripción de lo que hace la función
        parameters: Esquema de parámetros (JSON Schema)
    
    Returns:
        Diccionario con la configuración de la herramienta
    
    Ejemplo:
        tool = create_function_tool(
            name="get_weather",
            description="Get the current weather in a location",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    }
                },
                "required": ["location"]
            }
        )
    """
    return {
        'type': 'function',
        'function': {
            'name': name,
            'description': description,
            'parameters': parameters
        }
    }


# Herramientas predefinidas comunes
TOOL_WEB_SEARCH = create_web_search_tool()
TOOL_CODE_INTERPRETER = create_code_interpreter_tool()
TOOL_DRAWING = create_drawing_tool()
TOOL_TELEGRAM = create_telegram_tool()


def get_available_tools() -> dict:
    """
    Obtiene un diccionario con todas las herramientas disponibles
    
    Returns:
        Diccionario con nombre y descripción de cada herramienta
    """
    return {
        'web_search': {
            'name': 'Web Search',
            'description': 'Permite al agente buscar información en la web',
            'function': create_web_search_tool
        },
        'code_interpreter': {
            'name': 'Code Interpreter',
            'description': 'Permite al agente ejecutar código Python',
            'function': create_code_interpreter_tool
        },
        'drawing_tool': {
            'name': 'Drawing Tool',
            'description': 'Permite al agente generar imágenes',
            'function': create_drawing_tool
        },
        'telegram': {
            'name': 'Telegram',
            'description': 'Permite al agente enviar mensajes a Telegram',
            'function': create_telegram_tool
        },
        'function': {
            'name': 'Custom Function',
            'description': 'Define una función personalizada',
            'function': create_function_tool
        }
    }


def print_available_tools():
    """Imprime todas las herramientas disponibles"""
    tools = get_available_tools()
    print("\n=== Herramientas Disponibles ===\n")
    for key, info in tools.items():
        print(f"• {info['name']}")
        print(f"  Tipo: {key}")
        print(f"  Descripción: {info['description']}\n")


if __name__ == "__main__":
    # Ejemplo de uso
    print("=" * 60)
    print("  DEMO: Herramientas para Agentes")
    print("=" * 60)
    
    print_available_tools()
    
    print("=" * 60)
    print("  Ejemplos de Creación")
    print("=" * 60)
    
    print("\n1. Web Search Tool:")
    tool1 = create_web_search_tool()
    print(f"   {tool1}")
    
    print("\n2. Code Interpreter Tool:")
    tool2 = create_code_interpreter_tool()
    print(f"   {tool2}")
    
    print("\n3. Drawing Tool:")
    tool3 = create_drawing_tool()
    print(f"   {tool3}")
    
    print("\n4. Custom Function Tool:")
    tool4 = create_function_tool(
        name="get_weather",
        description="Get current weather",
        parameters={
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    )
    print(f"   {tool4}")
