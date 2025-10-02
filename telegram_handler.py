"""
Manejador de funciones de Telegram
Implementa la lógica para enviar mensajes a través de un bot de Telegram
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


def send_telegram_message(message: str, parse_mode: str = None) -> dict:
    """
    Envía un mensaje a través de un bot de Telegram
    
    Args:
        message: El mensaje a enviar
        parse_mode: Formato del mensaje ('Markdown' o 'HTML')
    
    Returns:
        Diccionario con el resultado de la operación
    
    Requiere variables de entorno:
        TELEGRAM_BOT_TOKEN: Token del bot de Telegram
        TELEGRAM_CHAT_ID: ID del chat donde enviar el mensaje
    """
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        return {
            'success': False,
            'error': 'TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID deben estar configurados en .env'
        }
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    
    if parse_mode:
        payload['parse_mode'] = parse_mode
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        return {
            'success': True,
            'message': 'Mensaje enviado exitosamente',
            'response': response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'Error al enviar mensaje: {str(e)}'
        }


def handle_function_call(function_name: str, arguments: dict) -> dict:
    """
    Maneja las llamadas a funciones desde el agente
    
    Args:
        function_name: Nombre de la función a ejecutar
        arguments: Argumentos de la función
    
    Returns:
        Resultado de la función
    """
    if function_name == 'send_telegram_message':
        return send_telegram_message(
            message=arguments.get('message'),
            parse_mode=arguments.get('parse_mode')
        )
    else:
        return {
            'success': False,
            'error': f'Función desconocida: {function_name}'
        }


if __name__ == "__main__":
    # Test de la función
    print("=== Test: Enviar mensaje a Telegram ===\n")
    
    # Verificar configuración
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("❌ Error: Configura TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID en .env")
        print("\nPara obtener tu bot token:")
        print("1. Habla con @BotFather en Telegram")
        print("2. Crea un nuevo bot con /newbot")
        print("3. Copia el token que te da")
        print("\nPara obtener tu chat ID:")
        print("1. Habla con @userinfobot en Telegram")
        print("2. Te dará tu chat ID")
    else:
        print(f"✓ Bot Token configurado: {bot_token[:10]}...")
        print(f"✓ Chat ID configurado: {chat_id}\n")
        
        # Enviar mensaje de prueba
        result = send_telegram_message("🤖 Mensaje de prueba desde el sistema de agentes Z.AI")
        
        if result['success']:
            print("✅ Mensaje enviado exitosamente!")
            print(f"Response: {result['response']}")
        else:
            print(f"❌ Error: {result['error']}")
