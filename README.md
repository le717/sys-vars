# python-docker-secret

> Small Python module for easily accessing Docker secrets (particularly on Windows).

## Usage

* Python 3.3+

### API

```py
from docker_secret import DockerSecret

# Param 1: secret name
# Param 2: secret value
DockerSecret.set("secret-thing", "secret value")

# Optional second parameter as fallback, like dict.get()
secret_docker_value = DockerSecret.get("secret-thing")
```

### Command-line (set only)

```bat
python docker_secret.py <secret key name> <secret_key_value>
```

## Backstory

As specified in the [`docker secret` docs](https://docs.docker.com/engine/swarm/secrets/#windows-support), Docker for Windows and Windows containers have limited support for `secrets` and stores `secrets` in plaintext in an [implementation-detail location](https://docs.docker.com/engine/swarm/secrets/#how-docker-manages-secret). This location is different for Linux containers, which presents a problem of how to cleanly access `secrets` in a cross-platform manner, especially if developing in a non-containerized Windows environment. The Linux container `secrets` location, however, is not an implementation detail. Therefore, the stable Linux secrets location can be used to as a cross-platform, cross-environment manner to access `secrets` while abiding by OS-specific security details (e.g., encrypted on Linux, plaintext on Windows), which is the function of this script.

This script was inspired by a function being copy-pasted around in various projects at work as well as an in-house native Windows app to create Docker `secrets` in the aforementioned manner.

## License

[MIT](LICENSE)

2018 Caleb Ely
