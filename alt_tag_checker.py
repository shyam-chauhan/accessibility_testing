import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_images_missing_alt(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad responses
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    print(f"Total <img> tags found: {len(img_tags)}\n")

    missing_alt = []
    for img in img_tags:
        if not img.has_attr('alt') or img['alt'].strip() == '':
            # Make the src absolute (in case it's relative)
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
website_url = 'https://www.explmpl.org/'  # Replace with your target URL
find_images_missing_alt(website_url)
