import os
import sys
import time
from datetime import datetime

# Добавляем путь к проекту
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

# Выводим информацию о тесте
print("="*80)
print("ТЕСТ ПРОДОЛЖЕНИЯ ФАЙЛОВ ПОСЛЕ ОБРЫВА СЕССИИ")
print(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Импортируем менеджеры
from system_protocols.file_continuity_manager import FileContinuityManager
from system_protocols.artifact_manager import ArtifactManager

# Создаем тестовые директории
test_dir = os.path.join(project_path, 'test_files')
os.makedirs(test_dir, exist_ok=True)

print("\n1. Тест базовой функциональности FileContinuityManager")
print("-"*50)

# Создаем тестовый файл
test_file = os.path.join(test_dir, "test_continue.txt")
complete_content = """Это первая строка тестового файла.
Это вторая строка тестового файла.
Это третья строка тестового файла.
Это четвертая строка тестового файла.
Это пятая строка тестового файла."""

# Первый запуск - создание файла
result1 = FileContinuityManager.continue_file_writing(test_file, complete_content)
print(f"Первый запуск: {result1['status']} - {result1['message']}")

# Симуляция обрыва - создаем неполный файл
with open(test_file, 'w', encoding='utf-8') as f:
    f.write("""Это первая строка тестового файла.
Это вторая строка тестового файла.
""")

print(f"Симуляция обрыва: файл обрезан до первых двух строк")

# Второй запуск - продолжение файла
result2 = FileContinuityManager.continue_file_writing(test_file, complete_content)
print(f"Второй запуск: {result2['status']} - {result2['message']}")

# Проверка содержимого файла
with open(test_file, 'r', encoding='utf-8') as f:
    final_content = f.read()

print(f"Итоговый файл содержит {len(final_content)} символов")
print(f"Файл соответствует ожидаемому: {final_content == complete_content}")


print("\n2. Тест ArtifactManager с поддержкой непрерывности")
print("-"*50)

# Инициализируем ArtifactManager
artifact_manager = A