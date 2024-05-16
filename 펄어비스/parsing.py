import xml.etree.ElementTree as ET

def find_and_print_next_fourth_line(file_path, search_string1,search_string2,search_string3):
    with open(file_path, 'r', encoding='EUC-KR') as file:
        found1 = False
        found2 = False
        found3 = False
        line_counter1 = 0
        line_counter2 = 0
        line_counter3 = 0
        
        for line in file:
            #print(line)
            if(found1 is True):
                if (line_counter1==3 or line_counter1==7 or line_counter1==11) and line_counter1 !=0:
                    print(line_counter1)
                    print(f"The 1th line after finding '{search_string1}': {line.strip()}")
                    
                    if(line_counter1>=9):
                        found1 = False
                        
                line_counter1 += 1
                continue
            elif(found2 is True):
                if (line_counter2==3 or line_counter2==7 or line_counter2==11) and line_counter2 !=0:
                    print(line_counter2)
                    print(f"The 1th line after finding '{search_string2}': {line.strip()}")
                    
                    if(line_counter2>=9):
                        found2 = False
                        
                line_counter2 += 1
                continue
            elif(found3 is True):
                if (line_counter3==3 or line_counter3==7 or line_counter3==11) and line_counter3 !=0:
                    print(line_counter3)
                    print(f"The 1th line after finding '{search_string3}': {line.strip()}")
                    
                    if(line_counter3>=9):
                        found3 = False
                        
                line_counter3 += 1
                continue
            

            elif (search_string1 in line):
                
                found1=True
            elif (search_string2 in line):
                found2=True
            elif (search_string3 in line):
                found3=True

            
                
        
            
           

# Example usage
xml_file = '펄어비스/20220322001101.xml'
#xml_file = '펄어비스/dummy.xml'
search_string1 = "영업활동으로 인한 현금흐름"
search_string2 = "투자활동으로 인한 현금흐름"
search_string3 = "재무활동으로 인한 현금흐름"
find_and_print_next_fourth_line(xml_file, search_string1,search_string2,search_string3)