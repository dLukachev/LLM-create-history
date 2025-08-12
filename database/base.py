from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Создаём подключение к базе
engine = create_engine('sqlite:///history.db', echo=True)  # echo=True для логов SQL

# Базовый класс для моделей
Base = declarative_base()