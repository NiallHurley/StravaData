"""
Class for read/parse/write XML into inheriting class attributes

to create dummy XML file:
    from XMLSerializer import XMLSerializer
    from XMLSerializer import Config
    c = Config.Config()
    c.SaveToFile('testConfig.xml')

"""

import xml.dom.minidom as md
class XMLSerializer:
    def ReadFromXML(self,root):
        """
        Read/parse the XML structure into classes
            .ReadFromXML(xmlRootNode)
        """
        if root.childNodes:
            for node in root.childNodes:
                if node.nodeType == node.ELEMENT_NODE:    
                    numGrandChildren = len(node.childNodes)
                    if numGrandChildren==0:
                        if hasattr(self,node.tagName):
                            setattr(self, node.tagName, {})           
                    elif numGrandChildren==1:
                        if node.childNodes[0].nodeType == node.TEXT_NODE:
                            value = node.childNodes[0].nodeValue
                            name = node.childNodes[0].parentNode.nodeName
                            try: 
                                value = str(value)
                            except:
                                value = str(value)
                            if hasattr(self,name):
                                setattr(self, name , value)
                    else:
                        if self.__IsPropertySerializeable(node.tagName): 
                            getattr(self,node.tagName).ReadFromXML(node)
                            
    def ReadFromFile(self,fileName):
        """
        Supply an XML file for parsing
            .ReadFromFile(fileName)
        """
        import os.path
        os.path.isfile(fileName)
        dom = md.parse(fileName)
        root = dom.documentElement
        self.ReadFromXML(root)
    
    def SaveToXML(self,doc,root): 
         """
         Save current class to XML structure
             .SaveToXML(documentElement,rootNode)
         """
         for var in vars(self):
            name = var
            value = getattr(self,name)           
            if self.__IsPropertySerializeable(name):
                # Create Element
                tempChild = doc.createElement(name)
                tempChild = value.SaveToXML(doc,tempChild)
                root.appendChild(tempChild)                
            else:    
                # Write Text
                tempChild = doc.createElement(name)
                nodeText = doc.createTextNode('{}'.format(value))
                tempChild.appendChild(nodeText)                
                root.appendChild(tempChild)   
         return(root)                

    def SaveToFile(self,fileName):
         """
         Save current class to XML file
             .SaveToFile(fileName)
         """
         doc = md.Document()   
         root = doc.createElement(self.__class__.__name__)
         #root = dom.documentElement            
         #root = doc.documentElement
         root = self.SaveToXML(doc,root)  
         root.writexml( open(fileName, 'w'),
                       indent="  ",
                       addindent="  ",
                       newl='\n')
        
    def ToPrintable(self,indentLevel=0):
        """
        return a printable string of the XML struct
        """
        printableString = ''
        indent = '   '*indentLevel
        for var in vars(self):
            name = var
            value = getattr(self,name)
            if self.__IsPropertySerializeable(name):
                tmpString = '\n{}'.format(value.ToPrintable(indentLevel+1))
            else:
                tmpString = '{}\n'.format(value)                            
            printableString = '{}{}{}:\t{}'.format(
                printableString,indent,name,tmpString)           
        return(printableString)
    
    def __IsPropertySerializeable(self,name):
        if hasattr(self,name):
            return isinstance(getattr(self,name),XMLSerializer)
        else:
            return False
            