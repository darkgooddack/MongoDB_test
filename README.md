# MongoDB_test
Этот репозиторий — небольшая песочница для изучения работы с MongoDB и асинхронным клиентом Motor.

# Установка
1. Создай виртуальное окружение:
```
python -m venv venv
```
2. Активируй его:
```
source venv/bin/activate  # или venv\Scripts\activate на Windows
```
3. Установи зависимости:
```
pip install fastapi motor uvicorn pydantic_settings
```
4. Установи [MongoDB Compas](https://www.mongodb.com/try/download/compass) — удобный GUI-клиент.
5. Поднимай MongoDB в Docker:
```
docker run -d -p 27017:27017 --name mongo mongo
```
# Настройки
Создай .env в корне проекта:
```
mongodb_uri=mongodb://localhost:27017
mongodb_db=test
```

# Подключение к MongoDB
```
from motor.motor_asyncio import AsyncIOMotorClient
from app.infrastructure.config import settings

client = AsyncIOMotorClient(settings.mongodb_uri)   # Клиент MongoDB
db = client[settings.mongodb_db]                     # База данных
collection = db.users                                # Коллекция (таблица)
```
Коллекции и базы данных создаются автоматически при первом обращении.

# ObjectId
MongoDB по умолчанию создаёт уникальные _id — это ObjectId, а не обычная строка:
```
from bson import ObjectId

id = ObjectId("64ed....")  # Преобразование str в ObjectId
```

# Pydantic-модели
Используем две модели: одна с id (для вывода), другая без (для создания). 
Мы не передаём id при создании, MongoDB генерирует его автоматически.

# Методы коллекций

Вставка одного документа (dict)
```
await collection.insert_one(
    {
        "name": "Alice", 
        "email": "a@example.com"
    }
)
```

Поиск одного документа (искать можно по любому полю)
```
doc = await collection.find_one(
    {
        "_id": ObjectId(id)
    }
)
```
Поиск нескольких документов (пустые фигурные скобки = без фильтра)
```
cursor = collection.find({})
async for doc in cursor:
    print(doc)
```

Обновление
```
result = await collection.update_one(
    {"_id": ObjectId(id)},       # фильтр
    {"$set": {"name": "Bob"}}    # что обновить
)
```

Удаление
```
await collection.delete_one({"_id": ObjectId(id)})
```

Примеры операторов:
```
{"$set": {"name": "Alice"}}        # Обновить поле 'name' на 'Alice'
{"$inc": {"age": 1}}               # Увеличить поле 'age' на 1
{"$unset": {"email": ""}}         # Удалить поле 'email'
{"$rename": {"nickname": "alias"}}# Переименовать поле 'nickname' в 'alias'
{"$push": {"tags": "new"}}        # Добавить элемент в массив 'tags'
{"$pull": {"tags": "old"}}        # Удалить элемент из массива 'tags'
{"$addToSet": {"roles": "admin"}} # Добавить в массив, если такого элемента нет
```

# Запуск сервера
```
uvicorn app.main:app --reload
```
