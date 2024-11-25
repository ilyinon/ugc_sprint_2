import asyncio
import logging
import random
import uuid

import asyncpg

logging.basicConfig(level=logging.INFO)


async def generate_data():
    try:
        # Подключаемся к базе данных PostgreSQL
        conn = await asyncpg.connect(
            user="user",  # Замените на ваше имя пользователя
            password="pass",  # Замените на ваш пароль
            database="ugc",  # Замените на имя вашей базы данных
            host="127.0.0.1",  # Замените на ваш хост, если необходимо
        )

        total_users = 1_000_000  # Общее количество пользователей
        batch_size = 1000  # Размер каждого чанка
        total_inserted = 0

        for batch_start in range(0, total_users, batch_size):
            users = []
            ratings = []
            likes = []
            bookmarks = []
            current_batch_size = min(batch_size, total_users - batch_start)

            for _ in range(current_batch_size):
                user_id = uuid.uuid4()
                users.append(user_id)

                # Генерация рейтингов
                for _ in range(3):
                    item_id = uuid.uuid4()
                    rating = random.randint(1, 10)
                    ratings.append((user_id, item_id, rating))

                # Генерация лайков
                for _ in range(2):
                    item_id = uuid.uuid4()
                    likes.append((user_id, item_id))

                # Генерация закладок
                for _ in range(1):
                    item_id = uuid.uuid4()
                    bookmarks.append((user_id, item_id))

            # Вставка данных в таблицу users
            await conn.executemany(
                "INSERT INTO users(id) VALUES($1)", [(user_id,) for user_id in users]
            )

            # Вставка данных в таблицу ratings
            await conn.executemany(
                "INSERT INTO ratings(user_id, item_id, rating) VALUES($1, $2, $3)",
                ratings,
            )

            # Вставка данных в таблицу likes
            await conn.executemany(
                "INSERT INTO likes(user_id, item_id) VALUES($1, $2)", likes
            )

            # Вставка данных в таблицу bookmarks
            await conn.executemany(
                "INSERT INTO bookmarks(user_id, item_id) VALUES($1, $2)", bookmarks
            )

            total_inserted += current_batch_size
            logging.info(
                f"Общее количество вставленных пользователей: {total_inserted}"
            )

        logging.info("Генерация данных завершена.")

    except Exception as e:
        logging.exception("Ошибка при вставке данных: %s", e)
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(generate_data())
