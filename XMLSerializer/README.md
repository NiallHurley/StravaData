# XML serializer
This is a module that can be used to create and read from configuration XML files. The tags of the .xml files are attributes/properties of the Config class and, on parsing the XML file are read into their respective places. The Config class can then be passed to other functions who need access to the configuration data - the idea being that the file containing the true XML configuration will not be distributed/version-controlled. 

# Examples
## create a new configuration file
```python 
#import the module
import XMLSerializer

# create an instance of the Config class (populated with default values for the attributes/variables
configData = XMLSerializer.Config()

# display the information in 'configData'  
print configData.ToPrintable()

# Save this data to an XML file
configData.SaveToFile('blankSettingsFileWithDefaultValues.xml')

# edit the variables between the tags in the blank settings file if necessary... and save. 
```

## load configuration from file
```python 
#import the module
import XMLSerializer

# create instance of class:Config
c = XMLSerializer.Config()

# Read the Settings to the Config class
c.ReadFromFile('blankSettingsFileWithDefaultValues.xml')

# display the loaded data
print c.ToPrintable()
```