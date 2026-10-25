import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "TU_API_KEY"  # <- reemplaza por tu clave de Graphhopper

# Perfiles que ve el usuario -> valor que entiende la API
PERFILES = {
    "auto": "car", "bicicleta": "bike", "a pie": "foot",
    "car": "car", "bike": "bike", "foot": "foot",
}
SALIR = ("s", "salir")


def quiere_salir(texto):
    return texto.strip().lower() in SALIR


def pedir(mensaje):
    """Pide un dato. Repite si queda vacío. Devuelve None si el usuario quiere salir."""
    while True:
        texto = input(mensaje).strip()
        if quiere_salir(texto):
            return None
        if texto != "":
            return texto
        print("Debes ingresar un valor (o 's' / 'salir' para terminar).")


def geocoding(location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode(
        {"q": location, "limit": "1", "locale": "es", "key": key}
    )
    replydata = requests.get(url)
    json_status = replydata.status_code
    json_data = replydata.json()

    if json_status == 200 and len(json_data["hits"]) != 0:
        hit = json_data["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        name = hit["name"]
        value = hit["osm_value"]
        country = hit.get("country", "")
        state = hit.get("state", "")
        if state and country:
            new_loc = name + ", " + state + ", " + country
        elif country:
            new_loc = name + ", " + country
        else:
            new_loc = name
        print("URL de la API de geocodificación para " + new_loc
              + " (Tipo de ubicación: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de la API de geocodificación: " + str(json_status)
                  + "\nMensaje de error: " + str(json_data.get("message", "")))
        else:
            print("No se encontró la ubicación '" + location + "'. Intenta con otro nombre.")
    return json_status, lat, lng, new_loc


while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículo disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("auto, bicicleta, a pie")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    entrada = input("Ingresa un perfil de vehículo de la lista (s/salir para terminar): ").strip().lower()
    if quiere_salir(entrada):
        break
    vehicle = PERFILES.get(entrada)
    if vehicle is None:
        vehicle = "car"
        print("Perfil no válido, se usará 'auto' por defecto.")

    loc1 = pedir("Ubicación de origen: ")
    if loc1 is None:
        break
    orig = geocoding(loc1, key)

    loc2 = pedir("Destino: ")
    if loc2 is None:
        break
    dest = geocoding(loc2, key)

    print("=================================================")
    if orig[0] == 200 and dest[0] == 200 and orig[1] != "null" and dest[1] != "null":
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode(
            {"key": key, "vehicle": vehicle, "locale": "es"}
        ) + op + dp
        paths_response = requests.get(paths_url)
        paths_status = paths_response.status_code
        paths_data = paths_response.json()

        print("Estado de la API de rutas: " + str(paths_status)
              + "\nURL de la API de rutas:\n" + paths_url)
        print("=================================================")
        print("Indicaciones desde " + orig[3] + " hasta " + dest[3]
              + " en " + (entrada if entrada in PERFILES else "auto"))
        print("=================================================")
        if paths_status == 200:
            ruta = paths_data["paths"][0]
            km = ruta["distance"] / 1000
            miles = km / 1.61
            ms = ruta["time"]
            sec = int(ms / 1000 % 60)
            minu = int(ms / 1000 / 60 % 60)
            hr = int(ms / 1000 / 60 / 60)
            print("Distancia recorrida: {0:.2f} millas / {1:.2f} km".format(miles, km))
            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, minu, sec))
            print("=================================================")
            print("Narrativa del viaje:")
            for paso in ruta["instructions"]:
                d_km = paso["distance"] / 1000
                d_mi = d_km / 1.61
                print("{0} ( {1:.2f} km / {2:.2f} millas )".format(paso["text"], d_km, d_mi))
            print("=================================================")
        else:
            print("Mensaje de error: " + str(paths_data.get("message", "")))
            print("*************************************************")
    else:
        print("No se pudo calcular la ruta: revisa el origen y el destino.")