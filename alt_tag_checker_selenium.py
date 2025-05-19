from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def find_images_missing_alt(url):
    # Setup headless browser options
    options = Options()
    options.headless = True
    options.add_argument("--disable-blink-features=AutomationControlled")


    # Start the browser
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)  # Let the page load (increase if needed)

    # Get rendered page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    img_tags = soup.find_all('img')
    print(f"Total <img> tags found: {len(img_tags)}\n")

    missing_alt = []
    for img in img_tags:
        if not img.has_attr('alt') or img['alt'].strip() == '':
            src = img.get('src', '')
            abs_src = urljoin(url, src)
            missing_alt.append(abs_src)

    if missing_alt:
        print(f"Images missing 'alt' attributes ({len(missing_alt)}):")
        for i, img_src in enumerate(missing_alt, 1):
            print(f"{i}. {img_src}") 
    else:
        print("✅ All images have alt attributes.")

# Example usage
website_url = 'https://example.com/'
find_images_missing_alt(website_url)
