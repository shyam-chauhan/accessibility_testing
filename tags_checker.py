import requests
from bs4 import BeautifulSoup
import re

def get_color_from_style(style):
    match = re.search(r'color:\s*(#[0-9a-fA-F]{3,6}|rgb\([^)]+\))', style)
    if match:
        return match.group(1)
    return None

def analyze_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    print(f"\n📄 Analyzing: {url}")

    # Tag presence checks
    tags = ['h1', 'p', 'img', 'nav', 'a', 'section', 'footer']
    missing_alt_images = []
    h1_elements = []

    for tag in tags:
        elements = soup.find_all(tag)
        print(f"\n🔍 Found {len(elements)} <{tag}> tag(s):")
        if tag == 'img':
            missing_alt_images = [img for img in elements if not img.get('alt')]
            print(f"   ❌ {len(missing_alt_images)} <img> tags missing alt attributes")
        elif tag == 'h1':
            h1_elements = elements
            if len(elements) > 1:
                print("   ⚠️ Multiple <h1> tags found. Only one is recommended.")
            for h in elements:
                print(f"   ✔️ H1 content: {h.get_text(strip=True)}")
        else:
            for e in elements[:3]:
                print(f"   ✔️ Sample: {str(e)[:80]}...")

    # Form label checks (inputs, textareas, selects)
    inputs = soup.find_all(['input', 'textarea', 'select'])
    labels = soup.find_all('label')
    label_for_ids = {label.get('for') for label in labels if label.get('for')}
    inputs_with_ids = [(inp.name, inp.get('id'), inp) for inp in inputs if inp.get('id')]
    missing_labels = [(tag, id_, inp) for tag, id_, inp in inputs_with_ids if id_ not in label_for_ids]

    print(f"\n📝 Form Label Check:")
    if missing_labels:
        print(f"   ❌ {len(missing_labels)} element(s) missing associated <label for='...'>:")
        for tag, id_, inp in missing_labels:
            input_type = inp.get('type', 'text')
            placeholder = inp.get('placeholder', '')
            snippet = inp.prettify()[:120].replace('\n', '')
            print(f"   ➤ Tag: <{tag}> | ID: {id_} | Type: {input_type} | Placeholder: '{placeholder}'")
            print(f"      HTML Snippet: {snippet}")
    else:
        print("   ✅ All form elements with IDs have matching labels.")



    # Missing elements list
    if missing_alt_images:
        print("\n🔎 Missing <alt> in <img> tags:")
        for img in missing_alt_images:
            src = img.get('src', 'N/A')
            snippet = img.prettify()[:120].replace('\n', '')
            print(f"   ➤ src: {src} | HTML Snippet: {snippet}")


    print("\n✅ Check Complete.")

# Example usage
analyze_website("https://www.gujaratuniversity.ac.in/")
