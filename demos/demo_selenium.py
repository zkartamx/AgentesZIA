#!/usr/bin/env python3
"""
Demo: Agente con Selenium para automatización web
Muestra cómo crear un agente que puede navegar y extraer información de páginas web
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_creator import Agent
from tools import create_selenium_tool
from utils import LoadingIndicator


def demo_basic_navigation():
    """Demo básico de navegación con Selenium"""
    print("=" * 70)
    print("  DEMO: Navegación Básica con Selenium")
    print("=" * 70)
    
    # Crear agente con Selenium
    agent = Agent(
        name="Web Navigator",
        instructions="""
        Eres un asistente que puede navegar páginas web usando Selenium.
        Cuando el usuario te pida visitar una página, usa selenium_navigate.
        """,
        tools=[create_selenium_tool()]
    )
    
    print(f"\n✓ Agente creado: {agent}")
    print(f"✓ Herramientas: {len(agent.get_tools())}\n")
    
    # Ejemplo: Navegar a una página
    request = "Navega a https://www.example.com y dime qué ves"
    print(f"Usuario: {request}\n")
    
    loader = LoadingIndicator("Navegando")
    loader.start()
    
    try:
        response = agent.chat(request)
    finally:
        loader.stop()
    
    print(f"Agente: {response}\n")
    
    print("=" * 70)


def demo_web_scraping():
    """Demo de web scraping con Selenium"""
    print("=" * 70)
    print("  DEMO: Web Scraping con Selenium")
    print("=" * 70)
    
    agent = Agent(
        name="Web Scraper",
        instructions="""
        Eres un experto en web scraping usando Selenium.
        Puedes navegar páginas web y extraer información.
        Usa selenium_navigate para visitar páginas.
        """,
        tools=[create_selenium_tool()]
    )
    
    print(f"\n✓ Agente creado: {agent}")
    print(f"✓ Herramientas: {len(agent.get_tools())}\n")
    
    # Ejemplo: Extraer información
    request = "Visita https://www.python.org y dime cuál es el título de la página"
    print(f"Usuario: {request}\n")
    
    loader = LoadingIndicator("Extrayendo información")
    loader.start()
    
    try:
        response = agent.chat(request)
    finally:
        loader.stop()
    
    print(f"Agente: {response}\n")
    
    print("=" * 70)


def demo_manual_selenium():
    """Demo de uso manual de Selenium (sin agente)"""
    print("=" * 70)
    print("  DEMO: Uso Manual de Selenium")
    print("=" * 70)
    
    from selenium_handler import selenium_navigate, selenium_get_text, selenium_close
    
    print("\n1. Navegando a Example.com...")
    result = selenium_navigate("https://www.example.com")
    if result['success']:
        print(f"   ✓ Título: {result['title']}")
        print(f"   ✓ URL: {result['url']}")
    else:
        print(f"   ❌ Error: {result['error']}")
    
    print("\n2. Obteniendo texto de la página...")
    result = selenium_get_text()
    if result['success']:
        print(f"   ✓ Texto obtenido: {result['length']} caracteres")
        print(f"   ✓ Primeros 200 caracteres:")
        print(f"   {result['text'][:200]}...")
    else:
        print(f"   ❌ Error: {result['error']}")
    
    print("\n3. Cerrando navegador...")
    result = selenium_close()
    print(f"   ✓ {result['message']}")
    
    print("\n" + "=" * 70)


def main():
    print("\n" + "=" * 70)
    print("  SISTEMA DE AUTOMATIZACIÓN WEB CON SELENIUM")
    print("=" * 70)
    
    # Demo 1: Uso manual
    demo_manual_selenium()
    
    print("\n")
    
    # Demo 2: Navegación básica con agente
    # demo_basic_navigation()  # Descomenta para probar
    
    # Demo 3: Web scraping con agente
    # demo_web_scraping()  # Descomenta para probar
    
    print("\n" + "=" * 70)
    print("  Demos completados!")
    print("=" * 70)
    print("\n💡 Nota: Selenium requiere Chrome instalado en el sistema")
    print("   El navegador se ejecuta en modo headless (sin interfaz gráfica)")


if __name__ == "__main__":
    main()
