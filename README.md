# Evaluacion2 - Rutas con Graphhopper en español

Aplicación de consola en Python que consulta la API de Graphhopper (geocodificación y rutas) y entrega la distancia, la duración y la narrativa del viaje en español. Fue desarrollada para la Evaluación Parcial N° 2 de CUY6142.

## Funcionalidades

- Interacción con el usuario completamente en español.
- Distancias y valores numéricos con un máximo de dos decimales.
- Narrativa paso a paso del viaje en español.
- Perfiles de transporte: auto, bicicleta y a pie.
- Para salir, ingresa `s` o `salir` en cualquier pregunta.

## Requisitos

- Python 3
- Librería `requests`: `pip3 install requests`
- Una clave de API de Graphhopper (https://www.graphhopper.com/)

## Cómo ejecutarlo

1. Clona el repositorio y entra a la carpeta:
   ```
   git clone https://github.com/TU_USUARIO/Evaluacion2.git
   cd Evaluacion2
   ```
2. Abre `graphhopper_es.py` y reemplaza `TU_API_KEY` por tu clave.
3. Ejecuta:
   ```
   python3 graphhopper_es.py
   ```
4. Ingresa el perfil de vehículo, la ubicación de origen y el destino (por ejemplo: `Santiago, Chile`).
5. Escribe `s` o `salir` para terminar.