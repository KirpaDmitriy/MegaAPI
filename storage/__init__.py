from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app import app
from storage_exceptions import NotFound, BrokenEntity


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/postgres"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class FilmModel(db.Model):
    __tablename__ = "films"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    year = db.Column(db.Integer())
    length = db.Column(db.String())
    rating = db.Column(db.Integer())

    def __init__(self, title, year, length, rating) -> None:
        assert isinstance(title, str)
        assert len(title) <= 100
        assert isinstance(year, int)
        assert 1900 <= year <= 2100

        self.title = title
        self.year = year
        self.length = length
        self.rating = rating

    def __repr__(self) -> str:
        return f"<Film {self.title} ({self.year})>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title, 
            "year": self.year,
            "length": self.length,
            "rating": self.rating,
        }


class ProducerModel(db.Model):
    __tablename__ = "producers"

    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String())

    def __init__(self, fio) -> None:
        assert isinstance(fio, str)
        assert len(fio) <= 100

        self.fio = fio

    def __repr__(self) -> str:
        return f"<Producer {self.fio}>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "fio": self.fio,
        }



def get_all_films() -> list[dict]:
    return [film.to_dict() for film in FilmModel.query.all()]


def get_all_producers() -> list[dict]:
    return [producer.to_dict() for producer in ProducerModel.query.all()]


def get_film(film_id) -> dict:
    try:
        return FilmModel.query.get(film_id).to_dict()
    except Exception:
        raise NotFound("Фильм с id {film_id} не найден")


def get_producer(producer_id) -> dict:
    try:
        return ProducerModel.query.get(producer_id).to_dict()
    except Exception:
        raise NotFound("Продюссер с id {producer_id} не найден")


def add_film(film: dict) -> dict:
    try:
        new_film = FilmModel(
            title=film["title"], year=film["year"], length=film["length"], rating=film["rating"]
        )
    except Exception:
        raise BrokenEntity("Сущность сформатирована неправильно")
    db.session.add(new_film)
    db.session.commit()
    return FilmModel.query.get(new_film.id).to_dict()


def add_producer(producer: dict) -> dict:
    try:
        new_producer = ProducerModel(fio=producer["fio"])
    except Exception:
        raise BrokenEntity("Сущность сформатирована неправильно")
    db.session.add(new_producer)
    db.session.commit()
    return FilmModel.query.get(new_producer.id).to_dict()


def update_film(film: dict) -> dict:
    return add_film(get_film(film["id"]))


def update_producer(producer: dict) -> dict:
    return add_producer(get_producer(producer["id"]))


def remove_film(film_id) -> None:
    db.session.add(get_film(film_id))
    db.session.commit()


def remove_producer(producer_id) -> None:
    db.session.add(get_producer(producer_id))
    db.session.commit()
