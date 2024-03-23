from flask import request, abort

from app import app
import storage
import storage.exceptions as storage_exceptions


##### ОБРАБОТЧИКИ ЗАПРОСОВ ПРО ФИЛЬМЫ #####


@app.get("/api/movies")
def get_all_films():
    return {"list": storage.get_all_films()}


@app.get("/api/movies/<film_id>")
def get_film(film_id):
    try:
        found_film = storage.get_film(film_id)
        return {"movie": found_film}
    except storage_exceptions.NotFound:
        return {"status": 500, "reason": "Запрошенной сущности не существует"}, 404
    except Exception as unknown_error:
        return {"status": 500, "reason": f"Неизвестная ошибка {unknown_error}"}, 500


@app.post("/api/movies")
def add_film():
    if "movie" not in request.json:
        return {"status": 500, "reason": "Отсутствует ключ movie во входном JSON"}, 500
    
    try:
        added_movie = storage.add_film(request.json["movie"])
        return {"movie": added_movie}
    except storage_exceptions.BrokenEntity:
        return {"status": 500, "reason": "Передана неправильная сущность"}, 500
    except Exception as unknown_error:
        return {"status": 500, "reason": f"Неизвестная ошибка {unknown_error}"}, 500


@app.patch("/api/movies/<film_id>")
def edit_film(film_id):
    if "movie" not in request.json:
        return {"status": 500, "reason": "Отсутствует ключ movie во входном JSON"}, 500
    
    try:
        added_movie = storage.update_film(request.json["movie"])
        return {"movie": added_movie}
    except storage_exceptions.BrokenEntity:
        return {"status": 500, "reason": "Передана неправильная сущность"}, 500
    except storage_exceptions.NotFound:
        return {"status": 500, "reason": "Запрошенной сущности не существует"}, 404
    except Exception as unknown_error:
        return {"status": 500, "reason": f"Неизвестная ошибка {unknown_error}"}, 500


@app.delete("/api/movies/<film_id>")
def remove_film(film_id):
    try:
        storage.remove_film(film_id)
        abort(202)
    except storage_exceptions.NotFound:
        return {"status": 500, "reason": "Запрошенной сущности не существует"}, 404
    except Exception as unknown_error:
        return {"status": 500, "reason": f"Неизвестная ошибка {unknown_error}"}, 500


##### ОБРАБОТЧИКИ ЗАПРОСОВ ПРО РЕЖИССЁРОВ #####


@app.get("/api/producers")
def get_all_producers():
    return {"list": storage.get_all_producers()}


@app.get("/api/producers/<producer_id>")
def get_producer(producer_id):
    try:
        found_producer = storage.get_film(producer_id)
        return {"producer": found_producer}
    except storage_exceptions.NotFound:
        return {"status": 500, "reason": "Запрошенной сущности не существует"}, 404
    except Exception as unknown_error:
        return {"status": 500, "reason": f"Неизвестная ошибка {unknown_error}"}, 500


@app.post("/api/producers")
def add_producer():
    if "producer" not in request.json:
        return {"status": 500, "reason": "Отсутствует ключ movie во входном JSON"}, 500
    
    try:
        added_producer = storage.add_producer(request.json["producer"])
        return {"movie": added_producer}
    except storage_exceptions.BrokenEntity:
        return {"status": 500, "reason": "Передана неправильная сущность"}, 500
    except Exception as unknown_error:
        return {"status": 500, "reason": f"Неизвестная ошибка {unknown_error}"}, 500


@app.patch("/api/producers/<producer_id>")
def edit_producer(producer_id):
    if "producer" not in request.json:
        return {"status": 500, "reason": "Отсутствует ключ movie во входном JSON"}, 500
    
    try:
        added_producer = storage.update_producer(request.json["producer"])
        return {"producer": added_producer}
    except storage_exceptions.BrokenEntity:
        return {"status": 500, "reason": "Передана неправильная сущность"}, 500
    except storage_exceptions.NotFound:
        return {"status": 500, "reason": "Запрошенной сущности не существует"}, 404
    except Exception as unknown_error:
        return {"status": 500, "reason": f"Неизвестная ошибка {unknown_error}"}, 500


@app.delete("/api/producers/<producer_id>")
def remove_producer(producer_id):
    try:
        storage.remove_producer(producer_id)
        abort(202)
    except storage_exceptions.NotFound:
        return {"status": 500, "reason": "Запрошенной сущности не существует"}, 404
    except Exception as unknown_error:
        return {"status": 500, "reason": f"Неизвестная ошибка {unknown_error}"}, 500
