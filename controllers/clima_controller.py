import json
import re
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError

class ClimaController:
    def consultar(self):
        print("\n--- CONSULTAR CLIMA ---")
        ciudad = input("Ingrese una ciudad (0 para volver): ").strip()

        if ciudad == "0":
            return

        if not ciudad or len(ciudad) > 60:
            print("Error: Ingrese una ciudad válida")
            return

        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s'-]+", ciudad):
            print("Error: La ciudad contiene caracteres no permitidos")
            return

        try:
            parametros = urlencode({
                "name": ciudad,
                "count": 20,
                "countryCode": "CL",
                "language": "es",
                "format": "json"
            })

            url_ciudad = "https://geocoding-api.open-meteo.com/v1/search?" + parametros

            with urlopen(url_ciudad, timeout=10) as respuesta:
                datos_ciudad = json.load(respuesta)

            resultados = datos_ciudad.get("results", [])

            if not resultados:
                print("No se encontró la ciudad en Chile")
                return

            ubicacion = resultados[0]

            if ciudad.casefold() == "san carlos":
                for resultado in resultados:
                    if (
                        resultado.get("name", "").casefold() == "san carlos"
                        and "ñuble" in resultado.get("admin1", "").casefold()
                    ):
                        ubicacion = resultado
                        break

            latitud = ubicacion["latitude"]
            longitud = ubicacion["longitude"]

            parametros_clima = urlencode({
                "latitude": latitud,
                "longitude": longitud,
                "current": "temperature_2m,wind_speed_10m"
            })

            url_clima = "https://api.open-meteo.com/v1/forecast?" + parametros_clima

            with urlopen(url_clima, timeout=10) as respuesta:
                datos_clima = json.load(respuesta)

            clima = datos_clima["current"]

            print(f"\n--- CLIMA EN {ubicacion['name'].upper()} ---")
            print(f"Región: {ubicacion.get('admin1', 'No disponible')}")
            print(f"País: {ubicacion.get('country', 'Chile')}")
            print(f"Temperatura: {clima['temperature_2m']} °C")
            print(f"Velocidad del viento: {clima['wind_speed_10m']} km/h")

        except (URLError, HTTPError, TimeoutError, ValueError, KeyError, TypeError) as e:
            print(f"No se pudo consultar el clima: {e}")
