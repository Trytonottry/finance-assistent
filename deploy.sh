#!/bin/bash
set -e

APP_DIR="$HOME/finance_assistant_2.1"

echo "🚀 Установка Finance Assistant 2.1..."
sleep 1

# Проверяем зависимости
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установи его вручную."
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 не найден. Установи его вручную."
    exit 1
fi

# Клонирование проекта или копирование из архива
if [ ! -d "$APP_DIR" ]; then
    mkdir -p "$APP_DIR"
    echo "📂 Распакуй архив finance_assistant_2.1.zip в $APP_DIR перед запуском!"
fi

cd "$APP_DIR"

# Создание виртуального окружения
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
fi

# Активация venv
source venv/bin/activate

# Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt

# Применение миграций БД (если нужно)
if [ ! -f finance.db ]; then
    echo "📦 Создаём базу данных..."
    python3 - <<EOF
import db
print("✅ База данных готова")
EOF
fi

# Запуск приложения
echo "🚀 Запускаем Finance Assistant..."
python3 app.py

