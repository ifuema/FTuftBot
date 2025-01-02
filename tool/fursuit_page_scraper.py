import random

import aiohttp
import asyncio
import os
from bs4 import BeautifulSoup

domain = ""
PHPSESSID = ""
autologinAuth = ""
start_page_id = 10000
end_page_id = 10000


async def download_image(image_url, headers, image_path, session):
    try:
        async with session.get(image_url, headers=headers, ssl=False) as img_response:
            if img_response.status != 200:
                print(f"下载图片失败: {image_url}，状态码：{img_response.status}")
            with open(image_path, 'wb') as img_file:
                img_file.write(await img_response.read())
            print(f"图片已保存: {image_path}")
    except Exception as e:
        print(f"下载图片时出错: {image_url}，错误信息：{e}")


async def fetch_page(page_id, session):
    url = f"https://{domain}/fursuit/{page_id}/view.html"
    headers = {
        "authority": domain,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "max-age=0",
        "cookie": f"PHPSESSID={PHPSESSID};autologinAuth={autologinAuth}",
        "dnt": "1",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    async with session.get(url, headers=headers, ssl=False) as response:
        if response.status != 200:
            print(f"请求失败，页面 {page_id} 状态码：{response.status}")
            return

        text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')

        # 创建本地文件夹用于保存图片
        page_folder = f'images/page/fursuit_page_{page_id}'
        if not os.path.exists(page_folder):
            os.makedirs(page_folder)

        # 提取图片链接并下载
        image_div = soup.find('div', class_='fursuitAuth-images')
        if image_div:
            image_links = [a['href'] for a in image_div.find_all('a', class_='fursuitAuth-image')]
            download_tasks = []
            for link in image_links:
                image_url = f"https://{domain}{link}"
                image_name = os.path.basename(link)
                image_path = os.path.join(page_folder, image_name)
                download_tasks.append(download_image(image_url, headers, image_path, session))
            await asyncio.gather(*download_tasks)

        # 提取并保存个人资料
        profile_div = soup.find('div', class_='fursuitAuth-profile')
        data = {}
        if profile_div:
            for col in profile_div.find_all('div', class_='fursuitAuth-profile-col'):
                title = col.find('div', class_='fursuitAuth-profile-title')
                content = col.find('div', class_='fursuitAuth-profile-content')
                if title and content:
                    title_text = title.text.strip()
                    content_text = content.text.strip()
                    if title_text and content_text:  # 跳过空项
                        data[title_text] = content_text

            # 保存资料信息到文本文件
            profile_file_path = os.path.join(page_folder, 'fursuit_profile.txt')
            with open(profile_file_path, 'w', encoding='utf-8') as file:
                for key, value in data.items():
                    file.write(f"{key}: {value}\n")
            print(f"资料信息已保存到 {profile_file_path}")


async def fetch_all_pages(start_id, end_id):
    async with aiohttp.ClientSession() as session:
        for page_id in range(start_id, end_id + 1):
            await asyncio.sleep(random.uniform(1, 3))
            await fetch_page(page_id, session)


if __name__ == "__main__":
    asyncio.run(fetch_all_pages(start_page_id, end_page_id))
