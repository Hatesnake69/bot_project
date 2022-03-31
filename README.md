

## Внутренний проект компаний **Ylab**

**Для запуска проекта, выполните следующие шаги:**
* Создайте своего собтсвенного бота
https://telegram.me/BotFather

* Создайте виртуальное окружение и установите зависимости
```
python -m venv venv
&&
pip install -r requirements.txt
```
* Скопируйте файл с переменными окружения
```sh
cp .env.example .env
```
* Установите в переменную `BOT_TOKEN`, токен своего созданного бота
```
BOT_TOKEN=...
```
# Запустить docker контейнер 
```sh
docker run -p 6379:6379 -d redis:5
```
Для остановки или перезапуска Redis использовать:
```sh
/etc/init.d/redis-server stop
/etc/init.d/redis-server restart
```
После всех выполненных шагов, запускаем наш файл `bot.py`
```sh
python bot.py

После всех выполненных шагов, запускаем 
```bash
docker compose up -d --build
```

Остановить:
```bash
docker compose stop
```

Уничтожить:
```bash
docker-compose down -v
```