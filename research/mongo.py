import asyncio
import logging
import random
import uuid

from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(level=logging.INFO)


async def generate_data():
    try:
        # Подключаемся к MongoDB
        client = AsyncIOMotorClient("mongodb://root:example@localhost:27017")
        db = client["ugc"]  # Замените 'your_database' на имя вашей базы данных
        collection = db["users"]  # Замените 'your_collection' на имя вашей коллекции

        total_documents = 1_000_000  # Общее количество документов для генерации
        batch_size = 1000  # Размер каждого чанка

        total_inserted = 0

        for batch_start in range(0, total_documents, batch_size):
            documents = []
            current_batch_size = min(batch_size, total_documents - batch_start)

            for _ in range(current_batch_size):
                document = {
                    "_id": str(uuid.uuid4()),
                    "ratings": {
                        str(uuid.uuid4()): random.randint(1, 10) for _ in range(3)
                    },
                    "likes": [str(uuid.uuid4()) for _ in range(2)],
                    "bookmarks": [str(uuid.uuid4()) for _ in range(1)],
                }
                documents.append(document)

            # Вставляем документы в коллекцию
            result = await collection.insert_many(documents)
            batch_inserted = len(result.inserted_ids)
            total_inserted += batch_inserted

            logging.info(
                f"Вставлено документов в текущем чанке: {batch_inserted}, Общее количество вставленных документов: {total_inserted}"
            )

        logging.info("Генерация данных завершена.")

    except Exception as e:
        logging.exception("Ошибка при вставке данных: %s", e)
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(generate_data())
