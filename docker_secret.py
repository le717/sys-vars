# -*- coding: utf-8 -*
"""docker-python-secret: Easily access Docker secrets, particularly on Windows.

Created 2018 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""

import os


__all__ = ["DockerSecret"]


class DockerSecret:
    __path = "/run/secrets/"

    @staticmethod
    def get(secret, default=None):
        """Get a Docker secret.

        @param {String} secret - The name of the Docker secret.
        @param {*} [default=None] - A fallback value if the
                                    Docker secret doesn't exist.
        @return {*} The Docker secret value or the value of @param default.
        """
        try:
            self = DockerSecret
            with open("{}{}".format(self.__path, secret), "rt") as f:
                return f.readline()

        # That secret was not found
        except FileNotFoundError:
            return default

    @staticmethod
    def set(secret, value):
        """Set a Docker secret.

        @param {String} secret - The name of the Docker secret.
        @param {String} value - The value of the Docker secret.
        """
        # Create the path if needed
        self = DockerSecret
        if not os.path.isdir(self.__path):
            os.makedirs(self.__path)

        value = value.strip()
        with open("{}{}".format(self.__path, secret), "wt") as f:
            f.write(value)


if __name__ == "__main__":
    import sys

    # Set the Docker secret
    try:
        secret_name = sys.argv[1]
        secret_value = sys.argv[2]
        DockerSecret.set(secret_name, secret_value)
        print("Docker secret `{}` successfully created.".format(secret_name))

    # We weren't given the information needed
    except IndexError:
        print("""USAGE
{0} <secret key name> <secret_key_value>
 """.format(sys.argv[0]))
