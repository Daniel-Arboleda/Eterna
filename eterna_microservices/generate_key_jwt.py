
'''
Se actualiza la version del archivo para que cuando se crea un nuevo microservicio que necesita la JWT_SECRET_KEY, el script debe ser capaz de agregar la clave al archivo .env de ese microservicio sin generar una nueva clave, para no desconfigurar los servicios existentes.

Modificar el script para que no genere una nueva clave
El script debe ser modificado para verificar si la clave JWT_SECRET_KEY ya existe en el archivo .env antes de intentar agregarla. Si la clave no existe, se generará y se añadirá, pero si ya existe, el script simplemente no hará nada y no modificará el archivo.

Lista de rutas de los microservicios (microservices_env_paths): Se define una lista que contiene las rutas de todos los archivos .env de los microservicios que necesitan la JWT_SECRET_KEY. En este caso, se incluyen auth_service y register_service, pero puedes agregar otros microservicios a la lista si los necesitas.

Función check_if_jwt_secret_exists: Esta función verifica si la clave JWT_SECRET_KEY ya está presente en el archivo .env de un microservicio dado. Si existe, no se agregará una nueva clave.

Función add_jwt_secret_to_env: En esta función, el script recorre todos los archivos .env de la lista, verifica si la JWT_SECRET_KEY ya existe y, si no, la agrega. Si ya existe, se imprime un mensaje indicando que no se agregará la clave.

¿Qué hacer cuando se agregue un nuevo microservicio?
Cuando se agregue un nuevo microservicio que necesite la JWT_SECRET_KEY, simplemente añade su ruta .env al arreglo microservices_env_paths en el script.

Por ejemplo, si agregas un microservicio llamado profile_service, añade la ruta correspondiente:

microservices_env_paths = [
    "./auth_service/.env",
    "./register_service/.env",
    "./profile_service/.env",  # Nuevo microservicio
]


'''

import secrets
import os
from dotenv import load_dotenv

# Directorio donde está el script generate_key_jwt.py
script_directory = os.path.dirname(os.path.abspath(__file__))

# Lista de los archivos .env de los microservicios que deben contener la JWT_SECRET_KEY
microservices_env_paths = [
    os.path.join(script_directory, "auth_service", ".env"),
    # os.path.join(script_directory, "register_service", ".env"),  # Descomenta si tienes más microservicios
    # Puedes agregar más microservicios aquí, si es necesario.
]

# Función para obtener la clave JWT existente del archivo .env
def get_existing_jwt_secret(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            # Buscar la línea con la clave JWT_SECRET_KEY
            for line in content.splitlines():
                if line.startswith("JWT_SECRET_KEY="):
                    return line.split('=')[1].strip()
    return None

# Función para verificar si la JWT_SECRET_KEY ya existe en el archivo .env
def check_if_jwt_secret_exists(file_path):
    return get_existing_jwt_secret(file_path) is not None

# Función para agregar o actualizar la clave JWT_SECRET_KEY en el archivo .env
def add_jwt_secret_to_env():
    jwt_secret_key = secrets.token_urlsafe(64)  # Generar la nueva clave JWT
    
    for env_path in microservices_env_paths:
        if not os.path.exists(env_path):
            print(f"Error: El archivo {env_path} no existe.")
            continue  # Saltar al siguiente archivo si no existe
        
        existing_secret = get_existing_jwt_secret(env_path)
        
        if existing_secret is None:
            # Si no existe la clave, agregarla al archivo .env
            try:
                with open(env_path, 'a') as file:
                    file.write(f"JWT_SECRET_KEY={jwt_secret_key}\n")
                print(f"JWT_SECRET_KEY agregada al archivo .env de {env_path}")
            except PermissionError:
                print(f"Error: No se tienen permisos suficientes para escribir en el archivo {env_path}")
        elif existing_secret != jwt_secret_key:
            # Si la clave es incorrecta, actualizarla con la nueva generada
            try:
                with open(env_path, 'r') as file:
                    lines = file.readlines()
                
                with open(env_path, 'w') as file:
                    for line in lines:
                        # Reemplazar la línea de la clave JWT_SECRET_KEY si es diferente
                        if line.startswith("JWT_SECRET_KEY="):
                            file.write(f"JWT_SECRET_KEY={jwt_secret_key}\n")
                        else:
                            file.write(line)
                print(f"JWT_SECRET_KEY actualizada en el archivo .env de {env_path}")
            except PermissionError:
                print(f"Error: No se tienen permisos suficientes para escribir en el archivo {env_path}")
        else:
            # Si la clave es correcta, no hacer nada
            print(f"JWT_SECRET_KEY ya es correcta en {env_path}, no se necesita cambiarla.")

# Ejecutar la función para agregar o actualizar la clave
add_jwt_secret_to_env()
