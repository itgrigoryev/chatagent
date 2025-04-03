import sys
import os
import json
from datetime import datetime

# Адаптируем путь к системным протоколам
sys.path.append('C:\\Users\\Sergio\\Desktop\\CRM-LLM-Integration-Platform')

# Импортируем менеджер контекста
try:
    from system_protocols.context_manager import ContextManager
    
    # Инициализация менеджера с правильным путем
    context_manager = ContextManager(
        base_path='C:\\Users\\Sergio\\Desktop\\CRM-LLM-Integration-Platform'
    )
    
    # Тест сохранения контекста
    test_data = {
        'test_id': 'test_001',
        'timestamp': datetime.now().isoformat(),
        'description': 'Тестирование системы сохранения контекста',
        'parameters': {
            'parameter1': 'value1',
            'parameter2': 42,
            'parameter3': [1, 2, 3, 4, 5]
        }
    }
    
    # Сохраняем микро-контекст
    micro_path = context_manager.save_context('микро', test_data)
    
    # Выводим результат
    print(f"Контекст успешно сохранен в: {micro_path}")
    
    # Загружаем сохраненный контекст
    loaded_context = context_manager.load_context(micro_path)
    
    # Проверяем целостность
    if loaded_context and loaded_context['data']['test_id'] == test_data['test_id']:
        print("Тест ПРОЙДЕН: Сохранение и загрузка контекста работают корректно!")
    else:
        print("Тест НЕ ПРОЙДЕН: Ошибка при сохранении или загрузке контекста!")
    
    # Выводим список всех контекстов
    print("\nСписок доступных контекстов:")
    contexts = context_manager.list_contexts()
    for ctx in contexts:
        print(f" - {ctx}")
    
    print(f"\nВсего найдено контекстов: {len(contexts)}")
    
except ImportError as e:
    print(f"Ошибка импорта модуля: {str(e)}")
except Exception as e:
    print(f"Непредвиденная ошибка: {str(e)}")
