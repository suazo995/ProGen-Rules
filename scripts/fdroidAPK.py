import random
import urllib
import bs4
import os
import requests
import wget
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


root_url = 'https://f-droid.org'
ids = ["system", "connectivity", "development", "games", "graphics", "internet", "money", "multimedia", "navigation", "phone-sms", "reading", "science-education", "security", "sports-health", "theming", "time", "writing"]
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36' }

os.chdir(f'/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/')

random.shuffle(ids)
no_errors = 0
errores = []
for i in ids:
    for x in range(0, 20):
        if x == 0:
            page = requests.get(f'{root_url}/en/categories/{i}', headers=headers)
        else:
            page = requests.get(f'{root_url}/en/categories/{i}/{x}', headers=headers)
        print(page)
        if page.status_code == 404:
            print(f'no se encontró la pagina {root_url}en/categories/{i}/{x}')
        else:
            soup = bs4.BeautifulSoup(page.text, 'html.parser')
            a = soup.find_all('a', class_='package-header', href=True)
            print("********************************************************")
            print("********************************************************\n")
            print(f"Estamos descargando las aplicaciones de la página {i}\n")
            print("********************************************************")
            print("********************************************************\n")

            for d in a:
                result = None
                while result is None:
                    try:
                        app_url = f"{root_url}{d['href']}"
                        app_page = requests.get(app_url, headers=headers)
                        session = requests.Session()
                        retry = Retry(connect=3, backoff_factor=0.5)
                        app_page = requests.get(app_url, headers=headers)
                        adapter = HTTPAdapter(max_retries=retry)
                        session.mount('http://', adapter)
                        session.mount('https://', adapter)
                        app_page = session.get(app_url)
                        result = "Done"
                    except requests.exceptions.ConnectionError:
                        pass

                # print(app_page.status_code)
                soup = bs4.BeautifulSoup(app_page.text, 'html.parser')
                h3_app = soup.find_all('h3', class_='package-name')[0]
                name = h3_app.contents[0].strip().replace(" ", "")
                name_dir = ''.join(e for e in name if e.isalnum())
                parent_dir = os.getcwd()

                print(app_url)
                print("--------------------------------------------------------")
                if os.path.exists(f'/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps{os.sep}{name_dir}'):
                    if not os.path.exists(f'{parent_dir}{os.sep}{name_dir}{os.sep}apk'):
                        print(app_url)
                        print(app_page)
                        os.mkdir(name_dir + os.sep + 'apk')
                        os.chdir(f'{parent_dir}{os.sep}{name_dir}{os.sep}apk')
                        p_app = soup.find_all('p', class_='package-version-download')[0]
                        link_app = p_app.find('a').get('href')
                        print(link_app)
                        print("--------------------------------------------------------")
                        print("--------------------------------------------------------")

                        result = None
                        while result is None:
                            try:
                                wget.download(link_app)
                                result = "Done"
                            except urllib.error.URLError:
                                pass

                        tarName = link_app.split('/')[-1]
                        print(name_dir)
                        os.system(f'unzip {tarName} > /dev/null')
                        os.system('/Volumes/WanShiTong/Archive/UChile/Título/work/tools/dex2jar/2.0/bin/d2j-dex2jar classes.dex > /dev/null')
                        os.system('java -jar /Volumes/WanShiTong/Archive/UChile/Título/work/tools/jd-cli-1.2.0-dist/jd-cli.jar -od source classes-dex2jar.jar > /dev/null')

                        os.chdir(parent_dir)
print(no_errors, 'de 649 sin errores')
print(errores)