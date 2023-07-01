import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker
# from my_interface_work_7_1_1_ishet_ne_povtoriaet_1 import BotInterface
import config
from config import comunity_token, acces_token, db_url_object
from config import db_url_object


def database_exists():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname='IgorIgor3'")
    exists = cursor.fetchone()
    cursor.close()
    conn.close()

    return exists is not None



def create_database():  # подкючается к базе данных которя 100% существует
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    db_name = "test"

    try:
        cursor.execute(f"CREATE DATABASE {db_name};")
        print(f"Database '{db_name}' created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the database ага вот тут вылетает зараза: {e}")
    finally:
        cursor.close()
        conn.close()


# Database schema
# metadata = MetaData()
Base = declarative_base()


class Viewed(Base):
    __tablename__ = 'viewed'
    id = sq.Column(sq.Integer, primary_key=True,  autoincrement=True)
    profile_id = sq.Column(sq.Integer, primary_key=True)
    worksheet_id = sq.Column(sq.Integer, primary_key=True)


# Добавляем данные
def add_user(engine, profile_id, worksheet_id):
    with Session(engine) as session:
        to_bd = Viewed(profile_id=profile_id, worksheet_id=worksheet_id)
        session.add(to_bd)
        session.commit()


# Проверяем наличие
# def check_user(engine, profile_id, worksheet_id):
#     with Session(engine) as session:
#         from_bd = session.query(Viewed).filter(
#             Viewed.profile_id == profile_id,
#             Viewed.worksheet_id == worksheet_id
#         ).first()
#         if from_bd:
#             return True
#         else:
#             to_bd = Viewed(profile_id=profile_id, worksheet_id=worksheet_id)
#             session.add(to_bd)
#             session.commit()
#             return False
def check_user(engine, profile_id, worksheet_id):
    with Session(engine) as session:
        from_bd = session.query(Viewed).filter(
            Viewed.profile_id == profile_id,
            Viewed.worksheet_id == worksheet_id
        ).first()
        if from_bd:
            return True
        else:
            to_bd = Viewed(profile_id=profile_id, worksheet_id=worksheet_id)
            session.add(to_bd)
            session.commit()
            return False
engine = create_engine("postgresql://test:test@localhost:5432/test")

if __name__ == "__main__":
    # if not database_exists():
    #     create_database()  # создаёт базу данных, проверял, создается
    #     if not database_exists():
    #         create_database()  # Тут просто уже создавал, чтобы хоть как то заработало убирая проверку,
        engine = create_engine("postgresql://test:test@localhost:5432/test")

        Base.metadata.create_all(engine)

        # bot_interface = BotInterface(comunity_token, acces_token)
        #
        # worksheet_id = bot_interface.event_handler()
        #
        # add_user(engine,  worksheet_id)
        #
        # check_user(engine, worksheet_id)
        #
        # res = check_user(engine, worksheet_id)
        #
        # print(res)




