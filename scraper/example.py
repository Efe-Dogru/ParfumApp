import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import sys
import os
import random
import signal

# List of modern user agents
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.204 Safari/537.36'
]

BASE_URL = "https://www.douglas.be/nl/c/parfum/01"

PRODUCT_LISTING_MAIN_DIV_ID = "productlisting"
PRODUCT_LISTING_PRODUCT_GRID_CLASS = "product-grid cms-component cms-component__margin cms-component__margin--default"
PRODUCT_CLASS = "product-tile__details-container"

PRODUCT_DETAIL_PAGE_NOTES_ELEMENT_EXAMPLE = """
<div class="hbqjtcyY4DmGUU0ezjD6" data-testid="product-detail-info__classifications"><div class="iayHgKPIUZWrzT4fpACP"><span class="PHtNB5LNBAR0ej2bv6Bf">Art-Nr.</span><span>103896</span></div><div class="iayHgKPIUZWrzT4fpACP"><span class="PHtNB5LNBAR0ej2bv6Bf">Geurnoot</span><span>Oriëntaal, Houtachtig</span></div><div class="iayHgKPIUZWrzT4fpACP"><span class="PHtNB5LNBAR0ej2bv6Bf">Topnoot</span><span>Oranje, Bergamot</span></div><div class="iayHgKPIUZWrzT4fpACP"><span class="PHtNB5LNBAR0ej2bv6Bf">Hartnoot</span><span>Muskus, Jasmijn, Roos, Mimosa</span></div><div class="iayHgKPIUZWrzT4fpACP"><span class="PHtNB5LNBAR0ej2bv6Bf">Basisnoot</span><span>Vetiver, Vanille</span></div><div class="iayHgKPIUZWrzT4fpACP"><span class="PHtNB5LNBAR0ej2bv6Bf">Ik ben refillable</span><span>Nee</span></div><div class="iayHgKPIUZWrzT4fpACP"><span class="PHtNB5LNBAR0ej2bv6Bf">Ik ben een refill</span><span>Nee</span></div><div class="iayHgKPIUZWrzT4fpACP"><span class="PHtNB5LNBAR0ej2bv6Bf">Season</span><span>Winter</span></div><div class="iayHgKPIUZWrzT4fpACP"><span class="PHtNB5LNBAR0ej2bv6Bf">Product type</span><span>Spray</span></div><div class="iayHgKPIUZWrzT4fpACP"><span class="PHtNB5LNBAR0ej2bv6Bf">Toepassingsgebied</span><span>Lichaam</span></div><div class="iayHgKPIUZWrzT4fpACP"><span class="PHtNB5LNBAR0ej2bv6Bf">Verantwoordelijkheid</span><span>Veganistisch</span></div><div class="iayHgKPIUZWrzT4fpACP"><span class="PHtNB5LNBAR0ej2bv6Bf">Toevoegingen</span><span>Vrij Van Parabenen, Ftalaat-Vrij, Sulfaat Vrij, Ammoniak Vrij, Siliconen Vrij, Paraffine-Vrij, Palmolievrij, Zonder Olieachtige Ingrediënten, Comedogeen-Vrij, Vrij Van Aceton</span></div></div>
"""

# Global variables for handling interruption
products = []
should_continue = True

def signal_handler(signum, frame):
    global should_continue
    print("\nCtrl+C detected. Gracefully stopping and saving progress...")
    should_continue = False

def setup_driver():
    try:
        options = uc.ChromeOptions()
        
        # Set a random user agent
        options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')
        
        # Additional anti-detection measures
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-notifications')
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless')
        
        # Common Brave locations on macOS
        brave_locations = [
            '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
            os.path.expanduser('~/Applications/Brave Browser.app/Contents/MacOS/Brave Browser')
        ]
        
        brave_binary = None
        for location in brave_locations:
            if os.path.exists(location):
                brave_binary = location
                break
                
        if not brave_binary:
            raise Exception("Brave browser not found. Please check if it's installed in the default location.")
            
        options.binary_location = brave_binary
        
        # Initialize driver without headless parameter
        driver = uc.Chrome(
            options=options,
            version_main=131
        )
        
        # Execute CDP commands to prevent detection
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(USER_AGENTS)})
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        })
        
        return driver
    except Exception as e:
        print(f"Error setting up Brave driver: {e}")
        sys.exit(1)

def get_fragrance_notes(driver, product_url):
    try:
        driver.get(product_url)
        time.sleep(random.uniform(1, 2))
        
        # Wait for the product details to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "hbqjtcyY4DmGUU0ezjD6"))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        notes_div = soup.find('div', class_='hbqjtcyY4DmGUU0ezjD6')
        
        if not notes_div:
            return {
                'geurnoot': None,
                'topnoot': None,
                'hartnoot': None,
                'basisnoot': None
            }
            
        notes = {}
        note_types = {
            'Geurnoot': 'geurnoot',
            'Topnoot': 'topnoot',
            'Hartnoot': 'hartnoot',
            'Basisnoot': 'basisnoot'
        }
        
        for div in notes_div.find_all('div', class_='iayHgKPIUZWrzT4fpACP'):
            label = div.find('span', class_='PHtNB5LNBAR0ej2bv6Bf')
            if label and label.text in note_types:
                value = div.find_all('span')[1].text if len(div.find_all('span')) > 1 else None
                notes[note_types[label.text]] = value
                
        # Ensure all note types exist in the dictionary
        for note_type in note_types.values():
            if note_type not in notes:
                notes[note_type] = None
                
        return notes
        
    except Exception as e:
        print(f"Error getting fragrance notes: {e}")
        return {
            'geurnoot': None,
            'topnoot': None,
            'hartnoot': None,
            'basisnoot': None
        }

def process_product(product, driver):
    try:
        time.sleep(random.uniform(0.1, 0.3))
        
        brand = product.find('div', class_='top-brand').text.strip()
        brand_line = product.find('div', class_='brand-line').text.strip()
        name = product.find('div', class_='name').text.strip()
        
        product_parent = product.find_parent('div', class_='product-tile')
        product_url = None
        img_url = None
        
        if product_parent:
            # Get product URL
            link_element = product_parent.find('a')
            if link_element:
                product_url = link_element.get('href')
                if not product_url.startswith('http'):
                    product_url = f"https://www.douglas.be{product_url}"
            
            img_element = product_parent.find('img', class_='image')
            img_url = img_element.get('src') if img_element else None
        
        # Get fragrance notes if we have a product URL
        fragrance_notes = get_fragrance_notes(driver, product_url) if product_url else {
            'geurnoot': None,
            'topnoot': None,
            'hartnoot': None,
            'basisnoot': None
        }
        
        return {
            'brand': brand,
            'brand_line': brand_line,
            'name': name,
            'image_url': img_url,
            **fragrance_notes  # Add all fragrance notes to the product data
        }
        
    except Exception as e:
        print(f"Error processing product: {e}")
        return None

def save_products():
    global products
    try:
        with open('parfums.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        print(f"\nSuccessfully saved {len(products)} products to parfums.json")
    except Exception as e:
        print(f"Error saving products to file: {e}")

def scrape_products():
    global products, should_continue
    driver = None
    current_page = 1
    
    try:
        # Set up signal handler for Ctrl+C
        signal.signal(signal.SIGINT, signal_handler)
        
        driver = setup_driver()
        
        while should_continue:
            page_url = f"{BASE_URL}?page={current_page}"
            print(f"\nProcessing page {current_page}...")
            
            time.sleep(random.uniform(1, 2))
            driver.get(page_url)
            
            time.sleep(random.uniform(1.5, 3))
            
            try:
                # Wait for the product listing to load
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, PRODUCT_LISTING_MAIN_DIV_ID))
                )
            except Exception as e:
                print(f"No more products found on page {current_page}. Finishing...")
                break
                
            # Random scroll behavior
            for _ in range(2):
                driver.execute_script(f"window.scrollTo(0, {random.randint(300, 700)});")
                time.sleep(random.uniform(0.3, 0.7))
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product_containers = soup.find_all('div', class_=PRODUCT_CLASS)
            
            if not product_containers:
                print("No products found on this page. Finishing...")
                break
                
            print(f"Found {len(product_containers)} products on page {current_page}")
            
            for product in product_containers:
                if not should_continue:
                    break
                    
                product_data = process_product(product, driver)
                if product_data:
                    products.append(product_data)
                    print(f"Processed product: {product_data['brand']} - {product_data['brand_line']} (Notes: {product_data['topnoot'] or 'N/A'})")
            
            current_page += 1
            
            # Save progress after each page
            save_products()
            
    except Exception as e:
        print(f"An error occurred: {e}")
        if driver:
            driver.save_screenshot('error.png')
            print("Screenshot saved as error.png")
    
    finally:
        if driver:
            driver.quit()
        # Final save
        save_products()

if __name__ == "__main__":
    scrape_products()