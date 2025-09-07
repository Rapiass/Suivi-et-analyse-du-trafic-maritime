from .object_to_sql import ObjectToSQL
from Variables import ORDER_INSERT
import os


class Parser :
    """
    Cette classe à pour objectif de creer tout les scripts d'insertion sql via les objets
    """

    def __init__(self):
        self.orderInsert = list(ORDER_INSERT)
        self.parserType = ObjectToSQL

    def __createSql__(self,object)->str:
        """
        Create an sql line with parser class
        """
        return self.parserType(object,'INSERT')
    
    def __createSQLForObject__(self,arrObject)->str:
        """
        Create SQL script for one list of object
        """
        final_script = ""
        for id,obj in arrObject.items() : final_script += self.__createSql__(obj)
        return final_script
    
    def CreateSQLFileForObjects(self,arrObject:list,objName:str)->None:
        """
        Vérifie que tout les objets soit bien inséré dans le bon ordre
        Créer le fichier sql
        """
        if(objName != self.orderInsert[0]) : raise Exception("Object must be created in the good order")
        else : self.orderInsert.pop(0)

        with open(f'{os.getcwd()}/ETL/TEMP/SQL_SCRIPT/{str(len(ORDER_INSERT)-len(self.orderInsert)).zfill(2)}_{objName}.sql','w') as file :
            file.write(self.__createSQLForObject__(arrObject=arrObject))