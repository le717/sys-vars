# python-docker-secret
> Small Python module for easily accessing Docker secrets (particularly on Windows)


## Usage ##
### API ###
```py
from docker_secret import DockerSecret

DockerSecret.set("secret-thing", "secret value")

# Optional second parameter as fallback, like dict.get()
secret_docker_value = DockerSecret.get("secret-thing")
```

### Command-line (set only) ##
```
python docker_secret.py <secret key name> <secret_key_value>
```

## Backstory ##



## License ##
[MIT](LICENSE)

2018 Caleb Ely
