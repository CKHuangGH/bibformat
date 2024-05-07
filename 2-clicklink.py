import PyPDF2
import re
from selenium import webdriver
import time
import re

def extract_urls_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        urls = []

        # 遍歷每頁
        for page in reader.pages:
            text = page.extract_text()
            if text:
                # 使用正規表達式找到所有 URL，確保格式為https://reurl.cc/後接六位字母或數字
                urls.extend(re.findall(r'https://reurl\.cc/[A-Za-z0-9]{6}\b', text))

    return urls

def open_and_close_urls(urls):
    # Setup Selenium WebDriver
    driver = webdriver.Chrome()  # Adjust if you're using a different browser
    
    # Ensure the URL list can be handled in chunks of five
    for i in range(0, len(urls), 5):
        # Open up to five URLs at a time
        for url in urls[i:i+5]:
            driver.execute_script("window.open('{}');".format(url))
        
        # Wait 30 seconds for each group of five URLs
        time.sleep(30)
        
        # Close all tabs before opening the next group
        driver.quit()
        
        # Reinitialize the WebDriver for the next batch of URLs
        driver = webdriver.Chrome()  # Adjust if you're using a different browser
    
    # Final cleanup: close the browser after processing all URLs
    driver.quit()

# 使用示例
pdf_path = 'Doctoral_Thesis.pdf'
urls = extract_urls_from_pdf(pdf_path)
print(urls)
open_and_close_urls(urls)
