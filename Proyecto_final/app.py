from flask import Flask, request, jsonify
from flask_cors import CORS
import json

class DogData:
    """Clase para manejar la lógica relacionada con los datos de perros."""
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        """Carga datos desde el archivo JSON."""
        try:
            with open(self.data_file, 'r') as archivo_json:
                return json.load(archivo_json)
        except FileNotFoundError:
            return []

    def filter_data(self, filters):
        """Aplica filtros a los datos y devuelve los resultados."""
        filtered_data = self.data
        mapeo_filtros = {
            "Amigable": "Friendly Rating (1-10)",
            "Tamaño": "Size",
            "Cuidado del Pelaje": "Grooming Needs",
            "Bueno con niños": "Good with Children",
            "Inteligencia": "Intelligence Rating (1-10)",
            "Nivel de muda": "Shedding Level",
            "Dificultad de entrenamiento": "Training Difficulty (1-10)"
        }

        mapeo_valores = {
            "small": (1, 3),
            "media": (4, 7),
            "alta": (8, 10),
            "pequeño": "Small",
            "pequeño-mediano": "Small-Medium",
            "mediano": "Medium",
            "grande": "Large",
            "gigante": "Giant",
            "si": "Yes",
            "no": "No"
        }

        for key, value in filters.items():
            if not value:
                continue
            # Convertir el filtro en el campo correspondiente
            field = mapeo_filtros.get(key, key)
            # Aplicar lógica de filtrado
            if field in ["Friendly Rating (1-10)", "Intelligence Rating (1-10)", "Training Difficulty (1-10)"]:
                if value == "media":
                    filtered_data = [item for item in filtered_data if 1 <= int(item.get(field, 0)) <= 7]
                elif value == "alta":
                    filtered_data = [item for item in filtered_data if 8 <= int(item.get(field, 0)) <= 10]
            elif field == "Size":
                size = mapeo_valores.get(value)
                if isinstance(size, tuple):
                    filtered_data = [item for item in filtered_data if size[0] <= int(item.get(field, 0)) <= size[1]]
                else:
                    filtered_data = [item for item in filtered_data if item.get(field, '').lower() == size.lower()]
            elif field in ["Grooming Needs", "Shedding Level"]:
                mapping = {"baja": "Low", "media": "Moderate", "alta": "High"}
                shedding_value = mapping.get(value)
                if shedding_value:
                    filtered_data = [item for item in filtered_data if item.get(field, '') == shedding_value]
            elif field in ["Good with Children", "Origin", "Type"]:
                filtered_data = [item for item in filtered_data if item.get(field, '').lower() == value.lower()]
            else:
                filtered_data = [item for item in filtered_data if str(item.get(field, '')).lower() == value.lower()]

        return filtered_data


class DogAPI:
    """Clase para encapsular la API Flask."""
    def __init__(self, dog_data):
        self.app = Flask(__name__)
        CORS(self.app)
        self.dog_data = dog_data
        self.setup_routes()

    def setup_routes(self):
        """Define las rutas de la API."""
        @self.app.route('/api/dogs', methods=['GET'])
        def obtener_dogs():
            filtros = request.args
            datos_filtrados = self.dog_data.filter_data(filtros)
            return jsonify(datos_filtrados)

    def run(self):
        """Ejecuta la aplicación Flask."""
        self.app.run(debug=True)


if __name__ == '__main__':
    dog_data = DogData('Proyecto_final/data/dogs.json')
    api = DogAPI(dog_data)
    api.run()
