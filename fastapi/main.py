# Importacion de librerias a utilizar

from fastapi import FastAPI
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine
import requests
import logging
import json

# Inicialización de aplicativo con FastAPI
app = FastAPI()

# Configuración de loggin para impresiones en ejecución
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# Conexión a la base de datos postgresql para consulta de manera local ejecutandose desde Docker
engine = create_engine('postgresql://enerbit:QPwoei2025@host.docker.internal:5432/enerbitdb', isolation_level="AUTOCOMMIT")

# Inicialización de objeto loggin para impresiones en ejecución
logger = logging.getLogger(__name__)

# Modelo de datos que se van a recibir por medio de POST
class Pokemon(BaseModel):
    nombre_pokemon_1:str
    nombre_pokemon_2:str

def validacionBatallas(engine, pokemon_1, pokemon_2):

    try:
        df = pd.read_sql_query("""
                                SELECT retador, contrincante, resultados
                                FROM resultado_batallas
                                WHERE (retador = '{0}' AND contrincante = '{1}') 
                                OR (retador = '{1}' AND contrincante = '{0}')
                                """.format(pokemon_1, pokemon_2), con=engine)
        if len(df)>0:
            return True, json.loads(df["resultados"].values[0])[0]
        else:
            return False, {}
    except Exception as e:
        logger.warning(e)
        return False, {}

# Declaración de endpoint POST
@app.post('/pokemon-battle', 
          summary="Batalla Pokemon",
          description="Petición para simulación de batalla pokemon", 
          responses={ 
            200: {
                "description": "Retorna el ganador y el perdedor con sus stats finales o empate con los stats comunes si el pokemon es el mismo",
                "content": {
                    "application/json": {
                        "example": {
                            "ganador": {
                                "nombre": "pidgeotto",
                                "hp": 61,
                                "speed": 71,
                                "attack": 60,
                                "defense": 55
                            },
                            "perdedor": {
                                "nombre": "rattata",
                                "hp": 0,
                                "speed": 72,
                                "attack": 56,
                                "defense": 35
                            }
                        }
                    }
                }   
            },
            422: {
                "description": "Fallo con las variables enviadas",
                "content": {
                    "application/json": {
                        "example": {
                        "detail": [
                            {
                            "type": "string_type -- tipo de fallo",
                            "loc -- en donde se ubica el error y la variable a la que corresponde": [
                                "body",
                                "nombre_pokemon_2"
                            ],
                            "msg": "Input should be a valid string  -- accion a tomar",
                            "input": 1
                            }
                        ]
                        }
                    }
                }
            },
            300: {
                "description": "Pokemon no encontrado",
                "content": {
                    "application/json": {
                         "example": {
                            "pokemon": "picachu",
                            "mensaje": "No existe"
                            }
                    }
                }
            }
            ,
            301: {
                "description": "Fallo al peticionar a la url https://pokeapi.co/api/v2/pokemon/",
                "content": {
                    "application/json": {
                         "example": {
                                "fallo":"Petición GET a https://pokeapi.co/api/v2/pokemon/",
                                "mensaje": "<error de excepción>"
                            }
                    }
                }
            },
            302: {
                "description": "Fallo en el llenado de datos provenientes de https://pokeapi.co/api/v2/pokemon/",
                "content": {
                    "application/json": {
                         "example": {
                                "fallo":"Llenado de datos de cada pokemon antes de la batalla",
                                "mensaje": "<error de excepción>"
                            }
                    }
                }
            },
            303: {
                "description": "Fallo en comparación de stats durante la batalla",
                "content": {
                    "application/json": {
                         "example": {
                                "fallo":"Validación de stats y batalla",
                                "mensaje": "<error de excepción>"
                            }
                    }
                }
            }
        }
        )
def pokemonBattle(pokemon: Pokemon):
    """Función que se ejecuta al consumir el enpoint por medio de POST y que recibe un json con los campos nombre_pokemon_1 y nombre_pokemon_2 ambos string"""

    # Llamado a la conexión de la base de datos que es declarada de manera global
    global engine
    
    nombre_pokemon1 = pokemon.nombre_pokemon_1.strip()
    nombre_pokemon2 = pokemon.nombre_pokemon_2.strip()
    pokemon1_stats = {}
    pokemon2_stats = {}

    # Validación de existencia de batallas entre los pokemon
    val, data = validacionBatallas(engine, nombre_pokemon1, nombre_pokemon2)

    if val:
        return JSONResponse(content=jsonable_encoder(data))
    
    # Petición a la api de pokeapi de donde se extraeran los datos de los pokemon con su respetivo control de error
    try:
        pokedata = requests.get('https://pokeapi.co/api/v2/pokemon/').json()
    except Exception as e:
        return JSONResponse(status_code=301, content=jsonable_encoder({
                            "fallo":"Petición GET a https://pokeapi.co/api/v2/pokemon/",
                            "mensaje": str(e)
                        }))
    
    # Ciclo para extraer los stats de los pokemon peticionados para su confrontación posterior con su respetivo control de error
    try:
        for poke in pokedata["results"]:
            hp = 0
            speed = 0
            attack = 0
            defense = 0

            # Validación existencia de pokemon 1
            if nombre_pokemon1 == poke["name"]:
                pokemon1 = requests.get(poke["url"]).json()['stats']
                
                for stat in pokemon1:
                    if stat["stat"]["name"] == "hp":
                        hp = stat["base_stat"]
                    if stat["stat"]["name"] == "speed":
                        speed = stat["base_stat"]
                    if stat["stat"]["name"] == "attack":
                        attack = stat["base_stat"]
                    if stat["stat"]["name"] == "defense":
                        defense = stat["base_stat"]

                # Llenado de datos en memoria pokemon 1
                pokemon1_stats = {  
                    "nombre":nombre_pokemon1,
                    "hp":hp,
                    "speed":speed,
                    "attack":attack,
                    "defense":defense
                }

            # Validación existencia de pokemon 2
            elif nombre_pokemon2 == poke["name"]:
                pokemon2 = requests.get(poke["url"]).json()['stats']

                for stat in pokemon2:
                    if stat["stat"]["name"] == "hp":
                        hp = stat["base_stat"]
                    if stat["stat"]["name"] == "speed":
                        speed = stat["base_stat"]
                    if stat["stat"]["name"] == "attack":
                        attack = stat["base_stat"]
                    if stat["stat"]["name"] == "defense":
                        defense = stat["base_stat"]

                # Llenado de datos en memoria pokemon 2
                pokemon2_stats = {
                    "nombre":nombre_pokemon2,
                    "hp":hp,
                    "speed":speed,
                    "attack":attack,
                    "defense":defense
                }

    except Exception as e:
        return JSONResponse(status_code=302, content=jsonable_encoder({
                            "fallo":"Llenado de datos de cada pokemon antes de la batalla",
                            "mensaje": str(e)
                        }))
    
    # Respuesta de empate si los pokemon son los mismos
    if nombre_pokemon1 == nombre_pokemon2:
        return JSONResponse(content=jsonable_encoder({
                                "empate":pokemon1_stats
                            }))
        
    # Validación de cargue de pokemon 1 y pokemon 2 en memoria para simular la batalla    
    if len(pokemon1_stats) > 0:
        if len(pokemon2_stats) > 0: 
          
            turno = 0
            ganador = 1 

            # Simulación de batalla comparando la velocidad para ver quien ocupa el primer turno y descontando del defensor los puntos de salud en una cantidad de puntos de ataque del atacante menos los puntos de defensa del defensor. Se hace una validación de que la defensa del atacado sea menos que el ataque ya que si no es asi el no deberia afectarse la salud de este.
            try:
                while ganador:
                    if turno == 0: 
                        if pokemon1_stats["speed"] > pokemon2_stats["speed"]:
                            if pokemon2_stats["defense"] < pokemon1_stats["attack"]:
                                pokemon2_stats["hp"] = pokemon2_stats["hp"] - (pokemon1_stats["attack"] - pokemon2_stats["defense"])
                            turno = 2
                        else:
                            if pokemon1_stats["defense"] < pokemon2_stats["attack"]:
                                logger.info(pokemon1_stats)
                                pokemon1_stats["hp"] = pokemon1_stats["hp"] - (pokemon2_stats["attack"] - pokemon1_stats["defense"])
                            turno = 1
                    else:
                        if turno == 1:
                            if pokemon2_stats["defense"] < pokemon1_stats["attack"]:
                                pokemon2_stats["hp"] = pokemon2_stats["hp"] - (pokemon1_stats["attack"] - pokemon2_stats["defense"])
                            turno = 2
                        else:
                            if pokemon1_stats["defense"] < pokemon2_stats["attack"]:
                                pokemon1_stats["hp"] = pokemon1_stats["hp"] - (pokemon2_stats["attack"] - pokemon1_stats["defense"])
                            turno = 1

                    # Validación de los puntos de vida de cada pokemon despues de cada ataque para encontrar el ganador
                    if pokemon1_stats["hp"] <= 0:
                        pokemon1_stats["hp"] = 0

                        df_resultado = pd.DataFrame({
                                            "retador":[pokemon1_stats["nombre"]],
                                            "contrincante":[pokemon2_stats["nombre"]],
                                            "resultados":json.dumps([{
                                                            "ganador":pokemon2_stats,
                                                            "perdedor":pokemon1_stats
                                                        }])
                                        })
                        
                        # Pesistencia en base de datos de los resultados para futuras consultas y validaciones
                        df_resultado.to_sql("resultado_batallas", if_exists="append", index=False, con=engine)

                        return JSONResponse(content=jsonable_encoder({
                                "ganador":pokemon2_stats,
                                "perdedor":pokemon1_stats
                            }))
                    elif pokemon2_stats["hp"] <= 0:
                        pokemon2_stats["hp"] = 0

                        df_resultado = pd.DataFrame({
                                            "retador":[pokemon1_stats["nombre"]],
                                            "contrincante":[pokemon2_stats["nombre"]],
                                            "resultados":json.dumps([{
                                                            "ganador":pokemon1_stats,
                                                            "perdedor":pokemon2_stats
                                                        }])
                                        })
                        
                        # Pesistencia en base de datos de los resultados para futuras consultas y validaciones
                        df_resultado.to_sql("resultado_batallas", if_exists="append", index=False, con=engine)

                        return JSONResponse(content=jsonable_encoder({
                                "ganador":pokemon1_stats,
                                "perdedor":pokemon2_stats
                            }))
            except Exception as e:
                return JSONResponse(status_code=303, content=jsonable_encoder({
                                    "fallo":"Validación de stats y batalla",
                                    "mensaje": str(e)
                                }))
        else:
            return JSONResponse(status_code=300, content=jsonable_encoder({
                            "pokemon nombre_pokemon_2":str(nombre_pokemon2),
                            "mensaje":"No existe"
                        }))
    else:
        return JSONResponse(status_code=300, content=jsonable_encoder({
                            "pokemon nombre_pokemon_1":str(nombre_pokemon1),
                            "mensaje":"No existe"
                        }))