import datetime
from typing import List

from sqlalchemy import select, insert, delete, update
from sqlalchemy.future import Engine

from src.database import tables
from src.user.models import UserResponseV1, UserAddRequestV1, StatsRepo, ResultUserRepo
import requests


class UserService:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def get_all_users(self) -> List[UserResponseV1]:
        query = select(tables.users)
        with self._engine.connect() as connection:
            users_data = connection.execute(query)
        users = []
        for user_data in users_data:
            user = UserResponseV1(
                id=user_data['id'],
                login=user_data['login'],
                name=user_data['name']
            )
            users.append(user)
        return users

    def get_user_by_id(self, id: int) -> UserResponseV1:
        query = select(tables.users).where(tables.users.c.id == id)
        with self._engine.connect() as connection:
            user_data = connection.execute(query)
        user = UserResponseV1(
            id=user_data['id'],
            login=user_data['login'],
            name=user_data['name']
        )
        return user

    def add_user(self, user: UserAddRequestV1) -> None:
        query = insert(tables.users).values(
            id=user.id,
            login=user.login,
            name=user.name
        )
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()

    def delete_user_by_id(self, id: int) -> None:
        query = delete(tables.users).where(tables.users.c.id == id)
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()

    def status_repo_by_id(self, id: int) -> None:
        query = select(tables.users, tables.stats).where(tables.users.c.id == id)
        with self._engine.connect() as connection:
            user_data = connection.execute(query)
        user = UserResponseV1(
            id=user_data['id'],
            login=user_data['login'],
            name=user_data['name']
        )
        repo = StatsRepo(
            repo_id=user_data['id'],
            date=user_data['data'],
            stargazers=user_data['stargazers'],
            forks=user_data['forks'],
            watchers=user_data['wachers']
        )
        result = ResultUserRepo(
            users=user,
            stats=repo
        )

        return result

    def update_repo_status(self):
        data_to = datetime.datetime.time()
        data_from = datetime.time(0, 00, 00)
        if data_to == data_from:
            query = select(tables.users)
            with self._engine.connect() as connection:
                users_data = connection.execute(query)
            users = []
            for user_data in users_data:
                user = UserResponseV1(
                    id=user_data['id'],
                    login=user_data['login'],
                    name=user_data['name']
                )
                users.append(user)

                if user in users:
                    response = requests.get(url=f'https://api.github.com/users/{user.name}/repos')
                    for repos in response.json():
                        query = update(tables.stats).values(
                            repo_id=repos['id'],
                            date=repos['updated_data'],
                            stargazers=repos['stargazers_count'],
                            forks=repos['forks'],
                            watchers=repos['watchers']
                        )

                    with self._engine.connect() as connection:
                        connection.execute(query)
                        connection.commit()
