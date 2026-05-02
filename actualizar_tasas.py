import requests
from bs4 import BeautifulSoup
import json
import os
import sys
import urllib3
from datetime import datetime, timezone, timedelta

# Silenciar advertencias de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def obtener_datos_bcv():
    url = "https://www.bcv.org.ve/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers, verify=False, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 1. Extraer Fecha (usando el atributo content del span)
    fecha_tag = soup.find('span', class_='date-display-single')
    fecha_iso = fecha_tag.get('content')
    fecha_formateada = fecha_iso.split('T')[0] 
    año_carpeta = fecha_formateada.split('-')[0]
    
    # 2. Extraer Tasas (Usando los IDs que proporcionaste)
    # Buscamos el div por ID y luego el fuerte <strong> dentro
    dolar_str = soup.find('div', id='dolar').find('strong').text.strip().replace(',', '.')
    euro_str = soup.find('div', id='euro').find('strong').text.strip().replace(',', '.')
    
    print(f"Fecha extraída: {fecha_formateada}")
    print(f"USD: {dolar_str} | EUR: {euro_str}")
    
    return [
        {"moneda": "USD", "tasa": float(dolar_str), "fecha": fecha_formateada, "año": año_carpeta},
        {"moneda": "EUR", "tasa": float(euro_str), "fecha": fecha_formateada, "año": año_carpeta}
    ]

def guardar_tasas(lista_tasas):
    for item in lista_tasas:
        carpeta = f"tasa/{item['moneda']}/{item['año']}"
        os.makedirs(carpeta, exist_ok=True)
        
        archivo = f"{carpeta}/{item['fecha']}.json"
        
        data = [{
            "fuente": "oficial",
            "moneda": item['moneda'],
            "tasa": item['tasa'],
            "fecha": item['fecha']
        }]
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Archivo generado: {archivo}")

def proximo_dia_habil(fecha):
    """Retorna el próximo día hábil: el viernes devuelve el lunes siguiente."""
    # weekday(): 0=lunes ... 4=viernes
    if fecha.weekday() == 4:  # viernes
        return fecha + timedelta(days=3)
    return fecha + timedelta(days=1)

def ya_existe_tasa_hoy():
    """Verifica si ya se guardó la tasa del próximo día hábil.
    El BCV publica cada día la tasa del día siguiente, y el viernes
    publica la del lunes próximo.
    """
    vet = timezone(timedelta(hours=-4))
    hoy = datetime.now(vet).date()
    proximo = proximo_dia_habil(hoy)
    fecha_str = proximo.strftime("%Y-%m-%d")
    año = proximo.strftime("%Y")

    monedas = ["USD", "EUR"]
    for moneda in monedas:
        archivo = f"tasa/{moneda}/{año}/{fecha_str}.json"
        if not os.path.exists(archivo):
            return False
    print(f"Las tasas del {fecha_str} ya fueron registradas. No se realizará una nueva consulta.")
    return True

if __name__ == "__main__":
    if ya_existe_tasa_hoy():
        sys.exit(0)
    try:
        datos = obtener_datos_bcv()
        guardar_tasas(datos)
        print("Proceso finalizado correctamente.")
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        sys.exit(1)