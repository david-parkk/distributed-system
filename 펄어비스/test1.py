from lxml import etree

def process_large_xml(file_path, tag_name, process_function):
    """
    Process a large XML file and apply a function to each element with a specific tag.

    :param file_path: Path to the XML file.
    :param tag_name: The tag name of the elements to process.
    :param process_function: A function that takes an element and processes it.
    """
    try:
        # Create an iterparse context for the specified tag
        context = etree.iterparse(file_path, events=('end',), tag=tag_name)
        
        for event, elem in context:
            process_function(elem)
            elem.clear()  #
    except etree.XMLSyntaxError as e:
        print(f"XML syntax error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_element_text(elem):
    """
    Process function to print the text of an element.

    :param elem: The XML element to process.
    """
    print(f"Element <{elem.tag}>: {elem.text.strip() if elem.text else 'No text'}")

# Example usage
xml_file = '펄어비스/20220322001101.xml'
tag_name = 'P'
process_large_xml(xml_file, tag_name, print_element_text)