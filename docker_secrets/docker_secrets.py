# -*- coding: utf-8 -*
"""python-docker-secrets: Easily access Docker secrets.

Created 2018 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""

from os import environ
from os.path import join, sep


__all__ = ["get_docker_secret"]


def get_docker_secret(secret: str) -> str:
    """Get a Docker secret value, falling back to os.environ.

    This function raises a ValueError if the secret could not be found.

    @param {str} secret - The secret key name.
    @return {str} - The value for the secret.
    """
    path = join(sep, "run", "secrets", secret)

    try:
        # Try to get the Docker secret value
        with open(path, "rt") as f:
            secret_value = f.read().strip()

    # The secret does not exist
    except FileNotFoundError:
        # Try to get it from the environment
        secret_value = environ.get(secret, "")

    # The secret could not be loaded at all
    if not secret_value:
        raise ValueError("Could not get value for secret {}".format(secret))
    return secret_value
