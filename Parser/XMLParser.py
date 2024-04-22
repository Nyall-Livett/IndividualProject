import xml.etree.ElementTree as ET

"""
This class handles the parsing of the XML to extract data about mutations
"""

class XMLParser:

    def __init__(self, xml_data: str):
        self.parsed_xml = ET.fromstring(xml_data)

    def find_alive_mutations(self, class_name):
        """
        Using XPath, find all elements named mutation that have the sourceFile child called the
        class name.
        Return all instances found as list of tuples with mutation status and the mutation applied.
        """

        mutations_info = []
        path = f".//mutation[sourceFile='{class_name}']"
        
        for mutation in self.parsed_xml.findall(path):
            status = mutation.get('status')
            description = mutation.find('description').text
            mutations_info.append((status, description))
        
        return mutations_info
