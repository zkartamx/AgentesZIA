"""
Agente mejorado con DSPy para mejor uso de herramientas
"""

import dspy
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
import json
import warnings
from debug_config import DebugConfig, debug_print

# Suprimir warnings de DSPy
warnings.filterwarnings('ignore', module='dspy')
warnings.filterwarnings('ignore', category=UserWarning, module='dspy')

# Suprimir warnings específicos de DSPy
import logging
logging.getLogger('dspy').setLevel(logging.ERROR)

load_dotenv()


class ToolDecider(dspy.Signature):
    """Decide si se debe usar una herramienta y cuál"""
    
    user_query = dspy.InputField(desc="La pregunta o solicitud del usuario")
    available_tools = dspy.InputField(desc="Lista de herramientas disponibles con sus descripciones")
    conversation_context = dspy.InputField(desc="Contexto de la conversación previa")
    
    should_use_tool = dspy.OutputField(desc="'yes' si debe usar una herramienta, 'no' si no")
    tool_name = dspy.OutputField(desc="Nombre de la herramienta a usar (o 'none')")
    reasoning = dspy.OutputField(desc="Razonamiento de por qué usar o no la herramienta")


class ToolExecutor(dspy.Module):
    """Ejecutor de herramientas con DSPy"""
    
    def __init__(self, use_examples: bool = True):
        super().__init__()
        
        if use_examples:
            # Usar ChainOfThoughtWithHint para incluir ejemplos
            self.decide_tool = dspy.ChainOfThought(ToolDecider)
            self._load_examples()
        else:
            self.decide_tool = dspy.ChainOfThought(ToolDecider)
    
    def _load_examples(self):
        """Carga ejemplos de entrenamiento"""
        try:
            from dspy_examples import ALL_EXAMPLES
            self.examples = ALL_EXAMPLES
            print(f"✓ {len(ALL_EXAMPLES)} ejemplos de entrenamiento cargados")
        except ImportError:
            self.examples = []
            print("⚠️  No se pudieron cargar ejemplos")
    
    def forward(self, user_query: str, available_tools, context: str = ""):
        """
        Decide si usar una herramienta y cuál
        
        Args:
            user_query: Pregunta del usuario
            available_tools: Lista de herramientas disponibles o string
            context: Contexto de la conversación
            
        Returns:
            Decisión sobre qué herramienta usar
        """
        # Formatear herramientas disponibles
        if isinstance(available_tools, str):
            tools_desc = available_tools  # Ya es string
        else:
            tools_desc = self._format_tools(available_tools)
        
        # Decidir qué herramienta usar
        decision = self.decide_tool(
            user_query=user_query,
            available_tools=tools_desc,
            conversation_context=context or "Sin contexto previo"
        )
        
        return {
            'should_use_tool': decision.should_use_tool.lower() == 'yes',
            'tool_name': decision.tool_name,
            'reasoning': decision.reasoning
        }
    
    def _format_tools(self, tools: List[Dict]) -> str:
        """Formatea las herramientas para el prompt"""
        if not tools:
            return "No hay herramientas disponibles"
        
        formatted = []
        for tool in tools:
            tool_type = tool.get('type', 'unknown')
            
            if tool_type == 'web_search':
                formatted.append("- web_search: Busca información actualizada en internet. Úsala para precios, noticias, datos actuales.")
            
            elif tool_type == 'function' and 'function' in tool:
                func = tool['function']
                name = func.get('name', 'unknown')
                desc = func.get('description', 'Sin descripción')
                formatted.append(f"- {name}: {desc}")
            
            elif tool_type == 'code_interpreter':
                formatted.append("- code_interpreter: Ejecuta código Python para cálculos y análisis.")
            
            elif tool_type == 'drawing_tool':
                formatted.append("- drawing_tool: Genera imágenes y visualizaciones.")
        
        return "\n".join(formatted)


class DSPyAgent:
    """Agente mejorado con DSPy para mejor toma de decisiones"""
    
    def __init__(self, base_agent, debug: bool = False):
        """
        Inicializa el agente DSPy
        
        Args:
            base_agent: Instancia del agente base (Agent)
            debug: Si True, muestra las decisiones de DSPy
        """
        self.base_agent = base_agent
        self.debug = debug
        
        # Configurar DSPy con Z.AI
        self._configure_dspy()
        
        # Crear ejecutor de herramientas
        self.tool_executor = ToolExecutor()
    
    def _configure_dspy(self):
        """Configura DSPy para usar Z.AI"""
        try:
            # Configurar LM con OpenAI-compatible API
            lm = dspy.LM(
                model='openai/glm-4.6',
                api_base='https://api.z.ai/api/paas/v4',
                api_key=os.getenv('ZAI_API_KEY')
            )
            dspy.configure(lm=lm)
            print("✓ DSPy configurado con Z.AI")
        except Exception as e:
            print(f"⚠️  Error configurando DSPy: {e}")
            print("   Continuando sin DSPy...")
    
    def chat(self, message: str, **kwargs) -> str:
        """
        Chat mejorado con decisión inteligente de herramientas
        
        Args:
            message: Mensaje del usuario
            **kwargs: Argumentos adicionales para el chat
            
        Returns:
            Respuesta del agente
        """
        # Si no hay herramientas, usar chat normal
        if not self.base_agent.get_tools():
            return self.base_agent.chat(message, **kwargs)
        
        try:
            # Obtener contexto de la conversación
            context = self._get_context()
            
            # Decidir si usar herramientas (usar __call__ en lugar de forward)
            decision = self.tool_executor(
                user_query=message,
                available_tools=self.base_agent.get_tools(),
                context=context
            )
            
            # Mostrar decisión si debug está activo o si self.debug=True
            if self.debug or DebugConfig.show_dspy_decisions:
                print(f"\n🤖 DSPy Decision:")
                print(f"   Should use tool: {decision['should_use_tool']}")
                print(f"   Tool: {decision['tool_name']}")
                print(f"   Reasoning: {decision['reasoning']}\n")
            
            # Usar el chat normal del agente (que ya maneja tool calls)
            return self.base_agent.chat(message, **kwargs)
            
        except Exception as e:
            print(f"⚠️  Error en DSPy, usando chat normal: {e}")
            return self.base_agent.chat(message, **kwargs)
    
    def _get_context(self) -> str:
        """Obtiene el contexto de la conversación"""
        history = self.base_agent.get_history()
        if len(history) <= 1:
            return "Sin contexto previo"
        
        # Obtener últimos 3 mensajes
        recent = history[-3:]
        context_parts = []
        for msg in recent:
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            if content:
                context_parts.append(f"{role}: {content[:100]}")
        
        return " | ".join(context_parts)
    
    def __getattr__(self, name):
        """Delega atributos no encontrados al agente base"""
        return getattr(self.base_agent, name)


def create_dspy_agent(name: str, instructions: str, tools: List[Dict] = None, **kwargs):
    """
    Crea un agente mejorado con DSPy
    
    Args:
        name: Nombre del agente
        instructions: Instrucciones del agente
        tools: Lista de herramientas
        **kwargs: Argumentos adicionales
        
    Returns:
        DSPyAgent instance
    """
    from agent_creator import Agent
    
    # Crear agente base
    base_agent = Agent(
        name=name,
        instructions=instructions,
        tools=tools or [],
        **kwargs
    )
    
    # Envolver con DSPy
    return DSPyAgent(base_agent)


if __name__ == "__main__":
    print("=" * 70)
    print("  TEST: DSPy Agent")
    print("=" * 70)
    
    from tools import create_web_search_tool, create_telegram_tool
    
    # Crear agente con DSPy
    agent = create_dspy_agent(
        name="Asistente DSPy",
        instructions="Eres un asistente útil",
        tools=[
            create_web_search_tool(),
            create_telegram_tool()
        ]
    )
    
    print(f"\n✓ Agente DSPy creado: {agent.base_agent}")
    print(f"✓ Herramientas: {len(agent.base_agent.get_tools())}\n")
    
    # Test
    print("Test: ¿Cuál es el precio de Bitcoin?")
    print("-" * 70)
    
    # DSPy decidirá si usar web_search
    response = agent.chat("¿Cuál es el precio actual de Bitcoin?")
    print(f"\nRespuesta: {response}")
