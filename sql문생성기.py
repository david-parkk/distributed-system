import xml.etree.ElementTree as ET

# Function to sanitize corp_name by removing special characters
def sanitize_corp_name(corp_name):
    return corp_name.replace("'", "")

# Load and parse the XML file
xml_file = 'CORPCODE.xml'
tree = ET.parse(xml_file)
root = tree.getroot()

# Open a file to write SQL insert statements
with open('output.sql', 'w', encoding='utf-8') as sql_file:
    # Loop through each 'list' element in the XML
    for item in root.findall('list'):
        # Extract the relevant data
        corp_code = item.find('corp_code').text
        corp_name = item.find('corp_name').text
        stock_code = item.find('stock_code').text if item.find('stock_code').text else 'NULL'
        modify_date = item.find('modify_date').text

        # Sanitize the corp_name by removing special characters
        sanitized_corp_name = sanitize_corp_name(corp_name)
        
        # Create an SQL insert statement
        sql_insert = (
            "INSERT INTO corpcode (corp_code, corp_name, stock_code, modify_date) "
            f"VALUES ('{corp_code}', '{sanitized_corp_name}', '{stock_code}', '{modify_date}');\n"
        )
        
        # Write the insert statement to the file
        sql_file.write(sql_insert)

print("SQL file has been created.")