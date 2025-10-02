#!/usr/bin/env python3
"""
Script para arreglar agentes guardados con configuración antigua de web_search
"""

import json
from pathlib import Path

def fix_web_search_tool(tool):
    """Actualiza la configuración de web_search al formato correcto"""
    if tool.get('type') == 'web_search':
        # Configuración correcta
        tool['web_search'] = {
            'enable': 'True',
            'search_engine': 'search-prime',
            'search_result': 'True',
            'count': '5',
            'search_recency_filter': 'noLimit',
            'content_size': 'high'
        }
    return tool

def fix_agent_file(filepath):
    """Arregla un archivo de agente"""
    print(f"Arreglando: {filepath.name}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Actualizar herramientas
    if 'tools' in config:
        config['tools'] = [fix_web_search_tool(tool) for tool in config['tools']]
        
        # Mejorar instrucciones si tiene web_search
        has_web_search = any(t.get('type') == 'web_search' for t in config['tools'])
        if has_web_search and 'web_search' not in config['instructions'].lower():
            config['instructions'] += "\n\nIMPORTANTE: Tienes acceso a web_search. Úsala cuando necesites información actualizada, precios, noticias o datos que cambian frecuentemente."
    
    # Guardar
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ Arreglado: {len(config.get('tools', []))} herramientas")

def main():
    print("=" * 70)
    print("  ARREGLANDO AGENTES GUARDADOS")
    print("=" * 70)
    
    agents_dir = Path("agents")
    if not agents_dir.exists():
        print("\n⚠️  No se encontró la carpeta 'agents'")
        return
    
    agent_files = list(agents_dir.glob("*.json"))
    
    if not agent_files:
        print("\n⚠️  No se encontraron agentes guardados")
        return
    
    print(f"\nEncontrados {len(agent_files)} agentes\n")
    
    for filepath in agent_files:
        try:
            fix_agent_file(filepath)
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("  ✅ Agentes arreglados!")
    print("=" * 70)
    print("\nAhora los agentes deberían usar web_search correctamente.")

if __name__ == "__main__":
    main()
