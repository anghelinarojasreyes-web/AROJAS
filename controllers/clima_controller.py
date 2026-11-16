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
                if respuesta.status != 200:
                    print("Error al consultar la ciudad")
                    return
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
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
            })

            url_clima = "https://api.open-meteo.com/v1/forecast?" + parametros_clima

            with urlopen(url_clima, timeout=10) as respuesta:
                if respuesta.status != 200:
                    print("Error al consultar el clima")
                    return
                datos_clima = json.load(respuesta)

            clima = datos_clima["current"]

            estados = {
                0: "Despejado",
                1: "Principalmente despejado",
                2: "Parcialmente nublado",
                3: "Nublado",
                45: "Niebla",
                48: "Niebla",
                51: "Llovizna",
                53: "Llovizna",
                55: "Llovizna intensa",
                61: "Lluvia leve",
                63: "Lluvia moderada",
                65: "Lluvia intensa",
                71: "Nieve leve",
                73: "Nieve moderada",
                75: "Nieve intensa",
                80: "Chubascos leves",
                81: "Chubascos moderados",
                82: "Chubascos intensos",
                95: "Tormenta"
            }

            estado = estados.get(clima["weather_code"], "No disponible")

            print(f"\n--- CLIMA EN {ubicacion['name'].upper()} ---")
            print(f"Región: {ubicacion.get('admin1', 'No disponible')}")
            print(f"País: {ubicacion.get('country', 'Chile')}")
            print(f"Temperatura: {clima['temperature_2m']} °C")
            print(f"Humedad: {clima['relative_humidity_2m']} %")
            print(f"Estado del tiempo: {estado}")
            print(f"Velocidad del viento: {clima['wind_speed_10m']} km/h")

        except HTTPError as e:
            if e.code == 400:
                print("Error 400: Solicitud incorrecta")
            elif e.code == 404:
                print("Error 404: Servicio no encontrado")
            elif e.code >= 500:
                print("Error del servidor. Intente más tarde")
            else:
                print("Error al consultar el servicio")

        except (URLError, TimeoutError):
            print("Error de conexión. Revise su internet e intente nuevamente")

        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            print("Error al procesar los datos recibidos")

