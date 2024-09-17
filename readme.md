# ¿Como correr el proyecto?

1. Instala las dependencias con poetry
   `poetry install`
2. Inicia mongo en tu local (CMD/Powershell/Bash)
   `mongo`
3. Popula la base de datos

```
    poetry shell
    python3 -m lib.seed.mongo_seed
```

4. Inicia el proyecto
   `fastapi dev apps/cart_api/main.py`

# ¿Cómo correr los tests?

### Con coverage

`pytest --cov`

### Sin coverage

`pytest`

# ¿Cómo correr el proyecto en Docker?

Asegurate de que docker daemon está corriendo en tu maquina.

### Haz el build con

`docker build -t mds_cart_api:latest -f Dockerfile .`

### Corre el contenedor con

`docker run mds_cart_api:latest`
