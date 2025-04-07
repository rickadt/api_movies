from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from typing import List, Dict
from collections import defaultdict
import csv

# Conexão com o banco sqlite em memória
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# Model da tabela movies do SQLAlchemy
class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    title = Column(String)
    studios = Column(String)
    producers = Column(String)
    winner = Column(String)


# cria o App da API
app = FastAPI()


# Carrega dados do CSV para o SQLite no startup
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    with open("Movielist.csv", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            movie = Movie(
                year=int(row["year"]),
                title=row["title"],
                studios=row["studios"],
                producers=row["producers"],
                winner=row["winner"].strip().lower()
            )
            db.add(movie)
        db.commit()
        db.close()


# Função que calcula os intervalos
def compute_intervals(movies: List[Movie]) -> Dict[str, List[Dict]]:
    wins = defaultdict(list)
    for movie in movies:
        if movie.winner.lower() == "yes":
            producers = [p.strip() for p in movie.producers.replace(" and ", ",").split(",")]
            for producer in producers:
                wins[producer].append(movie.year)

    result = []
    for producer, years in wins.items():
        years.sort()
        if len(years) < 2:
            continue
        for i in range(1, len(years)):
            result.append({
                "producer": producer,
                "interval": years[i] - years[i - 1],
                "previousWin": years[i - 1],
                "followingWin": years[i]
            })

    if not result:
        return {"min": [], "max": []}

    max_interval = max(result, key=lambda x: x["interval"])["interval"]
    min_interval = min(result, key=lambda x: x["interval"])["interval"]

    return {
        "min": [r for r in result if r["interval"] == min_interval],
        "max": [r for r in result if r["interval"] == max_interval],
    }


# Endpoint
@app.get("/producers/intervals")
def get_producer_intervals():
    db = SessionLocal()
    movies = db.query(Movie).all()
    db.close()
    return compute_intervals(movies)
