"""
Definition of the configuration class and sub-classes. 
Config is the overall container, containing:
	Schemas are stored in attributes of SchemasConfig
	General parameters are stored in attributes of GeneralParamsConfig
	Database connection properties are stored as attributes of DatabaseConfig
"""
from XMLSerializer.XMLSerializer import XMLSerializer
class SchemasConfig(XMLSerializer):
    """
    Config class for database schemas 
    """
    def __init__(self):
        self.tableRead = 'table_dummy'
        self.tableWrite = 'table_dummy'

class GeneralParamsConfig(XMLSerializer):
    """
    Config class for general parameters
    """
    def __init__(self):
        self.urlStravaActivities   = "https://www.strava.com/api/v3/activities"
        self.csvFilename = 'strava_activities_full.csv'

class StravaAPIConfig(XMLSerializer):
    """
    Config class for general parameters
    """
    def __init__(self):
        self.clientID = 0
        self.clientSecret = "clientSecret_dummy"
    
    def ToPrintable(self,indentLevel=0):
        indent = '   '*indentLevel
        return '{}ClientID: {}\n'.format(indent,self.clientID)
        
class DatabaseConfig(XMLSerializer):
    """
    Config class for database connection parameters  - note the method:ToPrintable 
     which doesn't print the password.
    """
    def __init__(self):
        self.username = 'username_dummy'
        self.password = 'password_dummy'
        self.hostname = 'hostname_dummy'
        
    def ToPrintable(self,indentLevel=0):
        indent = '   '*indentLevel
        return '{}{}@{}\n'.format(indent,self.username,self.hostname)

class LoginConfig(XMLSerializer):
    """
    Config class for database connection parameters  - note the method:ToPrintable 
     which doesn't print the password.
    """
    def __init__(self):
        self.username = 'username_dummy'
        self.password = 'password_dummy'
        self.url = 'hostname_dummy'
        
    def ToPrintable(self,indentLevel=0):
        indent = '   '*indentLevel
        return '{}{}@{}\n'.format(indent,self.username,self.url)



class Config(XMLSerializer):
    """
    Config class which holds all the configuration info
    """
    def __init__(self):
        self.stravaAPIConfig = StravaAPIConfig()
        self.stravaLogin = LoginConfig()
        self.generalParams = GeneralParamsConfig()


