from urllib.request import urlopen
from bs4 import BeautifulSoup

response=urlopen("https://dart.fss.or.kr/dsac001/mainK.do?selectDate=2022.03.22&sort=&series=&mdayCnt=0")
soup=BeautifulSoup(response,"html.parse")

value=soup.find("table",{"class","tbList"})
print(value)