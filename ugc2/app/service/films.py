from functools import lru_cache


class FilmService:
    def __init__(self, db: BaseDB):
        self.db = db

    async def create_film_if_not_exist(self, film_id):
        result = await collection.find_one({"film_id": film.film_id})
        if result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Film already exists."
            )

        await collection.insert_one(film.dict())
        return film

    async def like_film(self, film_id):
        result = await collection.update_one(
            {"film_id": film_id}, {"$inc": {"likes": 1}}
        )
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Film not found."
            )
        return {"message": "Like added."}

    async def dislike_film(self, film_id):
        result = await collection.update_one(
            {"film_id": film_id}, {"$inc": {"dislikes": 1}}
        )
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Film not found."
            )
        return {"message": "Dislike added."}

    async def get_film_detail(self, film_id):
        film = await collection.find_one({"film_id": film_id})
        if not film:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Film not found."
            )
        return film

    async def rate_film(self, film_id):
        result = await collection.update_one(
            {"film_id": film_id}, {"$push": {"ratings": rating.rating}}
        )
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Film not found."
            )
        return {"message": "Rating added."}

    async def get_film_rate(self, film_id):
        film = await collection.find_one({"film_id": film_id})
        if not film:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Film not found."
            )

        # Вычисление средней оценки
        ratings = film.get("ratings", [])
        if ratings:
            average_rating = sum(ratings) / len(ratings)
        else:
            average_rating = None

        film["average_rating"] = average_rating
        return film


@lru_cache()
def get_users_service() -> FilmService:

    return FilmService()
