from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time
import pandas as pd

path = '/path/to/your/chromedriver'

def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)
# driver = webdriver.Chrome(path)


options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(chrome_options=options, executable_path=path)
driver.maximize_window()
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
# driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=path)
# set_viewport_size(driver, 1920, 1080)

# url = "https://www.infojobs.net/jobsearch/search-results/list.xhtml"
url = 'https://www.infojobs.net/jobsearch/search-results/list.xhtml?provinceIds=&cityIds=&categoryIds=&workdayIds=&educationIds=&segmentId=&contractTypeIds=&page=1&sortBy=&onlyForeignCountry=false&countryIds=&sinceDate=ANY&subcategoryIds='
driver.get(url)
time.sleep(10)

timeout = 10
wait = WebDriverWait(driver, timeout)
childframe = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ij-ComponentList")))
page = driver.find_element_by_tag_name('html')
nums = 1
while nums < 7:
  page.send_keys(Keys.PAGE_DOWN)
  time.sleep(1)
  nums += 1
  if nums == 7:
    break
input()
# element = wait.until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/ul[1]/li[6]/button[1]")))
time.sleep(15)
element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[2]/div[1]/div[2]/div/div/div[3]/div[2]/ul/li[24]')))
# //*[@id="app"]/div/div/div[2]/div[1]/div[2]/div/div/div[3]/div[2]/ul/li[24]
table = driver.find_element_by_class_name('ij-ComponentList')
# offers = table.find_elements_by_tag_name('li')
offers = table.find_elements_by_class_name('ij-OfferCardContent-description')
print(len(offers))
total = []
for i in offers:
    header = i.find_element_by_tag_name('h2')
    title = header.find_element_by_tag_name('a').text # 1
    link = header.find_element_by_tag_name('a').get_attribute('href') # 11
    company = i.find_element_by_tag_name('h3')
    company_name = company.find_element_by_tag_name('a').text # 2
    location_jobboard = i.find_element_by_class_name('ij-OfferCardContent-description-list-item-truncate').text.strip() # 3
    posting_date = i.find_element_by_class_name('ij-FormatterSincedate ij-FormatterSincedate--success ij-FormatterSincedate--xs').text.strip() # 4

    bottom = i.find_elements_by_class_name('ij-OfferCardContent-description-list')[1].find_elements_by_tag_name('li')
    contract = bottom[0].text
    employment_type = contract # 8
    agreement = bottom[1].text
    full_description = agreement # 9
    salary = bottom[2].find_element_by_tag_name('span').text    # 6
    skills = None # 10
    sector_jobboard = None # 5
    new = ((title, company_name, location_jobboard, posting_date, sector_jobboard, salary, agency_or_direct, employment_type, full_description, skills, link))
    total.append(new)
button = driver.find_element_by_xpath("//span[@class='sui-MoleculePagination-nextButtonIcon']")
button.click()

df = pd.DataFrame(total, columns = ['Title', 'Company Name', 'Location', 'Date', 'Sector', 'Salary', 'Agency or Direct', 'Employment Type', 'Description', 'Skills', 'Link'])
#               ['1 Title', '2 Company Name', '3 Location', '4 Date', '5 Sector', '6 Salary', '7 Agency or Direct', '8 Employment Type', '9 Description', '10 Skills', '11 Link'])
df.to_excel('infojobsES.xlsx') 
driver.close()
# driver.close()
# num = 1
# while num != 0:
# input()