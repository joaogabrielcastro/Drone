import csv
from ..models.coordenada import Coordenada

def carregar_coordenadas(caminho):
    """
    Carrega coordenadas do arquivo CSV
    Formato esperado: cep,longitude,latitude
    """
    coordenadas = []
    try:
        with open(caminho, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for linha in reader:
                # Ajustar conforme o formato real do arquivo
                coord = Coordenada(
                    cep=linha['cep'],
                    latitude=float(linha['latitude']),
                    longitude=float(linha['longitude'])
                )
                coordenadas.append(coord)
        
        print(f"✅ {len(coordenadas)} coordenadas carregadas de {caminho}")
        return coordenadas
    
    except FileNotFoundError:
        print(f"❌ Arquivo {caminho} não encontrado")
        return []
    except Exception as e:
        print(f"❌ Erro ao carregar coordenadas: {e}")
        return []

def salvar_csv(dados, caminho, cabecalho=None):
    """Salva dados em arquivo CSV"""
    try:
        with open(caminho, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if cabecalho:
                writer.writerow(cabecalho)
            writer.writerows(dados)
        print(f"✅ Arquivo salvo: {caminho}")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar CSV: {e}")
        return False