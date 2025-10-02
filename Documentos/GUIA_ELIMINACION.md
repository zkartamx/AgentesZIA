# Guía: Eliminar Agentes Guardados

## 🗑️ Opciones para Eliminar Agentes

### Opción 1: Desde el Sistema Interactivo (Recomendado)

```bash
python agent_manager.py
```

En el menú principal, selecciona la opción **5. Eliminar agentes guardados**

#### Funcionalidades disponibles:

1. **Eliminar un agente específico**
   - Ingresa el número del agente que deseas eliminar
   - Confirma la eliminación
   
2. **Eliminar todos los agentes**
   - Escribe `todos`
   - Confirma la eliminación masiva
   
3. **Cancelar operación**
   - Escribe `cancelar` para volver al menú

---

## 📋 Ejemplo de Uso Interactivo

### Escenario 1: Eliminar un agente específico

```
=== Agentes Guardados ===
1. Math Tutor (math_tutor.json)
2. Code Reviewer (code_reviewer.json)
3. Creative Writer (creative_writer.json)

Opciones:
- Ingresa un número para eliminar ese agente
- Ingresa 'todos' para eliminar todos los agentes
- Ingresa 'cancelar' para volver

Selecciona una opción: 2

⚠️  ¿Eliminar 'Code Reviewer'? (s/n): s

✓ Agente 'Code Reviewer' eliminado
```

### Escenario 2: Eliminar todos los agentes

```
=== Agentes Guardados ===
1. Math Tutor (math_tutor.json)
2. Code Reviewer (code_reviewer.json)
3. Creative Writer (creative_writer.json)

Opciones:
- Ingresa un número para eliminar ese agente
- Ingresa 'todos' para eliminar todos los agentes
- Ingresa 'cancelar' para volver

Selecciona una opción: todos

⚠️  ¿Estás seguro de eliminar TODOS los agentes? (s/n): s

✓ 3 agente(s) eliminado(s)
```

### Escenario 3: Cancelar operación

```
Selecciona una opción: cancelar

Operación cancelada
```

---

## 💻 Opción 2: Desde Código Python

### Eliminar un agente específico

```python
from agent_creator import Agent

# Eliminar un archivo de agente
Agent.delete_agent("math_tutor.json")
# Output: Agente eliminado: math_tutor.json
```

### Eliminar múltiples agentes

```python
from agent_creator import Agent
from pathlib import Path

# Obtener todos los archivos de agentes
agents_dir = Path("agents")
agent_files = list(agents_dir.glob("*.json"))

# Eliminar todos
for agent_file in agent_files:
    Agent.delete_agent(str(agent_file))
```

### Eliminar agentes con confirmación

```python
from agent_creator import Agent
import json

def delete_agent_with_confirmation(filename):
    """Elimina un agente con confirmación del usuario"""
    try:
        # Leer información del agente
        with open(filename, 'r') as f:
            config = json.load(f)
        
        agent_name = config['name']
        confirm = input(f"¿Eliminar '{agent_name}'? (s/n): ").lower()
        
        if confirm == 's':
            Agent.delete_agent(filename)
            return True
        else:
            print("Operación cancelada")
            return False
    except FileNotFoundError:
        print(f"Archivo no encontrado: {filename}")
        return False

# Uso
delete_agent_with_confirmation("math_tutor.json")
```

---

## 🔒 Características de Seguridad

### Confirmación Obligatoria

- **Eliminación individual**: Requiere confirmación (s/n)
- **Eliminación masiva**: Requiere confirmación con advertencia ⚠️
- **Cancelación**: Siempre disponible escribiendo 'cancelar'

### Validaciones

- ✅ Verifica que el archivo existe antes de eliminar
- ✅ Muestra el nombre del agente antes de confirmar
- ✅ Cuenta cuántos agentes se eliminaron
- ✅ Maneja errores si el archivo no existe

---

## 📂 Ubicación de Archivos

Por defecto, los agentes se guardan en:
```
Antes_OpenAI/
└── agents/
    ├── math_tutor.json
    ├── code_reviewer.json
    └── creative_writer.json
```

También puedes tener agentes en el directorio raíz:
```
Antes_OpenAI/
├── math_tutor_agent.json
├── fitness_coach.json
└── ...
```

---

## ⚠️ Advertencias Importantes

1. **La eliminación es permanente**: No hay papelera de reciclaje
2. **No se puede deshacer**: Una vez eliminado, el archivo desaparece
3. **Solo elimina el archivo**: No afecta agentes en memoria
4. **Backup recomendado**: Considera hacer copias de seguridad de agentes importantes

---

## 💡 Mejores Prácticas

### 1. Revisar antes de eliminar
```bash
# Listar agentes primero (opción 4)
# Luego eliminar (opción 5)
```

### 2. Hacer backup de agentes importantes
```bash
# Copiar archivos importantes a un directorio de backup
mkdir backup_agents
cp agents/important_agent.json backup_agents/
```

### 3. Usar nombres descriptivos
```python
# Mal
agent.save_agent("agent1.json")

# Bien
agent.save_agent("math_tutor_advanced.json")
```

### 4. Organizar por categorías
```
agents/
├── tutors/
│   ├── math_tutor.json
│   └── science_tutor.json
├── writers/
│   ├── creative_writer.json
│   └── technical_writer.json
└── coders/
    ├── python_expert.json
    └── javascript_expert.json
```

---

## 🔧 Solución de Problemas

### Error: "Archivo no encontrado"
```
Solución: Verifica la ruta del archivo
- Usa rutas absolutas o relativas correctas
- Lista los agentes primero para ver los nombres exactos
```

### Error: "Permission denied"
```
Solución: Verifica permisos del archivo
- En Unix/Mac: chmod 644 archivo.json
- Verifica que no esté siendo usado por otro programa
```

### No aparecen agentes para eliminar
```
Solución: Verifica que existan archivos .json
- Usa la opción 4 para listar agentes
- Verifica el directorio 'agents/'
```

---

## 📚 Recursos Adicionales

- Ver `demo_delete.py` para ejemplos de código
- Ver `README.md` para documentación completa
- Ver `agent_manager.py` para implementación

---

## 🎯 Resumen Rápido

| Acción | Comando |
|--------|---------|
| Eliminar desde menú | `python agent_manager.py` → Opción 5 |
| Eliminar desde código | `Agent.delete_agent("archivo.json")` |
| Ver demo | `python demo_delete.py` |
| Listar antes de eliminar | Opción 4 en el menú |
| Cancelar eliminación | Escribir 'cancelar' |
