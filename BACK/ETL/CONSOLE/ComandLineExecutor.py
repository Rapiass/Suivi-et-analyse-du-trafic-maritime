import subprocess

class CommandLineExecutor :
    """
    This class aim to Execute command line 
    """
    
    def __init__(self):
        """
        Constructeur de la classe

        Returns
        -------
        None.

        """
        self._nbProcess = 0
        
    def ExecuteNoReturn(self,command:str)->bool:
        """
        Execute a command, without any return at all

        Parameters
        ----------
        command : str
            The command to execute.

        Returns
        -------
        bool
            If the command execute well.

        """
        
        resultat = subprocess.run(command, shell=True,capture_output=True,text=True)
        if(resultat.returncode == 0):
            return True
        else :
            return False
        
    
    def ExecuteWait(self,command:str)->bool:
        """
        Same as ExecuteNoReturn but we wait till the process is well finished

        Parameters
        ----------
        command : str
            The command to execute.

        Returns
        -------
        bool
            If the command execute well.

        """
        process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        process.wait()
        
        if(process.returncode == 0): 
            return True 
        else: 
            return False
        
    def ExecuteResult(self,command:str)->tuple:
        """
        Execute a Command line and return the result of it

        Parameters
        ----------
        command : str
            The command to execute.

        Returns
        -------
        tuple
            (result of the command,error code of the command).

        """
        process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout,stderr = process.communicate()
        
        return (stdout.decode(),stderr.decode())