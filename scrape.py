from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import re
def getPool(URL):
    options = Options()
    options.add_argument('--host-resolver-rules=MAP osu.ppy.sh 127.0.0.1:9876')
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=options) 
    driver.get(URL)
    driver.execute_cdp_cmd('Network.setBlockedURLs', {"urls": ["osu.ppy.sh"]})
    driver.execute_cdp_cmd('Network.enable', {})
    reg = re.search('[^/]+$', URL)
    id = reg.group(0)
    print(f"Processing {id}")
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
    mods = []
    rows = driver.find_elements(By.TAG_NAME, 'mat-row')
    for row in rows:
        mods.append(row.find_element(By.XPATH, 'mat-cell[1]').text)
        row.click()
    for ind, mod in enumerate(mods):
        driver.switch_to.window(driver.window_handles[-1])
        beatmap = driver.current_url
        reg = re.search('\d+$', beatmap)
        pool['maps'][mod[:2]].append({
            'id': reg.group(0)
        })
        driver.close()
    driver.quit()
    with open('./pools/' + id + '.json', 'w+') as output:
        json.dump(pool, output)

def main():
    with open('./pools.txt', 'r') as input:
        lines = input.readlines()
    for line in lines:
        getPool(line.strip())

if __name__ == "__main__":
    main()