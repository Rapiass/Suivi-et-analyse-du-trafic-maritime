import requests
from tqdm import tqdm
import zipfile
from datetime import datetime
import os

# Fonction pour télécharger un fichier ZIP à partir d'une URL donnée
def DownloadZip(date):
    try:
        # Vérification de la date
        date = VerificationDate(date)

        # Extraire l'année de la date
        year = date.split('_')[0]
        
        # Construction de l'URL du zip
        zip_url = f'https://coast.noaa.gov/htdata/CMSP/AISDataHandler/{year}/AIS_{date}.zip'

        # Chemins pour enregistrer les fichiers
        files_zip = f"{os.getcwd()}/ETL/TEMP/DATA"
        files = f"{os.getcwd()}/ETL/TEMP/DATA"

        # Créer le répertoire de téléchargement s'il n'existe pas
        if not os.path.exists(files_zip):
            os.makedirs(files_zip)

        # On récupère le nom du fichier ZIP à partir de l'URL
        filename = zip_url.split('/')[-1]
        file_path = os.path.join(files_zip, filename)

        # Télécharger le fichier ZIP avec une barre de progression
        with requests.get(zip_url, stream=True) as zip_response:
            zip_response.raise_for_status()  # Vérifie si la requête a réussi
            total_size = int(zip_response.headers.get('content-length', 0))
            
            with open(file_path, 'wb') as file, tqdm(
                desc=filename,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in zip_response.iter_content(chunk_size=1024):
                    file.write(data)
                    bar.update(len(data))

        print(f"Fichier téléchargé : {file_path}")
        unzip_file(file_path, files)

        # on retourne le chemin et le nom du fichier
        file_path_csv = file_path.replace(".zip", ".csv")
        return file_path_csv

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement : {e}")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {e}")

#--------------------------------------------------------------------------------------------------#

def VerificationDate(date):
    """
    Vérifie si une date est valide :
    - Elle doit être après le 1er janvier 2015.
    - Elle doit être comprise dans une période de 2 ans avant la date actuelle.

    Si la date est valide, alors elle renvoie la date. Sinon, elle envoie la date corrigée
    """

    # Obtenir la date actuelle puis soustraire 2 ans
    current_date = datetime.now()
    current_date_modif = current_date.replace(year=current_date.year - 2)
    
    # Définir la première date de référence
    firstdate = datetime.strptime("2015/01/01", "%Y/%m/%d")
    
    # Conversion de la date passée en paramètre AAAA_MM_JJ vers AAAA/MM/JJ
    date = date.replace('_', '/')
    dateObj = datetime.strptime(date, "%Y/%m/%d")
    
    # Vérification des conditions
    if current_date_modif < dateObj :
        date = f"{current_date_modif.year}_{current_date_modif.month:02}_{current_date_modif.day:02}"
        print(f"Erreur de date : date entrée est supérieure à la date actuelle !")
        print(f"Remplace la date choisi par la date actuelle ! {date}")
        return date
    elif dateObj < firstdate:
        date = f"{firstdate.year}_{firstdate.month:02}_{firstdate.day:02}"
        print(f"Erreur de date : la date entrée ne correspond pas à celle présente dans la base de donnée !")
        print(f"Remplace la date choisi par la date la plus ancienne dans la base de données ! {date}")
        return date
    else:
        return f"{dateObj.year}_{dateObj.month:02}_{dateObj.day:02}"

#--------------------------------------------------------------------------------------------------#

# Fonction pour dézipper le fichier et l'enregistrer dans un répertoire
def unzip_file(zip_path, file_path):
    try:
        # Créer le répertoire de sortie s'il n'existe pas
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # Dézipper le fichier
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            if not zip_ref.namelist():
                print("Le fichier ZIP est vide.")
                return
            print(f"Décompression de {zip_path} dans {file_path}")
            zip_ref.extractall(file_path)
        print(f"Fichier {zip_path} décompressé avec succès dans {file_path}")

        # Suppression du zip après extraction
        if os.path.exists(zip_path):
            os.remove(zip_path)  

    except zipfile.BadZipFile:
        print(f"Erreur : le fichier {zip_path} est corrompu ou n'est pas un fichier ZIP valide.")
    except Exception as e:
        print(f"Une erreur inattendue lors de la décompression : {e}")

# Exemple d'utilidation
#date = "2023_11_04" 
#DownloadZip(date)


