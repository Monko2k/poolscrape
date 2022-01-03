from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
import re
def getPool(URL):
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get(URL)
    id = 'test'
    _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, 'mat-row')))
    pool = {}
    pool['name'] = driver.find_element(By.TAG_NAME, 'mat-card-title').text
    pool['maps'] = {}
    pool['maps']['NM'] = []
    pool['maps']['HD'] = []
    pool['maps']['HR'] = []
    pool['maps']['DT'] = []
    pool['maps']['FM'] = []
    pool['maps']['TB'] = []
    rows = driver.find_elements(By.TAG_NAME, 'mat-row')
    for row in rows:
        mod = row.find_element(By.XPATH, 'mat-cell[1]').text
        row.click()
        driver.switch_to.window(driver.window_handles[-1])
        beatmap = driver.current_url
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        reg = re.search('\d+$', beatmap)
        pool['maps'][mod[:2]].append({
            'id': reg.group(0)
        })

    driver.close()
    with open('./pools/' + id + '.json', 'w') as output:
        json.dump(pool, output)

def main():
    getPool('https://oma.hwc.hr/pools/906bcbf4-6675-3d23-b888-eff53539a19b')

if __name__ == "__main__":
    main()