# pokemonbattle
Simulador de batallas pokemon desarrollado con FastAPI, se adiciona un directorio con una base de django y una de flask para su revision. los tres se ejecutan igual por docker pero la url es del aplicativo FastAPI para sus pruebas(tener presente ejecutar cada directorio independiente con sus respectivos archivos).

# Requerimientos
* **Postgresql**: Se requiere una base de datos de postgresql ejecutandose en local o modificar la conexión en el script main.py de fastAPI modificando la cadena de conexión en la linea 27
  ```
    engine = create_engine('postgresql://enerbit:QPwoei2025@host.docker.internal:5432/enerbitdb', isolation_level="AUTOCOMMIT")
  ```
  La creación de la tabla de resultados automaticamente la realiza la API.
* **Docker**: Se requiere docker para realizar el despliegue, los compose y dockerfile ya están configurados con lo necesario.

# Ejecución del contenedor
## Para ejecutar el proyecto se ejecuta el siguiente comando dentro del repositorio descargado:
  ```
    docker-compose up --build
  ```
## Si se llega a presentar algun inconveniente con el docker compose, ejecutar la siguiente linea para crear la imagen y luego volver a ejecutar el docker-compose up
  ```
    docker build --pull --rm -f "flask\Dockerfile" -t prueba-enerbit-fastapi:latest "fastapi"
  ```
## Una vez ejecutado este, él se auto configura y despliega para ser consumido por el puerto 80 en la siguiente URL donde podran interactuar con esta:
  [http://localhost/docs](http://localhost/docs)

En el link se puede ver la documentación y realizar peticiones para sus pruebas.

# SQL Tabla 
## En dado caso de requerirse el siguiente es el SQL a ejecutar para la creación de la tabla, pero como se menciona al pricipio, el script se encarga de crearla despues de la primera interacción exitosa.
    ```
    -- Table: public.resultado_batallas

    -- DROP TABLE IF EXISTS public.resultado_batallas;

    CREATE TABLE IF NOT EXISTS public.resultado_batallas
    (
        retador text COLLATE pg_catalog."default",
        contrincante text COLLATE pg_catalog."default",
        resultados text COLLATE pg_catalog."default"
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public.resultado_batallas
        OWNER to enerbit;
    ```
