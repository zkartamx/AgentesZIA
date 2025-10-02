"""
Configuración de Debug para el Sistema de Agentes
Permite activar/desactivar diferentes niveles de logging
"""

import os
from enum import Enum


class DebugLevel(Enum):
    """Niveles de debug disponibles"""
    NONE = 0
    BASIC = 1      # Muestra decisiones principales
    DETAILED = 2   # Muestra detalles de herramientas
    VERBOSE = 3    # Muestra todo (historial, requests, etc.)


class DebugConfig:
    """Configuración global de debug"""
    
    # Nivel de debug actual
    level = DebugLevel.NONE
    
    # Flags individuales
    show_dspy_decisions = False
    show_tool_calls = False
    show_history = False
    show_instructions = False
    show_api_calls = False
    show_retries = False
    
    @classmethod
    def set_level(cls, level: DebugLevel):
        """
        Configura el nivel de debug
        
        Args:
            level: Nivel de debug (NONE, BASIC, DETAILED, VERBOSE)
        """
        cls.level = level
        
        # Configurar flags según el nivel
        if level == DebugLevel.NONE:
            cls.show_dspy_decisions = False
            cls.show_tool_calls = False
            cls.show_history = False
            cls.show_instructions = False
            cls.show_api_calls = False
            cls.show_retries = False
        
        elif level == DebugLevel.BASIC:
            cls.show_dspy_decisions = True
            cls.show_tool_calls = True
            cls.show_history = False
            cls.show_instructions = False
            cls.show_api_calls = False
            cls.show_retries = True
        
        elif level == DebugLevel.DETAILED:
            cls.show_dspy_decisions = True
            cls.show_tool_calls = True
            cls.show_history = True
            cls.show_instructions = False
            cls.show_api_calls = False
            cls.show_retries = True
        
        elif level == DebugLevel.VERBOSE:
            cls.show_dspy_decisions = True
            cls.show_tool_calls = True
            cls.show_history = True
            cls.show_instructions = True
            cls.show_api_calls = True
            cls.show_retries = True
    
    @classmethod
    def enable_all(cls):
        """Activa todos los flags de debug"""
        cls.set_level(DebugLevel.VERBOSE)
    
    @classmethod
    def disable_all(cls):
        """Desactiva todos los flags de debug"""
        cls.set_level(DebugLevel.NONE)
    
    @classmethod
    def from_env(cls):
        """Configura desde variable de entorno DEBUG_LEVEL"""
        level_str = os.getenv('DEBUG_LEVEL', 'NONE').upper()
        level_map = {
            'NONE': DebugLevel.NONE,
            '0': DebugLevel.NONE,
            'BASIC': DebugLevel.BASIC,
            '1': DebugLevel.BASIC,
            'DETAILED': DebugLevel.DETAILED,
            '2': DebugLevel.DETAILED,
            'VERBOSE': DebugLevel.VERBOSE,
            '3': DebugLevel.VERBOSE,
        }
        cls.set_level(level_map.get(level_str, DebugLevel.NONE))
    
    @classmethod
    def print_status(cls):
        """Imprime el estado actual de debug"""
        print("=" * 70)
        print("  DEBUG CONFIGURATION")
        print("=" * 70)
        print(f"Level: {cls.level.name}")
        print(f"\nFlags:")
        print(f"  DSPy Decisions:  {'✓' if cls.show_dspy_decisions else '✗'}")
        print(f"  Tool Calls:      {'✓' if cls.show_tool_calls else '✗'}")
        print(f"  History:         {'✓' if cls.show_history else '✗'}")
        print(f"  Instructions:    {'✓' if cls.show_instructions else '✗'}")
        print(f"  API Calls:       {'✓' if cls.show_api_calls else '✗'}")
        print(f"  Retries:         {'✓' if cls.show_retries else '✗'}")
        print("=" * 70)


def debug_print(message: str, flag: str = None):
    """
    Imprime un mensaje de debug si el flag está activo
    
    Args:
        message: Mensaje a imprimir
        flag: Flag a verificar (None = siempre imprime si hay debug)
    """
    if DebugConfig.level == DebugLevel.NONE:
        return
    
    if flag is None:
        print(f"[DEBUG] {message}")
        return
    
    flag_value = getattr(DebugConfig, flag, False)
    if flag_value:
        print(f"[DEBUG] {message}")


# Configurar desde variable de entorno al importar
DebugConfig.from_env()


if __name__ == "__main__":
    print("Testing Debug Configuration\n")
    
    # Test diferentes niveles
    for level in DebugLevel:
        print(f"\n--- Testing {level.name} ---")
        DebugConfig.set_level(level)
        DebugConfig.print_status()
