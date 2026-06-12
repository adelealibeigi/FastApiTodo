import bcrypt

from src.core.service_contract.interface.ipassword_hasher import IPasswordHasher


class PasswordHasher(IPasswordHasher):

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, plain_password: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed.encode("utf-8"))
