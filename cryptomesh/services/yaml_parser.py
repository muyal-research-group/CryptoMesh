import yaml
import os
from cryptomesh.models import Policy

# Obtener la ruta base de la carpeta cryptomesh
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
YAML_PATH = os.path.join(BASE_DIR, "policies/example_1.yml")

def load_yaml(file_path: str = YAML_PATH) -> Policy:
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
        return Policy(**data)  # Validación con Pydantic

# Prueba de lectura
if __name__ == "__main__":
    policy = load_yaml()
    print(policy)
