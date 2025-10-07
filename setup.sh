#!/bin/bash
set -e

echo "🚀 Установка Finance Assistant 2.1..."

sudo apt update
sudo apt install -y python3 python3-venv python3-pip

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

if [ ! -f "finance.db" ]; then
  echo "📂 Создаём базу данных..."
  python3 -c "import db; db.init_db()"
fi

echo "✅ Установка завершена!"
echo "Запуск: source venv/bin/activate && python3 app.py"
