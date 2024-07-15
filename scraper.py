import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def sikayetCek(base_url, filter_word):
    global_delay = 0.5
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
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

                for index, complaint in enumerate(complaints):
                    try:
                        text = complaint.text
                        if filter_word.lower() in text.lower():
                            filtered_text = re.sub(r'\b' + re.escape(filter_word) + r'\b', '', text, flags=re.IGNORECASE).strip()
                            filtered_text = preprocess_text(filtered_text)
                            print(f'Şikayet {sikayet_number}: {filtered_text}')
                            with open("sikayetler.txt", "a", encoding='utf-8') as sikayet_file:
                                sikayet_file.write(f'{filtered_text}\n')
                        else:
                            text = preprocess_text(text)
                            print(f'Şikayet {sikayet_number}: {text}')
                            with open("sikayetler.txt", "a", encoding='utf-8') as sikayet_file:
                                sikayet_file.write(f'{text}\n')
                        sikayet_number += 1
                        time.sleep(global_delay)
                    except Exception as e:
                        print(f'Şikayet yazılırken hata oluştu: {str(e)}')

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
filter_word = input("Filtrelemek istediğiniz kelimeyi giriniz: ")
sikayetCek(base_url, filter_word)
