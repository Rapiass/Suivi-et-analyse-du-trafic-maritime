from datetime import datetime
from dateutil.relativedelta import relativedelta
import csv
import os
from tqdm import tqdm
from CSV.CsvDownloader import DownloadZip
from MAPPING.mapper import Mapper
from PARSING.parser import Parser
from CONSOLE.ComandLineExecutor import CommandLineExecutor
from Variables import ORDER_INSERT

def main():
    
    console_exec = CommandLineExecutor()

    print("BACKUP")
    print(console_exec.ExecuteResult(f"./ETL/CONSOLE/BASH_FILE/backup_user.sh"))
    print("NO PURGING")
    #print(console_exec.ExecuteResult(f"./CONSOLE/BASH_FILE/purging_db.sh"))

    # téléchargement des données (on récupère au passage le nom et le chemin du fichier .csv)
    #two_years_ago = (datetime.now() - relativedelta(years=2)).strftime("%Y_%m_%d")
    #chemin = DownloadZip(two_years_ago)
    chemin = os.getcwd() + "/ETL/TEMP/DATA/AIS_2023_01_01_Smaller.csv"

    ####### MAPPING #######

    # création du mapper
    mapper = Mapper()

    #Lecture des 3 fichiers statiques
    #Country
    with open(os.getcwd()+'/ETL/TEMP/STATIC/Country.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mapper.ReadRow(row)
    
    #NavigationStatus
    with open(os.getcwd()+'/ETL/TEMP/STATIC/NavigationStatus.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mapper.ReadRow(row)
    
    #VesselType
    with open(os.getcwd()+'/ETL/TEMP/STATIC/VesselType.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mapper.ReadRow(row)

    #VesselType
    with open(os.getcwd()+'/ETL/TEMP/STATIC/Role.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mapper.ReadRow(row)

    #Static backup data 
    with open(os.getcwd()+'/ETL/TEMP/CSV_BACKUP/Company.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mapper.ReadRow(row)

    with open(os.getcwd()+'/ETL/TEMP/STATIC/User.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mapper.ReadRow(row)

    with open(os.getcwd()+'/ETL/TEMP/STATIC/UserHasRole.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mapper.ReadRow(row)

    with open(os.getcwd()+'/ETL/TEMP/CSV_BACKUP/UserHasVessel.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mapper.ReadRow(row)

    # lecture du fichier
    with open(chemin, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in tqdm(reader,"Mapping CSV"):
            mapper.ReadRow(row)
    
    # récupération des données mappées
    data = mapper.GetAllObject()

    print("DATA ACQUIRED")
    print("CREATING SCRIPT")
    #######################

    parser = Parser()
    #Boucle sur toutes les tables 
    for table_name in ORDER_INSERT:
        #J'appelle mon parser sur chaque objet 
        parser.CreateSQLFileForObjects(data[table_name],table_name)

    print("SCRIPT CREATED")
    print("MOVING TO SCRIPT EXECUTION")


    #print(console_exec.ExecuteResult(f"./CONSOLE/BASH_FILE/create_db.sh -f {os.getcwd()}/DB/DB.SQL"))

    list_sql = sorted(os.listdir(os.getcwd()+"/ETL/TEMP/SQL_SCRIPT"))

    for files in list_sql:
        print(files)
        if(files.endswith(".sql")):
            print(console_exec.ExecuteResult(f"./ETL/CONSOLE/BASH_FILE/sql_file.sh -f {os.getcwd()}/ETL/TEMP/SQL_SCRIPT/{ files}"))
    

if __name__ == "__main__":
    main()


    

