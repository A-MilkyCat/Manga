import requests
from bs4 import BeautifulSoup
import os
import time
def download_images(url, directory_name, cnt):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 下載圖片
    img_tags = soup.find_all('img')

    for img_tag in img_tags[:-1]:
        img_url = img_tag['src']
        img_name = str(cnt) + ".jpg"
        img_path = os.path.join(directory_name, img_name)

        img_response = requests.get(img_url)
        with open(img_path, 'wb') as img_file:
            img_file.write(img_response.content)

        print(f"下載 {img_name} 完成")
        cnt = cnt+1
    
    # 找到包含下一章節連結的 div
    next_chapter_div = soup.find('div', class_='next_chapter')

    # 如果找到了下一章節連結
    if next_chapter_div:
        # 找到 <a> 標籤
        next_chapter_a = next_chapter_div.find('a')

        # 獲取 href 屬性
        next_chapter_url = next_chapter_a['href']
        print(next_chapter_url)
        # 獲取下一章節的完整網址
        # next_chapter_url = url[:url.rfind('/') + 1] + next_chapter_url

        # 遞迴下一章節
        time.sleep(3)
        download_images(next_chapter_url, directory_name, cnt)

if __name__ == "__main__":
    # 初始網址
    print('輸入你的網址:')
    website = input()
    initial_url = website

    # 目錄名稱，用來保存下載的圖片
    directory_name = "downloaded_images"
    os.makedirs(directory_name, exist_ok=True)

    # 開始遞迴下載
    download_images(initial_url, directory_name, 1)
