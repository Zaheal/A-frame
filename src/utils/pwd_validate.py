from fastapi_users import InvalidPasswordException

from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher
from pwdlib.exceptions import UnknownHashError



async def validate_password(password, email):
    if len(password) < 8:
        raise InvalidPasswordException(
            reason="Password should be at least 8 characters"
        )


def verify_pwd(
        password: str | bytes, hash: str | bytes
    ) -> bool:
    """
    Verifies if a password matches a given hash.

    Args:
        password: The password to be checked.
        hash: The hash to be verified.

    Returns:
        True if the password matches the hash, False otherwise.

    Raises:
        exceptions.UnknownHashError: If the hash is not recognized by any of the hashers.

    Examples:
        >>> password_hash.verify("herminetincture", hash)
        True

        >>> password_hash.verify("INVALID_PASSWORD", hash)
        False
    """
    hashers = (Argon2Hasher(), BcryptHasher())
    for hasher in hashers:
        if hasher.identify(hash):
            return hasher.verify(password, hash)
    raise UnknownHashError(hash)