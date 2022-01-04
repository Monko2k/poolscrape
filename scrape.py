from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import re
def getPool(URL, driver):
    driver.get(URL)
    reg = re.search('[^/]+$', URL)
    id = reg.group(0)
    print(f"Processing {id}")
    _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, 'mat-row')))
    pool = {}
    modgroups = {}
    pool['name'] = driver.find_element(By.TAG_NAME, 'mat-card-title').text
    pool['modgroups'] = []
    modgroups['NM'] = []
    modgroups['HD'] = []
    modgroups['HR'] = []
    modgroups['DT'] = []
    modgroups['FM'] = []
    modgroups['TB'] = []
    mods = []
    rows = driver.find_elements(By.TAG_NAME, 'mat-row')
    for row in rows:
        mods.append(row.find_element(By.XPATH, 'mat-cell[1]').text)
        row.click()
    for mod in mods:
        driver.switch_to.window(driver.window_handles[-1])
        beatmap = driver.current_url
        reg = re.search('\d+$', beatmap)
        modgroups[mod[:2]].append(reg.group(0))
        driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    for group in modgroups:
        pool['modgroups'].append({
            "mod": group,
            "maps": modgroups[group]
        })
    with open('./pools/' + id + '.json', 'w+') as output:
        json.dump(pool, output)

def main():
    with open('./pools.txt', 'r') as input:
        lines = input.readlines()
    options = Options()
    options.add_argument('--host-resolver-rules=MAP osu.ppy.sh 127.0.0.1:9876')
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=options) 
    for line in lines:
        getPool(line.strip(), driver)

if __name__ == "__main__":
    main()