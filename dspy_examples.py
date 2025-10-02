"""
Ejemplos de entrenamiento para DSPy
Define casos de uso comunes para mejorar las decisiones del agente
"""

import dspy

# Ejemplos de cuándo usar web_search
WEB_SEARCH_EXAMPLES = [
    dspy.Example(
        user_query="¿Cuál es el precio actual de Bitcoin?",
        available_tools="web_search: Busca información actualizada en internet",
        conversation_context="Sin contexto previo",
        should_use_tool="yes",
        tool_name="web_search",
        reasoning="El usuario pregunta por el precio ACTUAL, que es información que cambia constantemente. Web search es necesaria para obtener datos en tiempo real."
    ).with_inputs("user_query", "available_tools", "conversation_context"),
    
    dspy.Example(
        user_query="¿Qué pasó hoy en las noticias?",
        available_tools="web_search: Busca información actualizada en internet",
        conversation_context="Sin contexto previo",
        should_use_tool="yes",
        tool_name="web_search",
        reasoning="Pregunta por noticias de HOY, requiere información actualizada que solo web search puede proporcionar."
    ).with_inputs("user_query", "available_tools", "conversation_context"),
    
    dspy.Example(
        user_query="Busca información sobre inteligencia artificial",
        available_tools="web_search: Busca información actualizada en internet",
        conversation_context="Sin contexto previo",
        should_use_tool="yes",
        tool_name="web_search",
        reasoning="Usuario pide explícitamente BUSCAR información, debe usar web_search."
    ).with_inputs("user_query", "available_tools", "conversation_context"),
    
    dspy.Example(
        user_query="¿Qué es Python?",
        available_tools="web_search: Busca información actualizada en internet",
        conversation_context="Sin contexto previo",
        should_use_tool="no",
        tool_name="none",
        reasoning="Pregunta general sobre Python que puede responderse con conocimiento base. No requiere búsqueda web."
    ).with_inputs("user_query", "available_tools", "conversation_context"),
    
    dspy.Example(
        user_query="Explícame qué es blockchain",
        available_tools="web_search: Busca información actualizada en internet",
        conversation_context="Sin contexto previo",
        tool_name="none",
        reasoning="Pregunta conceptual que puede responderse con conocimiento general. No necesita datos actualizados."
    ).with_inputs("user_query", "available_tools", "conversation_context"),
]

# Ejemplos de cuándo usar Selenium
SELENIUM_EXAMPLES = [
    dspy.Example(
        user_query="Navega a https://www.example.com",
        available_tools="selenium_navigate, web_search",
        conversation_context="",
        should_use_tool="yes",
        tool_name="selenium_navigate",
        reasoning="Usuario pide explícitamente navegar a una URL usando Selenium"
    ).with_inputs("user_query", "available_tools", "conversation_context"),
    
    dspy.Example(
        user_query="Realiza tus tareas pendientes",
        available_tools="task_list, task_complete, web_search",
        conversation_context="",
        should_use_tool="yes",
        tool_name="task_list",
        reasoning="Usuario pide realizar tareas. PRIMERO debo usar task_list para ver qué tareas tengo asignadas"
    ).with_inputs("user_query", "available_tools", "conversation_context"),
    
    dspy.Example(
        user_query="¿Qué tareas tienes?",
        available_tools="task_list, task_add",
        conversation_context="",
        should_use_tool="yes",
        tool_name="task_list",
        reasoning="Usuario pregunta por mis tareas. Debo usar task_list para mostrarlas"
    ).with_inputs("user_query", "available_tools", "conversation_context"),
    
    dspy.Example(
        user_query="Marca la tarea 1 como completada",
        available_tools="task_complete, task_list",
        conversation_context="Acabo de terminar la tarea #1",
        should_use_tool="yes",
        tool_name="task_complete",
        reasoning="Usuario pide marcar tarea como completada. Debo usar task_complete"
    ).with_inputs("user_query", "available_tools", "conversation_context"),
    
    dspy.Example(
        user_query="Notifícame cuando termines",
        available_tools="send_telegram_message: Envía un mensaje a través de un bot de Telegram",
        should_use_tool="yes",
        tool_name="send_telegram_message",
        reasoning="Usuario pide notificación, debe usar Telegram para enviar el aviso."
    ).with_inputs("user_query", "available_tools", "conversation_context"),
    
    dspy.Example(
        user_query="¿Puedes enviarme eso por mensaje?",
        available_tools="send_telegram_message: Envía un mensaje a través de un bot de Telegram",
        conversation_context="user: Dame un resumen | assistant: Aquí está el resumen...",
        should_use_tool="yes",
        tool_name="send_telegram_message",
        reasoning="Usuario pide enviar información por mensaje, debe usar Telegram."
    ).with_inputs("user_query", "available_tools", "conversation_context"),
]

# Ejemplos de múltiples herramientas
MULTI_TOOL_EXAMPLES = [
    dspy.Example(
        user_query="Busca el precio de Bitcoin y envíamelo por Telegram",
        available_tools="web_search: Busca información actualizada\nsend_telegram_message: Envía mensajes a Telegram",
        conversation_context="Sin contexto previo",
        should_use_tool="yes",
        tool_name="web_search",
        reasoning="Primero debe buscar el precio con web_search, luego enviará por Telegram en la siguiente iteración."
    ).with_inputs("user_query", "available_tools", "conversation_context"),
    
    dspy.Example(
        user_query="Investiga las noticias de hoy y notifícame lo importante",
        available_tools="web_search: Busca información actualizada\nsend_telegram_message: Envía mensajes a Telegram",
        conversation_context="Sin contexto previo",
        should_use_tool="yes",
        tool_name="web_search",
        reasoning="Primero debe investigar con web_search, luego notificará por Telegram."
    ).with_inputs("user_query", "available_tools", "conversation_context"),
]

# Ejemplos de code_interpreter
CODE_EXAMPLES = [
    dspy.Example(
        user_query="Calcula el factorial de 100",
        available_tools="code_interpreter: Ejecuta código Python",
        conversation_context="Sin contexto previo",
        should_use_tool="yes",
        tool_name="code_interpreter",
        reasoning="Cálculo matemático complejo que requiere ejecutar código Python."
    ).with_inputs("user_query", "available_tools", "conversation_context"),
    
    dspy.Example(
        user_query="Analiza estos datos y crea un gráfico",
        available_tools="code_interpreter: Ejecuta código Python",
        conversation_context="Sin contexto previo",
        should_use_tool="yes",
        tool_name="code_interpreter",
        reasoning="Análisis de datos y visualización requiere ejecutar código Python."
    ).with_inputs("user_query", "available_tools", "conversation_context"),
    
    dspy.Example(
        user_query="¿Cuánto es 2+2?",
        available_tools="code_interpreter: Ejecuta código Python",
        conversation_context="Sin contexto previo",
        should_use_tool="no",
        tool_name="none",
        reasoning="Cálculo simple que no requiere ejecutar código, puede responderse directamente."
    ).with_inputs("user_query", "available_tools", "conversation_context"),
]

# Combinar todos los ejemplos
ALL_EXAMPLES = (
    WEB_SEARCH_EXAMPLES +
    SELENIUM_EXAMPLES +
    MULTI_TOOL_EXAMPLES +
    CODE_EXAMPLES
)


def get_examples_by_tool(tool_name: str):
    """
    Obtiene ejemplos específicos para una herramienta
    
    Args:
        tool_name: Nombre de la herramienta ('web_search', 'telegram', 'code', 'all')
        
    Returns:
        Lista de ejemplos
    """
    if tool_name == 'web_search':
        return WEB_SEARCH_EXAMPLES
    elif tool_name == 'telegram':
        return TELEGRAM_EXAMPLES
    elif tool_name == 'code':
        return CODE_EXAMPLES
    elif tool_name == 'multi':
        return MULTI_TOOL_EXAMPLES
    elif tool_name == 'all':
        return ALL_EXAMPLES
    else:
        return []


def print_examples():
    """Imprime todos los ejemplos de entrenamiento"""
    print("=" * 70)
    print("  EJEMPLOS DE ENTRENAMIENTO DSPY")
    print("=" * 70)
    
    categories = [
        ("Web Search", WEB_SEARCH_EXAMPLES),
        ("Telegram", TELEGRAM_EXAMPLES),
        ("Múltiples Herramientas", MULTI_TOOL_EXAMPLES),
        ("Code Interpreter", CODE_EXAMPLES)
    ]
    
    for category, examples in categories:
        print(f"\n### {category} ({len(examples)} ejemplos)")
        print("-" * 70)
        for i, ex in enumerate(examples, 1):
            print(f"\n{i}. Query: {ex.user_query}")
            print(f"   Usar herramienta: {ex.should_use_tool}")
            print(f"   Herramienta: {ex.tool_name}")
            print(f"   Razón: {ex.reasoning[:80]}...")
    
    print(f"\n{'=' * 70}")
    print(f"Total de ejemplos: {len(ALL_EXAMPLES)}")


if __name__ == "__main__":
    print_examples()
