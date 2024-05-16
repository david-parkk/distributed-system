from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

url = 'https://dart.fss.or.kr/dsac001/mainK.do?selectDate=2022.03.22&sort=&series=&mdayCnt=0'

# Set up Chrome options
driver_options = webdriver.ChromeOptions()
driver_options.add_argument("headless")  # Run Chrome in headless mode

# Specify the path to the ChromeDriver executable
service = Service()

# Initialize the Chrome WebDriver with the service
driver = webdriver.Chrome(service=service, options=driver_options)


# Open the URL
driver.get(url)

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
print(soup)

# Quit the driver
driver.quit()
