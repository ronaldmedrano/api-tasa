import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def obtener_tasas_bcv():
    url = "https://www.bcv.org.ve/"
    # El 'headers' es clave para que el BCV te deje entrar
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscamos los valores (Asegúrate de que los IDs coincidan con la web actual del BCV)
    dolar_str = soup.find('div', id='dolar').find('strong').text.strip().replace(',', '.')
    euro_str = soup.find('div', id='euro').find('strong').text.strip().replace(',', '.')
    
    return [
        {"moneda": "USD", "tasa": float(dolar_str), "fecha": datetime.now().strftime('%Y-%m-%d')},
        {"moneda": "EUR", "tasa": float(euro_str), "fecha": datetime.now().strftime('%Y-%m-%d')}
    ]

def guardar_tasas(tasas):
    for tasa in tasas:
        año = datetime.now().strftime('%Y')
        carpeta = f"tasa/{tasa['moneda']}/{año}"
        os.makedirs(carpeta, exist_ok=True)
        
        archivo = f"{carpeta}/{tasa['fecha']}.json"
        
        data = [{
            "fuente": "BCV",
            "moneda": tasa['moneda'],
            "tasa": tasa['tasa'],
            "fecha": tasa['fecha']
        }]
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    tasas = obtener_tasas_bcv()
    guardar_tasas(tasas)