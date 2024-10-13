import requests

# Token de Graphhopper
token = "a62f7a1e-1046-4a92-862f-467476b3e2a1"

# Función para obtener las coordenadas de una ciudad usando la API de Graphhopper Geocoding
def obtener_coordenadas(ciudad):
    url = f"https://graphhopper.com/api/1/geocode?q={ciudad}&locale=es&key={token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['hits']:
            lat = data['hits'][0]['point']['lat']
            lon = data['hits'][0]['point']['lng']
            return lat, lon
        else:
            print(f"No se encontraron resultados para {ciudad}.")
            return None
    else:
        print(f"Error en la solicitud de geocodificación: {response.status_code}")
        return None

# Función para calcular distancia y mostrar narrativa
def calcular_ruta(origen_coords, destino_coords, transporte):
    # Construir URL con el tipo de transporte elegido
    url_ruta = f"https://graphhopper.com/api/1/route?point={origen_coords[0]},{origen_coords[1]}&point={destino_coords[0]},{destino_coords[1]}&vehicle={transporte}&locale=es&key={token}"
    response_ruta = requests.get(url_ruta)
    
    if response_ruta.status_code == 200:
        data = response_ruta.json()

        if 'paths' in data:
            distancia_km = data['paths'][0]['distance'] / 1000
            distancia_millas = distancia_km * 0.621371
            duracion = data['paths'][0]['time'] / 3600000
            narrativa = data['paths'][0]['instructions']

            print(f"\nDistancia: {distancia_km:.2f} km | {distancia_millas:.2f} millas")
            print(f"Duración del viaje: {duracion:.2f} horas\n")
            print("Narrativa del viaje:")
            for step in narrativa:
                print(step['text'])
        else:
            print("Error: No se encontraron rutas entre las ciudades proporcionadas.")
    else:
        print(f"Error en la solicitud de la ruta: {response_ruta.status_code}")

# Menú principal
def main():
    while True:
        print("\nIngrese 's' en cualquier momento para salir.")
        
        # Solicitar ciudades
        origen = input("Ingrese la ciudad de origen: ")
        if origen.lower() == 's':
            break
        destino = input("Ingrese la ciudad de destino: ")
        if destino.lower() == 's':
            break

        # Obtener coordenadas
        coords_origen = obtener_coordenadas(origen)
        coords_destino = obtener_coordenadas(destino)

        if coords_origen and coords_destino:
            # Elegir medio de transporte
            print("\nSeleccione el medio de transporte:")
            print("1. Auto")
            print("2. Bicicleta")
            print("3. A pie")
            
            transporte_opcion = input("Ingrese el número del medio de transporte: ")
            if transporte_opcion == '1':
                transporte = "car"
            elif transporte_opcion == '2':
                transporte = "bike"
            elif transporte_opcion == '3':
                transporte = "foot"
            else:
                print("Opción no válida, usando 'auto' por defecto.")
                transporte = "car"

            # Calcular la ruta
            calcular_ruta(coords_origen, coords_destino, transporte)
        else:
            print("No se pudieron obtener las coordenadas de una o ambas ciudades.")
        
# Ejecutar el script
if __name__ == "__main__":
    main()
