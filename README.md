# python-docker-secrets

> Easily access Docker secrets.

## Usage

- Python 3.6+
- Searches for Docker secret, falls back to environment variables, raises `ValueError` if both fails.

### API

```python
from docker_secrets import get_docker_secret

secret = get_docker_secret("SECRET_KEY")
```

## Backstory

As specified in the [Docker secret docs](https://docs.docker.com/engine/swarm/secrets/#windows-support), Docker for Windows and Windows containers have limited support for secrets and stores secrets in plaintext in an [implementation-detail location](https://docs.docker.com/engine/swarm/secrets/#how-docker-manages-secrets). This location is different for Linux containers, which presents a problem of how to cleanly access secrets in a cross-platform manner, especially if developing in a non-containerized Windows environment. The Linux container secrets location, however, is not an implementation detail. Therefore, the stable Linux secrets location can be used to as a cross-platform, cross-environment manner to access secrets while abiding by OS-specific security details (e.g., encrypted on Linux, plaintext on Windows), which is the function of this script.

This script was inspired by a function being copy-pasted around in various projects at work as well as an in-house native Windows app to create Docker secrets in the aforementioned manner.

## License

[MIT](LICENSE)

2018 Caleb Ely
