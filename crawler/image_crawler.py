from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import requests
import time
import argparse

def main(config):
    
    max_cnt = config.max_cnt
    
    # 검색할 Query
    keyword = config.query
    
    # google URL
    GOOGLE = 'https://www.google.com/'
    
    # browser 실행
    browser = webdriver.Chrome('./chromedriver')

    # 전체화면
    browser.maximize_window()

    # google로 이동
    browser.get(GOOGLE)


    # 검색창
    elem = browser.find_element(By.NAME, 'q')

    # keyword 입력
    elem.send_keys(keyword)
    elem.send_keys(Keys.RETURN)
    
    # 이미지 클릭
    elem = browser.find_element(By.LINK_TEXT, '이미지').click()
    
    # 스크롤 내리기
    SCROLL_PAUSE_SEC = config.pause
    SCROLL_COUNT = config.scroll_cnt
    last_height = browser.execute_script("return document.body.scrollHeight")
    for _ in range(SCROLL_COUNT):
        # 끝까지 스크롤 다운
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 대기
        time.sleep(SCROLL_PAUSE_SEC)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = browser.execute_script("return document.body.scrollHeight")

        # 이미지 더 가져오기 클릭 
        if new_height == last_height:
            try:
                elem = browser.find_element(By.CLASS_NAME, 'mye4qd')
            except:
                break
        last_height = new_height
    
    # img tag 다 가져오기
    imgs = browser.find_elements(By.TAG_NAME, 'img')
    # img url 다 가져오기
    img_urls = [img.get_attribute('src') for img in imgs]
    
    # 이미지 읽고 저장 
    idx = 1
    for img in img_urls:
        try:
            img_res = requests.get(img)

            if img_res.ok:
                fn = os.path.join(config.save_dir, f'{idx}.jpg')
                with open(fn, 'bw') as f:
                    f.write(img_res.content)

                print(f'({idx}th image saved in {fn})')

                idx += 1
                                
        except:
            continue
        
        if idx >= max_cnt:
            print('*** COMPLETED  ***')
            break
    
    # 브라우저 종료
    browser.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type = str, required = True)
    parser.add_argument('--max_cnt', type = int, default = 200)
    parser.add_argument('--save_dir', type = str, required = True)
    parser.add_argument('--pause', type = int, default = 2)
    parser.add_argument('--scroll_cnt', type = int, default = 10)
    config = parser.parse_args()
    
    main(config)