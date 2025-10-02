"""
Evaluador de DSPy - Verifica que las decisiones sean correctas
"""

import dspy
from dspy_agent import ToolExecutor, DSPyAgent
from dspy_examples import ALL_EXAMPLES, get_examples_by_tool
from agent_creator import Agent
from tools import create_web_search_tool, create_telegram_tool, create_code_interpreter_tool
import os
from dotenv import load_dotenv

load_dotenv()


class DSPyEvaluator:
    """Evalúa la precisión de las decisiones de DSPy"""
    
    def __init__(self):
        self.tool_executor = ToolExecutor(use_examples=True)
        self.results = []
    
    def evaluate_example(self, example):
        """
        Evalúa un ejemplo individual
        
        Args:
            example: Ejemplo de DSPy
            
        Returns:
            dict con resultados de la evaluación
        """
        # Convertir available_tools string a lista de dicts
        # (para que funcione con _format_tools)
        tools_list = []  # Simplificado para evaluación
        
        # Obtener decisión de DSPy
        decision = self.tool_executor.forward(
            user_query=example.user_query,
            available_tools=example.available_tools,  # Pasar como string
            context=example.conversation_context
        )
        
        # Comparar con la respuesta esperada
        correct_tool = decision['tool_name'] == example.tool_name
        correct_decision = (
            (decision['should_use_tool'] and example.should_use_tool == 'yes') or
            (not decision['should_use_tool'] and example.should_use_tool == 'no')
        )
        
        result = {
            'query': example.user_query,
            'expected_tool': example.tool_name,
            'predicted_tool': decision['tool_name'],
            'expected_use': example.should_use_tool,
            'predicted_use': 'yes' if decision['should_use_tool'] else 'no',
            'correct_tool': correct_tool,
            'correct_decision': correct_decision,
            'reasoning': decision['reasoning'],
            'expected_reasoning': example.reasoning
        }
        
        return result
    
    def evaluate_all(self, examples=None):
        """
        Evalúa todos los ejemplos
        
        Args:
            examples: Lista de ejemplos (usa ALL_EXAMPLES por defecto)
            
        Returns:
            dict con métricas de evaluación
        """
        if examples is None:
            examples = ALL_EXAMPLES
        
        print("=" * 70)
        print("  EVALUACIÓN DE DSPY")
        print("=" * 70)
        print(f"\nEvaluando {len(examples)} ejemplos...\n")
        
        self.results = []
        correct_tools = 0
        correct_decisions = 0
        
        for i, example in enumerate(examples, 1):
            print(f"[{i}/{len(examples)}] Evaluando: {example.user_query[:50]}...")
            
            try:
                result = self.evaluate_example(example)
                self.results.append(result)
                
                if result['correct_tool']:
                    correct_tools += 1
                if result['correct_decision']:
                    correct_decisions += 1
                
                # Mostrar si hay error
                if not result['correct_tool'] or not result['correct_decision']:
                    print(f"    ❌ Error:")
                    print(f"       Esperado: {result['expected_tool']}")
                    print(f"       Obtenido: {result['predicted_tool']}")
                else:
                    print(f"    ✅ Correcto")
                    
            except Exception as e:
                print(f"    ⚠️  Error: {e}")
                self.results.append({
                    'query': example.user_query,
                    'error': str(e),
                    'correct_tool': False,
                    'correct_decision': False
                })
        
        # Calcular métricas
        total = len(examples)
        accuracy_tool = (correct_tools / total * 100) if total > 0 else 0
        accuracy_decision = (correct_decisions / total * 100) if total > 0 else 0
        
        metrics = {
            'total_examples': total,
            'correct_tools': correct_tools,
            'correct_decisions': correct_decisions,
            'accuracy_tool': accuracy_tool,
            'accuracy_decision': accuracy_decision,
            'results': self.results
        }
        
        return metrics
    
    def print_report(self, metrics):
        """Imprime un reporte detallado de la evaluación"""
        print("\n" + "=" * 70)
        print("  REPORTE DE EVALUACIÓN")
        print("=" * 70)
        
        print(f"\n📊 Métricas Generales:")
        print(f"   Total de ejemplos: {metrics['total_examples']}")
        print(f"   Herramientas correctas: {metrics['correct_tools']}/{metrics['total_examples']}")
        print(f"   Decisiones correctas: {metrics['correct_decisions']}/{metrics['total_examples']}")
        print(f"\n   🎯 Precisión (Herramienta): {metrics['accuracy_tool']:.1f}%")
        print(f"   🎯 Precisión (Decisión): {metrics['accuracy_decision']:.1f}%")
        
        # Mostrar errores
        errors = [r for r in metrics['results'] if not r.get('correct_tool', True)]
        if errors:
            print(f"\n❌ Errores ({len(errors)}):")
            for err in errors:
                print(f"\n   Query: {err['query']}")
                print(f"   Esperado: {err.get('expected_tool', 'N/A')}")
                print(f"   Obtenido: {err.get('predicted_tool', 'N/A')}")
                if 'error' in err:
                    print(f"   Error: {err['error']}")
        
        # Evaluación final
        print("\n" + "=" * 70)
        if metrics['accuracy_tool'] >= 90:
            print("  ✅ EXCELENTE - DSPy está funcionando muy bien")
        elif metrics['accuracy_tool'] >= 70:
            print("  ⚠️  BUENO - DSPy funciona pero puede mejorar")
        else:
            print("  ❌ NECESITA MEJORA - DSPy no está decidiendo correctamente")
        print("=" * 70)
    
    def evaluate_by_category(self):
        """Evalúa por categoría de herramienta"""
        categories = {
            'web_search': get_examples_by_tool('web_search'),
            'telegram': get_examples_by_tool('telegram'),
            'code': get_examples_by_tool('code'),
            'multi': get_examples_by_tool('multi')
        }
        
        print("\n" + "=" * 70)
        print("  EVALUACIÓN POR CATEGORÍA")
        print("=" * 70)
        
        for category, examples in categories.items():
            if not examples:
                continue
                
            print(f"\n### {category.upper()}")
            metrics = self.evaluate_all(examples)
            print(f"   Precisión: {metrics['accuracy_tool']:.1f}%")


def test_live_agent():
    """Prueba con un agente real"""
    print("\n" + "=" * 70)
    print("  TEST: Agente Real con DSPy")
    print("=" * 70)
    
    # Crear agente con DSPy
    from dspy_agent import create_dspy_agent
    
    agent = create_dspy_agent(
        name="Test Agent",
        instructions="Eres un asistente útil",
        tools=[
            create_web_search_tool(),
            create_telegram_tool()
        ]
    )
    
    # Casos de prueba
    test_cases = [
        {
            'query': '¿Cuál es el precio actual de Ethereum?',
            'expected_tool': 'web_search',
            'reason': 'Precio actual requiere búsqueda web'
        },
        {
            'query': 'Envíame un mensaje de prueba',
            'expected_tool': 'send_telegram_message',
            'reason': 'Usuario pide explícitamente enviar mensaje'
        },
        {
            'query': '¿Qué es Ethereum?',
            'expected_tool': 'none',
            'reason': 'Pregunta conceptual, no requiere herramientas'
        }
    ]
    
    print("\nProbando casos en vivo...\n")
    
    for i, test in enumerate(test_cases, 1):
        print(f"{i}. Query: {test['query']}")
        print(f"   Herramienta esperada: {test['expected_tool']}")
        print(f"   Razón: {test['reason']}")
        print(f"   Probando...")
        
        # Aquí normalmente llamarías a agent.chat()
        # pero solo mostramos la decisión de DSPy
        print(f"   ⏭️  (Saltando ejecución real para no consumir créditos)\n")


def main():
    """Ejecuta todas las evaluaciones"""
    print("\n" + "=" * 70)
    print("  SISTEMA DE EVALUACIÓN DSPY")
    print("=" * 70)
    
    # Configurar DSPy
    try:
        lm = dspy.LM(
            model='openai/glm-4.6',
            api_base='https://api.z.ai/api/paas/v4',
            api_key=os.getenv('ZAI_API_KEY')
        )
        dspy.configure(lm=lm)
        print("\n✓ DSPy configurado correctamente\n")
    except Exception as e:
        print(f"\n❌ Error configurando DSPy: {e}\n")
        return
    
    # Crear evaluador
    evaluator = DSPyEvaluator()
    
    # Opción 1: Evaluar todos los ejemplos
    print("\n🔍 Opción 1: Evaluar todos los ejemplos")
    metrics = evaluator.evaluate_all()
    evaluator.print_report(metrics)
    
    # Opción 2: Evaluar por categoría
    # print("\n🔍 Opción 2: Evaluar por categoría")
    # evaluator.evaluate_by_category()
    
    # Opción 3: Test con agente real
    # test_live_agent()


if __name__ == "__main__":
    main()
