import time 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def sikayetCek(url):
    global_delay = 0.5
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get(url)
        time.sleep(5)  
        print('Firmanın şikayet sayfasına gidildi')

        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            time.sleep(3)

            complaints = driver.find_elements(By.XPATH, '/html/body/div[1]/main/div/div/div[3]/div[1]/div[3]/article/h2/a')
            for complaint in complaints:
                try:
                    text = complaint.text
                    with open("yorumlar.txt", "a", encoding='utf-8') as yorum_file:
                        yorum_file.write(text + '\n')
                    time.sleep(global_delay)
                except Exception as e:
                    print(f'Yorum çekilirken hata oluştu: {str(e)}')

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break  
            last_height = new_height

    except Exception as e:
        print('Hata: ' + str(e))
    finally:
        print('Program sonlandı')
        driver.quit()

url = input("Şikayet var linkini giriniz: ")
sikayetCek(url)
