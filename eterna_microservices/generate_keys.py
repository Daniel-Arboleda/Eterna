'''
# Para activar el archivo 

¿Cómo ejecutar el script?
Ubicación del script: Colócalo en la raíz de tu proyecto (eterna_microservices/generate_keys.py).

Ejecutarlo:
Asegúrate de tener el entorno virtual activado y ejecuta el script con el siguiente comando:::

python generate_keys.py

# Para configurar el archivo

¿Cómo configurar la rotación periódica?
Si deseas que el script se ejecute automáticamente cada mes, puedes usar cron jobs (en sistemas Unix/Linux) para ejecutar este script. Aquí te dejo un ejemplo de cómo hacerlo:::

Crear un cron job para ejecutar el script el 1 de cada mes:
Abre el archivo de cron jobs con el siguiente comando:

crontab -e

Agrega la siguiente línea para ejecutar el script el 1 de cada mes a las 00:00:::

0 0 1 * * /ruta/a/python /ruta/a/eterna_microservices/generate_keys.py

Asegúrate de reemplazar /ruta/a/python y /ruta/a/eterna_microservices/generate_keys.py con las rutas correctas en tu sistema.

Este cron job ejecutará el script de generación de claves el primer día de cada mes, renovando las claves automáticamente.

# versión mejorada del script que asegura que las claves se generen cuando se ejecute por primera vez (independientemente de la fecha) y luego se actualicen al 1º de cada mes ::: Generación de claves si no existen: Si es la primera vez que se ejecuta el script y las claves no están en el archivo .env (verificado con la función check_if_keys_exist), las claves se generarán y guardarán inmediatamente.

Rotación de claves el 1º de cada mes: Si el script se ejecuta en el 1º de cada mes (o en cualquier otra fecha posterior), las claves se actualizarán.

Arvhibo actualizado para que despues de generar la clave en vez de solo agregar una nueva linea de codigo al final con la nueva clave creada, el escript ahora buscara la clave antigua en el archivo, la borara y la actualizara por la nueva asi evitando duplicidad y evitando errores en la implementacion de este script automatizado

Función replace_key_in_file:

Esta función busca una clave específica (key) dentro de un archivo .env y reemplaza su valor con el nuevo valor (new_value).
Si la clave ya existe en el archivo, la función sobrescribe su valor. Si no existe, deja el archivo tal como está.
Reemplazo de claves:

En lugar de agregar las claves al final de los archivos .env, se busca y reemplaza las claves COMMON_SECRET_KEY y SECRET_KEY en los archivos correspondientes.
Esto asegura que las claves se actualicen sin crear duplicados.

# Se actualiza la version del archivo mejorando la seguridad en el manejo y tramite de las variables de entorno en el archivo .env de los microservicios usando la libreria de python-dotenv en el venv de la raiz principal de eterna_microservices.

Flujo de seguridad:
Cargar las claves desde el archivo .env: Usando load_dotenv(), las claves ya están disponibles como variables de entorno sin necesidad de escribirlas directamente en el código.
Actualizar las claves de forma controlada: Usamos set_key() para asegurarnos de que las claves se actualicen de manera segura sin crear duplicados.
Evitar exponer las claves: Las claves secretas no están hardcodeadas en el código, sino que se gestionan y actualizan de manera controlada a través de los archivos .env.
Con esta adaptación, el manejo de las claves es más seguro y modular.

'''
import os
import secrets
from datetime import datetime
from dotenv import load_dotenv, set_key

# Ruta de los archivos .env
root_env_path = "./.env"  # Ruta al archivo .env de la raíz (eterna_microservices)
auth_service_env_path = "./auth_service/.env"  # Ruta al archivo .env de auth_service
register_service_env_path = "./register_service/.env"  # Ruta al archivo .env de register_service

# Definir la fecha de rotación de las claves (1 de cada mes)
rotation_date = datetime(datetime.now().year, datetime.now().month, 1)

# Cargar las variables de entorno del archivo .env de la raíz
load_dotenv(root_env_path)

# Función para verificar si las claves existen en el archivo .env
def check_if_keys_exist(path):
    if not os.path.exists(path):
        return False
    with open(path, 'r') as file:
        content = file.read()
        return 'COMMON_SECRET_KEY=' in content and 'SECRET_KEY=' in content

# Función para reemplazar una clave en un archivo .env
def replace_key_in_file(file_path, key, new_value):
    # Cargar el archivo .env correspondiente
    load_dotenv(file_path)
    
    # Usar `set_key` de dotenv para actualizar las claves de manera segura
    set_key(file_path, key, new_value)
    
    print(f"Clave actualizada: {key} en {file_path}")

# Función para generar nuevas claves
def generate_keys():
    common_secret_key = secrets.token_urlsafe(64)  # Clave común para los microservicios
    auth_service_secret_key = secrets.token_urlsafe(64)  # Clave secreta para auth_service
    register_service_secret_key = secrets.token_urlsafe(64)  # Clave secreta para register_service

    # Reemplazar las claves en el archivo .env de la raíz
    replace_key_in_file(root_env_path, 'COMMON_SECRET_KEY', common_secret_key)

    # Reemplazar las claves en los archivos .env específicos de los microservicios
    replace_key_in_file(auth_service_env_path, 'SECRET_KEY', auth_service_secret_key)
    replace_key_in_file(register_service_env_path, 'SECRET_KEY', register_service_secret_key)

    print("Claves generadas y guardadas en los archivos .env correspondientes.")

# Verificar si las claves existen en el archivo .env de la raíz
if not check_if_keys_exist(root_env_path):
    print("No se encontraron claves, generando nuevas...")
    generate_keys()

# Verificar si es la fecha de rotación (1 de cada mes)
if datetime.now() >= rotation_date:
    print("Es la fecha de rotación, generando nuevas claves...")
    generate_keys()
else:
    print("No es la fecha de rotación. No se generaron nuevas claves.")
