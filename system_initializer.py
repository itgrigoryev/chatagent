import os
import sys
import json
from datetime import datetime
import logging

class SystemInitializer:
    def __init__(self, base_path=None):
        # Определение базового пути проекта
        self.base_path = base_path or os.path.dirname(os.path.abspath(__file__))
        
        # Настройка логирования
        self.setup_logging()
        
        # Приветствие
        self.logger.info(f"Инициализация Универсального Протокола Разработки v8.0")
        self.logger.info(f"Базовая директория проекта: {self.base_path}")
        
        # Создание необходимых директорий
        self.create_required_directories()
        
        # Загрузка системных модулей
        self.load_system_modules()
        
        # Создание точки восстановления
        self.create_recovery_point()
        
        # Сохранение системного контекста
        self.save_system_context()
        
        self.logger.info("Инициализация системы завершена успешно!")

    def setup_logging(self):
        """Настройка логирования"""
        logs_dir = os.path.join(self.base_path, 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        log_file = os.path.join(logs_dir, f"system_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger('SystemInitializer')

    def create_required_directories(self):
        """Создание необходимых директорий"""
        required_dirs = [
            'artifacts',
            'configs',
            'context_storage',
            'recovery_points',
            'logs',
            'integrations'
        ]
        
        self.logger.info("Создание необходимых директорий:")
        for directory in required_dirs:
            dir_path = os.path.join(self.base_path, directory)
            os.makedirs(dir_path, exist_ok=True)
            self.logger.info(f" - {dir_path}")

    def load_system_modules(self):
        """Загрузка системных модулей"""
        self.logger.info("Загрузка системных модулей:")
        
        # Добавление системных протоколов в путь
        sys.path.append(self.base_path)
        
        try:
            # Импорт и инициализация модулей с правильным путем
            self.logger.info(" - Загрузка ContextManager")
            from system_protocols.context_manager import ContextManager
            self.context_manager = ContextManager(base_path=self.base_path)
            
            self.logger.info(" - Загрузка SpecializationManager")
            from system_protocols.specialization_manager import SpecializationManager
            self.specialization_manager = SpecializationManager
            
            # Исправление метода создания конфигурации
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
                filepath = os.path.join(self.base_path, 'configs', filename)
                
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                
                return filepath
            
            # Применяем фикс
            SpecializationManager.create_specialization_config = fixed_create_config
            
            self.logger.info("Все системные модули успешно загружены")
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке модулей: {str(e)}")
            raise

    def create_recovery_point(self):
        """Создание точки восстановления"""
        self.logger.info("Создание точки восстановления")
        
        try:
            # Простая реализация для проверки
            recovery_dir = os.path.join(self.base_path, 'recovery_points')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            recovery_point = os.path.join(recovery_dir, f'recovery_{timestamp}')
            
            os.makedirs(recovery_point, exist_ok=True)
            
            # Создание метаданных точки восстановления
            metadata = {
                'id': f"recovery_{timestamp}",
                'timestamp': datetime.now().isoformat(),
                'description': 'Инициализация системы',
                'created_by': 'SystemInitializer'
            }
            
            metadata_path = os.path.join(recovery_point, 'metadata.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Точка восстановления создана: {recovery_point}")
            self.recovery_point = recovery_point
        except Exception as e:
            self.logger.error(f"Ошибка при создании точки восстановления: {str(e)}")

    def save_system_context(self):
        """Сохранение системного контекста"""
        self.logger.info("Сохранение системного контекста")
        
        try:
            system_context = {
                'timestamp': datetime.now().isoformat(),
                'base_path': self.base_path,
                'recovery_point': getattr(self, 'recovery_point', None),
                'system_state': 'initialized',
                'initialized_modules': [
                    'ContextManager',
                    'SpecializationManager'
                ]
            }
            
            # Сохранение через менеджер контекста
            context_path = self.context_manager.save_context(
                'мета',
                system_context,
                project_id='system'
            )
            
            self.logger.info(f"Системный контекст сохранен: {context_path}")
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении системного контекста: {str(e)}")

# Запуск инициализатора
if __name__ == "__main__":
    initializer = SystemInitializer()
    
    print("="*80)
    print("СИСТЕМА УСПЕШНО ИНИЦИАЛИЗИРОВАНА")
    print(f"Базовая директория: {initializer.base_path}")
    print(f"Точка восстановления: {getattr(initializer, 'recovery_point', 'Не создана')}")
    print("="*80)
