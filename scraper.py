import time 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def sikayetCek(url):
    global_delay = 0.5
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    page_number = 1
    sikayet_number = 1
    try:
        while True:
            url = f"{base_url}?page={page_number}"
            driver.get(url)
            time.sleep(5)
            print(f'Sayfa {page_number} yüklendi.')
            last_height = driver.execute_script("return document.body.scrollHeight")
            
            while True:
                time.sleep(3)

                complaints = driver.find_elements(By.XPATH, '//h2[@class="complaint-title"]/a')
                if not complaints:
                    print(f'Sayfa {page_number} şikayet bulunamadı, sonlandı.')
                    return

                for index,complaint in enumerate(complaints):
                    try:
                        text = complaint.text
                        print(f'Şikayet {sikayet_number}: {text}')
                        with open("sikayetler.txt", "a", encoding='utf-8') as sikayet_file:
                            sikayet_file.write(f'{text}\n')
                        time.sleep(global_delay)
                        sikayet_number += 1  
                    except Exception as e:
                        print(f'Yorum çekilirken hata oluştu: {str(e)}')

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)  
                new_height = driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    break  
                last_height = new_height

            page_number += 1

    except Exception as e:
        print('Hata: ' + str(e))
    finally:
        print('Program sonlandı')
        driver.quit()

base_url = input("Şikayet var linkini giriniz: ")
sikayetCek(base_url)
