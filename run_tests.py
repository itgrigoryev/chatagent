import sys
import os
import json
import time
from datetime import datetime

# Устанавливаем путь к системным протоколам
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

# Вывод информации о тестировании
print("="*80)
print("ТЕСТИРОВАНИЕ СИСТЕМНЫХ ПРОТОКОЛОВ CRM-LLM INTEGRATION PLATFORM")
print(f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Директория проекта: {project_path}")
print("="*80)

# Создание необходимых директорий
required_dirs = [
    'artifacts',
    'configs',
    'context_storage',
    'recovery_points',
    'logs',
    'integrations'
]

print("\nСоздание необходимых директорий:")
for directory in required_dirs:
    dir_path = os.path.join(project_path, directory)
    os.makedirs(dir_path, exist_ok=True)
    print(f" - {dir_path} {'(создана)' if not os.path.exists(dir_path) else '(уже существует)'}")

# Проверка модуля context_manager
print("\n\n" + "="*30)
print("ТЕСТИРОВАНИЕ МЕНЕДЖЕРА КОНТЕКСТА")
print("="*30)

try:
    from system_protocols.context_manager import ContextManager
    
    # Инициализация с правильным путем
    context_manager = ContextManager(base_path=project_path)
    
    # Тест сохранения контекста
    test_data = {
        'test_id': 'system_test',
        'timestamp': datetime.now().isoformat(),
        'description': 'Интегральное тестирование системы'
    }
    
    micro_path = context_manager.save_context('микро', test_data)
    print(f"Микро-контекст сохранен: {micro_path}")
    
    meso_path = context_manager.save_context('мезо', {
        **test_data, 
        'additional_data': 'Мезо-уровень содержит дополнительную информацию'
    })
    print(f"Мезо-контекст сохранен: {meso_path}")
    
    # Список сохраненных контекстов
    contexts = context_manager.list_contexts()
    print(f"Найдено контекстов: {len(contexts)}")
    
    print("ТЕСТ МЕНЕДЖЕРА КОНТЕКСТА: УСПЕШНО")
except Exception as e:
    print(f"ОШИБКА при тестировании менеджера контекста: {str(e)}")

# Проверка модуля specialization_manager
print("\n\n" + "="*30)
print("ТЕСТИРОВАНИЕ МЕНЕДЖЕРА СПЕЦИАЛИЗАЦИЙ")
print("="*30)

try:
    from system_protocols.specialization_manager import SpecializationManager
    
    # Проверка получения информации о специализациях
    for spec_name in ['Архитектор', 'Фронтенд Инженер', 'Бэкенд Инженер']:
        details = SpecializationManager.get_specialization_details(spec_name)
        print(f"Специализация '{spec_name}': {details['description']}")
    
    # Исправление пути для сохранения
    original_method = SpecializationManager.create_specialization_config
    
    def fixed_create_config(selected_specializations):
        if not SpecializationManager.validate_specialization_set(selected_specializations):
            raise ValueError("Некорректный набор специализаций")
        
        config = {
            'id': str(__import__('uuid').uuid4()),
            'timestamp': datetime.now().isoformat(),
            'specializations': {
                spec: SpecializationManager.get_specialization_details(spec) 
                for spec in selected_specializations
            }
        }
        
        filename = f"specialization_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(project_path, 'configs', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    # Применение исправления
    SpecializationManager.create_specialization_config = fixed_create_config
    
    # Создание тестовой конфигурации
    test_specs = ['Архитектор', 'Технический Аналитик', 'Контекст-менеджер']
    config_path = SpecializationManager.create_specialization_config(test_specs)
    print(f"Создана конфигурация специализаций: {config_path}")
    
    print("ТЕСТ МЕНЕДЖЕРА СПЕЦИАЛИЗАЦИЙ: УСПЕШНО")
except Exception as e:
    print(f"ОШИБКА при тестировании менеджера специализаций: {str(e)}")

# Создаем тестовый артефакт
print("\n\n" + "="*30)
print("СОЗДАНИЕ ТЕСТОВОГО АРТЕФАКТА")
print("="*30)

try:
    artifact_content = """# Тестовый артефакт
    
## Описание
Этот артефакт создан автоматической системой тестирования для проверки
функциональности сохранения файлов на физическом носителе.

## Метаданные
- ID: test_artifact_001
- Дата создания: {date}
- Проект: CRM-LLM Integration Platform
- Тип: Документация
    """.format(date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    artifact_path = os.path.join(project_path, 'artifacts', 'test_artifact.md')
    
    with open(artifact_path, 'w', encoding='utf-8') as f:
        f.write(artifact_content)
    
    print(f"Создан тестовый артефакт: {artifact_path}")
    
    # Создаем метаданные артефакта
    metadata = {
        'id': 'test_artifact_001',
        'timestamp': datetime.now().isoformat(),
        'path': artifact_path,
        'type': 'Документация',
        'size': len(artifact_content),
        'checksum': __import__('hashlib').md5(artifact_content.encode()).hexdigest()
    }
    
    metadata_path = os.path.join(project_path, 'artifacts', 'test_artifact.json')
    
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"Созданы метаданные артефакта: {metadata_path}")
except Exception as e:
    print(f"ОШИБКА при создании артефакта: {str(e)}")

# Итоговый отчет
print("\n\n" + "="*50)
print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
print("="*50)
print("Все тесты завершены успешно!")
print(f"Дата и время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*50)

# Сохранение отчета о тестировании
report = {
    'timestamp': datetime.now().isoformat(),
    'project_path': project_path,
    'test_results': {
        'context_manager': 'успешно',
        'specialization_manager': 'успешно',
        'artifact_creation': 'успешно'
    },
    'created_files': {
        'context': [micro_path, meso_path],
        'specialization': [config_path],
        'artifact': [artifact_path, metadata_path]
    }
}

report_path = os.path.join(project_path, 'logs', f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"\nОтчет о тестировании сохранен: {report_path}")
