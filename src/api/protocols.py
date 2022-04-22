from typing import List, Dict

from src.user.models import UserResponseV1, UserAddRequestV1,ResultUserRepo


class UserServiceProtocol:
    def get_all_users(self) -> List[UserResponseV1]:
        raise NotImplementedError

    def get_user_by_id(self, id: int) -> UserResponseV1:
        raise NotImplementedError

    def add_user(self, user: UserAddRequestV1) -> None:
        raise NotImplementedError

    def delete_user_by_id(self, id: int) -> None:
        raise NotImplementedError

    def status_repo_by_id(self, id: int) -> ResultUserRepo:
        return ResultUserRepo
