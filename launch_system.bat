@echo off
echo ===================================
echo Запуск CRM-LLM Integration Platform
echo ===================================

cd %~dp0
python system_initializer.py

echo.
echo Система запущена успешно!
echo.

pause
