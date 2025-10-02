"""
Sistema de Gestión de Tareas para Agentes
Permite programar tareas y que el agente las marque como completadas
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class Task:
    """Representa una tarea individual"""
    
    def __init__(self, id: int, description: str, completed: bool = False, 
                 created_at: str = None, completed_at: str = None, assigned_to: str = None):
        self.id = id
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
        self.completed_at = completed_at
        self.assigned_to = assigned_to  # Nombre del agente asignado
    
    def complete(self):
        """Marca la tarea como completada"""
        self.completed = True
        self.completed_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convierte la tarea a diccionario"""
        return {
            'id': self.id,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at,
            'completed_at': self.completed_at,
            'assigned_to': self.assigned_to
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea una tarea desde un diccionario"""
        return cls(
            id=data['id'],
            description=data['description'],
            completed=data.get('completed', False),
            created_at=data.get('created_at'),
            completed_at=data.get('completed_at'),
            assigned_to=data.get('assigned_to')
        )
    
    def __str__(self):
        status = "✅" if self.completed else "⬜"
        agent_info = f" → {self.assigned_to}" if self.assigned_to else ""
        return f"{status} [{self.id}] {self.description}{agent_info}"


class TaskManager:
    """Gestor de tareas para agentes"""
    
    def __init__(self, tasks_file: str = "tasks.json"):
        self.tasks_file = Path(tasks_file)
        self.tasks: List[Task] = []
        self.next_id = 1
        self.load_tasks()
    
    def load_tasks(self):
        """Carga tareas desde archivo"""
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(t) for t in data.get('tasks', [])]
                    self.next_id = data.get('next_id', 1)
            except Exception as e:
                print(f"⚠️  Error cargando tareas: {e}")
                self.tasks = []
                self.next_id = 1
    
    def save_tasks(self):
        """Guarda tareas en archivo"""
        try:
            data = {
                'tasks': [t.to_dict() for t in self.tasks],
                'next_id': self.next_id
            }
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Error guardando tareas: {e}")
    
    def add_task(self, description: str) -> Task:
        """Agrega una nueva tarea"""
        task = Task(id=self.next_id, description=description)
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        return task
    
    def complete_task(self, task_id: int) -> bool:
        """Marca una tarea como completada"""
        for task in self.tasks:
            if task.id == task_id and not task.completed:
                task.complete()
                self.save_tasks()
                return True
        return False
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Obtiene una tarea por ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_pending_tasks(self) -> List[Task]:
        """Obtiene todas las tareas pendientes"""
        return [t for t in self.tasks if not t.completed]
    
    def get_completed_tasks(self) -> List[Task]:
        """Obtiene todas las tareas completadas"""
        return [t for t in self.tasks if t.completed]
    
    def delete_task(self, task_id: int) -> bool:
        """Elimina una tarea"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                self.save_tasks()
                return True
        return False
    
    def clear_completed(self):
        """Elimina todas las tareas completadas"""
        self.tasks = [t for t in self.tasks if not t.completed]
        self.save_tasks()
    
    def assign_task(self, task_id: int, agent_name: str) -> bool:
        """Asigna una tarea a un agente"""
        for task in self.tasks:
            if task.id == task_id:
                task.assigned_to = agent_name
                self.save_tasks()
                return True
        return False
    
    def get_tasks_by_agent(self, agent_name: str) -> List[Task]:
        """Obtiene todas las tareas asignadas a un agente"""
        return [t for t in self.tasks if t.assigned_to == agent_name]
    
    def get_agents_with_tasks(self) -> List[str]:
        """Obtiene lista de agentes que tienen tareas asignadas"""
        agents = set()
        for task in self.tasks:
            if task.assigned_to:
                agents.add(task.assigned_to)
        return sorted(list(agents))
    
    def get_summary(self) -> dict:
        """Obtiene un resumen de las tareas"""
        total = len(self.tasks)
        completed = len(self.get_completed_tasks())
        pending = len(self.get_pending_tasks())
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'progress': (completed / total * 100) if total > 0 else 0
        }
    
    def print_tasks(self, show_completed: bool = True):
        """Imprime todas las tareas"""
        pending = self.get_pending_tasks()
        completed = self.get_completed_tasks()
        
        print("\n" + "=" * 70)
        print("  LISTA DE TAREAS")
        print("=" * 70)
        
        if pending:
            print("\n📋 Tareas Pendientes:")
            for task in pending:
                print(f"  {task}")
        else:
            print("\n✨ No hay tareas pendientes")
        
        if show_completed and completed:
            print("\n✅ Tareas Completadas:")
            for task in completed:
                print(f"  {task}")
        
        # Resumen
        summary = self.get_summary()
        print("\n" + "-" * 70)
        print(f"Total: {summary['total']} | "
              f"Completadas: {summary['completed']} | "
              f"Pendientes: {summary['pending']} | "
              f"Progreso: {summary['progress']:.1f}%")
        print("=" * 70)


# Funciones para usar como herramientas del agente

def task_add(description: str) -> dict:
    """Agrega una nueva tarea"""
    manager = TaskManager()
    task = manager.add_task(description)
    return {
        'success': True,
        'task_id': task.id,
        'message': f'Tarea #{task.id} agregada: {description}'
    }


def task_complete(task_id: int) -> dict:
    """Marca una tarea como completada"""
    manager = TaskManager()
    if manager.complete_task(task_id):
        task = manager.get_task(task_id)
        return {
            'success': True,
            'message': f'✅ Tarea #{task_id} completada: {task.description}'
        }
    return {
        'success': False,
        'error': f'Tarea #{task_id} no encontrada o ya completada'
    }


def task_list() -> dict:
    """Lista todas las tareas"""
    manager = TaskManager()
    pending = manager.get_pending_tasks()
    completed = manager.get_completed_tasks()
    summary = manager.get_summary()
    
    return {
        'success': True,
        'pending': [{'id': t.id, 'description': t.description} for t in pending],
        'completed': [{'id': t.id, 'description': t.description} for t in completed],
        'summary': summary
    }


def task_delete(task_id: int) -> dict:
    """Elimina una tarea"""
    manager = TaskManager()
    if manager.delete_task(task_id):
        return {
            'success': True,
            'message': f'Tarea #{task_id} eliminada'
        }
    return {
        'success': False,
        'error': f'Tarea #{task_id} no encontrada'
    }


if __name__ == "__main__":
    # Demo
    print("=" * 70)
    print("  DEMO: Sistema de Tareas")
    print("=" * 70)
    
    manager = TaskManager()
    
    # Agregar tareas
    print("\n1. Agregando tareas...")
    manager.add_task("Investigar precio de Bitcoin")
    manager.add_task("Enviar reporte por Telegram")
    manager.add_task("Tomar captura de pantalla")
    
    # Mostrar tareas
    manager.print_tasks()
    
    # Completar una tarea
    print("\n2. Completando tarea #1...")
    manager.complete_task(1)
    
    # Mostrar tareas actualizadas
    manager.print_tasks()
    
    # Resumen
    summary = manager.get_summary()
    print(f"\n3. Progreso: {summary['progress']:.1f}%")
