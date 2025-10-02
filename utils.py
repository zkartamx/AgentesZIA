"""
Utilidades para el sistema de agentes
"""

import sys
import threading
import time


class LoadingIndicator:
    """
    Indicador de carga animado para mostrar mientras el agente procesa
    
    Uso:
        loader = LoadingIndicator("Procesando")
        loader.start()
        # ... hacer algo ...
        loader.stop()
    """
    
    def __init__(self, message="Pensando"):
        self.message = message
        self.is_running = False
        self.thread = None
        # Frames de animación (spinner)
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current_frame = 0
    
    def _animate(self):
        """Función interna para animar el spinner"""
        while self.is_running:
            frame = self.frames[self.current_frame % len(self.frames)]
            sys.stdout.write(f"\r{frame} {self.message}...")
            sys.stdout.flush()
            self.current_frame += 1
            time.sleep(0.1)
    
    def start(self):
        """Inicia la animación del indicador"""
        self.is_running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Detiene la animación y limpia la línea"""
        self.is_running = False
        if self.thread:
            self.thread.join()
        # Limpiar la línea
        sys.stdout.write("\r" + " " * (len(self.message) + 20) + "\r")
        sys.stdout.flush()


class DotLoader:
    """
    Indicador de carga con puntos animados (alternativa más simple)
    
    Uso:
        loader = DotLoader("Cargando")
        loader.start()
        # ... hacer algo ...
        loader.stop()
    """
    
    def __init__(self, message="Cargando"):
        self.message = message
        self.is_running = False
        self.thread = None
        self.dot_count = 0
    
    def _animate(self):
        """Función interna para animar los puntos"""
        while self.is_running:
            dots = "." * (self.dot_count % 4)
            spaces = " " * (3 - len(dots))
            sys.stdout.write(f"\r{self.message}{dots}{spaces}")
            sys.stdout.flush()
            self.dot_count += 1
            time.sleep(0.5)
    
    def start(self):
        """Inicia la animación del indicador"""
        self.is_running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Detiene la animación y limpia la línea"""
        self.is_running = False
        if self.thread:
            self.thread.join()
        # Limpiar la línea
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()


def format_message(role: str, content: str, max_length: int = None) -> str:
    """
    Formatea un mensaje para mostrar en consola
    
    Args:
        role: Rol del mensaje (user, assistant, system)
        content: Contenido del mensaje
        max_length: Longitud máxima (None para sin límite)
    
    Returns:
        Mensaje formateado
    """
    role_emoji = {
        "user": "👤",
        "assistant": "🤖",
        "system": "⚙️"
    }
    
    emoji = role_emoji.get(role.lower(), "💬")
    role_name = role.capitalize()
    
    if max_length and len(content) > max_length:
        content = content[:max_length] + "..."
    
    return f"{emoji} {role_name}: {content}"


if __name__ == "__main__":
    # Ejemplo de uso
    print("=== Ejemplos de Indicadores de Carga ===\n")
    
    # Ejemplo 1: Spinner
    print("1. Spinner animado:")
    loader = LoadingIndicator("Procesando")
    loader.start()
    time.sleep(3)
    loader.stop()
    print("✓ Completado!\n")
    
    # Ejemplo 2: Dots
    print("2. Puntos animados:")
    loader = DotLoader("Cargando")
    loader.start()
    time.sleep(3)
    loader.stop()
    print("✓ Completado!\n")
    
    # Ejemplo 3: Formato de mensajes
    print("3. Formato de mensajes:")
    print(format_message("user", "Hola, ¿cómo estás?"))
    print(format_message("assistant", "¡Hola! Estoy bien, gracias por preguntar."))
    print(format_message("system", "Sistema inicializado correctamente"))
