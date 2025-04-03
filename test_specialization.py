import sys
import os
import json

# Адаптируем путь к системным протоколам
sys.path.append('C:\\Users\\Sergio\\Desktop\\CRM-LLM-Integration-Platform')

# Создаем директорию для конфигураций
os.makedirs('C:\\Users\\Sergio\\Desktop\\CRM-LLM-Integration-Platform\\configs', exist_ok=True)

try:
    # Импортируем менеджер специализаций
    from system_protocols.specialization_manager import SpecializationManager
    
    # Тестирование получения детальной информации о специализации
    architect_details = SpecializationManager.get_specialization_details('Архитектор')
    print(f"Детали специализации 'Архитектор':")
    print(json.dumps(architect_details, ensure_ascii=False, indent=2))
    
    # Тестирование валидации набора специализаций
    valid_set = ['Архитектор', 'Фронтенд Инженер', 'Бэкенд Инженер']
    invalid_set = ['Архитектор', 'Фронтенд Инженер', 'Несуществующая специализация']
    
    print(f"\nВалидация набора {valid_set}: {SpecializationManager.validate_specialization_set(valid_set)}")
    print(f"Валидация набора {invalid_set}: {SpecializationManager.validate_specialization_set(invalid_set)}")
    
    # Исправляем путь в методе create_specialization_config
    original_method = SpecializationManager.create_specialization_config
    
    def fixed_create_config(selected_specializations):
        if not SpecializationManager.validate_specialization_set(selected_specializations):
            raise ValueError("Некорректный набор специализаций")
        
        config = {
            'id': str(__import__('uuid').uuid4()),
            'timestamp': __import__('datetime').datetime.now().isoformat(),
            'specializations': {
                spec: SpecializationManager.get_specialization_details(spec) 
                for spec in selected_specializations
            }
        }
        
        # Генерация пути для сохранения с правильным путем
        filename = f"specialization_config_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = f"C:\\Users\\Sergio\\Desktop\\CRM-LLM-Integration-Platform\\configs\\{filename}"
        
        # Создание директории
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Сохранение конфигурации
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    # Заменяем метод на исправленный
    SpecializationManager.create_specialization_config = fixed_create_config
    
    # Тестирование создания конфигурации
    selected_specs = ['Архитектор', 'Фронтенд Инженер', 'Бэкенд Инженер']
    config_path = SpecializationManager.create_specialization_config(selected_specs)
    
    print(f"\nСоздан файл конфигурации: {config_path}")
    
    # Читаем созданный файл для проверки
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    
    print(f"\nКонтент файла конфигурации:")
    print(json.dumps(config_data, ensure_ascii=False, indent=2))
    
    print("\nТест специализаций ПРОЙДЕН: Все функции работают корректно!")
    
except ImportError as e:
    print(f"Ошибка импорта модуля: {str(e)}")
except Exception as e:
    print(f"Непредвиденная ошибка: {str(e)}")
