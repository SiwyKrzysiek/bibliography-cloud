"""
Not in use in favor of Auth0.
Left for sentimental reasons.
"""

import redis
from hashlib import sha256


class UserManager(object):
    """Class for managing user account creation and validation"""

    def __init__(self, redisConnection):
        self.redis = redisConnection

    def addUser(self, login: str, password: str):
        """Add new user to database. Overwrite if user already exists."""
        hash = sha256(password.encode()).hexdigest()

        self.redis.hset('users', login, hash)

    def checkUser(self, login: str) -> bool:
        """Check if user with given login exists"""
        return self.redis.hexists('users', login)

    def validatePassword(self, login: str, password: str) -> bool:
        """Check if user password is valid"""
        hash = sha256(password.encode()).hexdigest().encode()
        return hash == self.redis.hget('users', login)
