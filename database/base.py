from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv('DATABASE_URL', 'sqlite:///history.db')

# Создаём подключение к базе
engine = create_engine(URL, echo=True)  # echo=True для логов SQL

# Базовый класс для моделей
Base = declarative_base()