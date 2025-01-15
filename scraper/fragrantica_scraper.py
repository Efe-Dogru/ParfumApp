import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import json
import time
import urllib.parse
import random
import os
import ssl

# Disable SSL verification for urllib
ssl._create_default_https_context = ssl._create_unverified_context

class FragranticaScraper:
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--disable-gpu')
        
        # Add user agent
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
        
        # Random window size to appear more human-like
        width = random.randint(1200, 1600)
        height = random.randint(800, 1000)
        options.add_argument(f'--window-size={width},{height}')
        
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.path.expanduser("~"), ".undetected_chromedriver")
        os.makedirs(data_dir, exist_ok=True)
        
        try:
            self.driver = uc.Chrome(
                options=options,
                driver_executable_path=None,
                suppress_welcome=True,
                version_main=131
            )
        except Exception as e:
            print(f"Error initializing Chrome: {str(e)}")
            raise
            
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "https://www.fragrantica.com"
        self.data = self.load_existing_data()

    def load_existing_data(self):
        """Load existing data from JSON file if it exists"""
        try:
            if os.path.exists("perfumes.json"):
                with open("perfumes.json", "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading existing data: {str(e)}")
        return {}

    def save_to_json(self):
        """Save current data to JSON file"""
        try:
            with open("perfumes.json", "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            print("Data saved successfully!")
        except Exception as e:
            print(f"Error saving data: {str(e)}")

    def random_sleep(self, min_seconds=1, max_seconds=2):
        time.sleep(random.uniform(min_seconds, max_seconds))

    def human_like_scroll(self):
        """Scroll the page in a more human-like manner"""
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        current_height = 0
        scroll_height = random.randint(300, 500)
        
        while current_height < total_height:
            current_height += scroll_height
            self.driver.execute_script(f"window.scrollTo(0, {current_height});")
            self.random_sleep(0.2, 0.5)

    def wait_and_get_elements(self, selector, by=By.CSS_SELECTOR, timeout=10, retries=3):
        for attempt in range(retries):
            try:
                self.wait = WebDriverWait(self.driver, timeout)
                elements = self.wait.until(
                    EC.presence_of_all_elements_located((by, selector))
                )
                if all(self.is_element_valid(elem) for elem in elements):
                    return elements
            except (TimeoutException, StaleElementReferenceException):
                if attempt == retries - 1:
                    return []
            self.random_sleep(0.5, 1)
        return []

    def wait_and_get_element(self, selector, by=By.CSS_SELECTOR, timeout=10, retries=3):
        for attempt in range(retries):
            try:
                self.wait = WebDriverWait(self.driver, timeout)
                element = self.wait.until(
                    EC.presence_of_element_located((by, selector))
                )
                if self.is_element_valid(element):
                    return element
            except (TimeoutException, StaleElementReferenceException):
                if attempt == retries - 1:
                    return None
            self.random_sleep(0.5, 1)
        return None

    def is_element_valid(self, element):
        try:
            element.is_enabled()
            return True
        except StaleElementReferenceException:
            return False

    def safe_get_attribute(self, element, attribute):
        try:
            return element.get_attribute(attribute)
        except (StaleElementReferenceException, NoSuchElementException):
            return None

    def get_perfume_details(self, url):
        try:
            self.driver.get(url)
            self.random_sleep(1, 2)
            self.human_like_scroll()
            
            # Get perfume name - Updated to get only the main name without small tag content
            name = "Unknown"
            name_container = self.wait_and_get_element(".cell.small-12 h1.text-center.medium-text-left")
            if name_container:
                # Get all text content
                full_text = name_container.text
                # Find and remove the small tag content if it exists
                small_tag = name_container.find_element(By.TAG_NAME, "small") if name_container else None
                if small_tag:
                    small_text = small_tag.text
                    name = full_text.replace(small_text, '').strip()
                else:
                    name = full_text.strip()
            
            # Get perfume image
            img_element = self.wait_and_get_element(".cell.small-12 img[itemprop='image']")
            if not img_element:
                img_element = self.wait_and_get_element(".cell.small-12 img")
            img_url = self.safe_get_attribute(img_element, "src") if img_element else None
            
            # Get main accords
            accords = []
            accord_container = self.wait_and_get_element(".grid-x:has(.cell.accord-box)")
            if accord_container:
                accord_elements = accord_container.find_elements(By.CLASS_NAME, "accord-box")
                for accord in accord_elements:
                    try:
                        accord_bar = accord.find_element(By.CLASS_NAME, "accord-bar")
                        if accord_bar:
                            accord_text = accord_bar.text.strip()
                            if accord_text:
                                accords.append(accord_text)
                    except (NoSuchElementException, StaleElementReferenceException):
                        continue

            # Get perfume notes
            notes = {
                "top": [],
                "middle": [],
                "base": []
            }
            
            # Find the pyramid section
            pyramid_section = self.wait_and_get_element("#pyramid")
            if pyramid_section:
                current_note_type = None
                # Find all h4 elements (note type headers) and their following note links
                elements = pyramid_section.find_elements(By.CSS_SELECTOR, "h4, a[href*='/notes/']")
                
                for element in elements:
                    try:
                        # If it's an h4 element, it indicates the note type
                        if element.tag_name == "h4":
                            header_text = element.text.lower().strip()
                            if "top" in header_text:
                                current_note_type = "top"
                            elif "middle" in header_text or "heart" in header_text:
                                current_note_type = "middle"
                            elif "base" in header_text:
                                current_note_type = "base"
                        # If it's an 'a' element and we know the current note type, add the note
                        elif element.tag_name == "a" and current_note_type:
                            note_text = element.text.strip()
                            if note_text and note_text not in notes[current_note_type]:
                                notes[current_note_type].append(note_text)
                    except (NoSuchElementException, StaleElementReferenceException) as e:
                        continue

            perfume_data = {
                "name": name.strip(),
                "image_url": img_url,
                "main_accords": accords,
                "notes": notes,
                "url": url
            }
            return perfume_data
        except Exception as e:
            print(f"Error scraping perfume {url}: {str(e)}")
            return None

    def get_urls_from_elements(self, elements):
        urls = []
        for element in elements:
            try:
                href = self.safe_get_attribute(element, "href")
                if href:
                    urls.append(urllib.parse.urljoin(self.base_url, href))
            except StaleElementReferenceException:
                continue
        return urls

    def scrape_brand_perfumes(self, brand_url, country_name):
        try:
            self.driver.get(brand_url)
            self.random_sleep(1, 2)
            self.human_like_scroll()
            
            perfume_links = self.wait_and_get_elements(".tabs-panel.is-active a[href*='/perfume/']")
            brand_name = brand_url.split('/')[-1].replace('.html', '')
            
            perfumes = []
            perfume_urls = self.get_urls_from_elements(perfume_links)
            
            for url in perfume_urls:
                perfume_details = self.get_perfume_details(url)
                if perfume_details:
                    perfumes.append(perfume_details)
                    # Update data structure and save after each perfume
                    if country_name not in self.data:
                        self.data[country_name] = {}
                    if brand_name not in self.data[country_name]:
                        self.data[country_name][brand_name] = []
                    self.data[country_name][brand_name] = perfumes
                    self.save_to_json()
                self.random_sleep(0.5, 1)
            
            return brand_name, perfumes
            
        except Exception as e:
            print(f"Error scraping brand {brand_url}: {str(e)}")
            return None, []

    def scrape_country_brands(self, country_url):
        try:
            self.driver.get(country_url)
            self.random_sleep(1, 2)
            self.human_like_scroll()
            
            brand_links = self.wait_and_get_elements("a[href*='/designers/']")
            country_name = country_url.split('/')[-1].replace('.html', '')
            
            brands = {}
            brand_urls = self.get_urls_from_elements(brand_links)
            
            for url in brand_urls:
                brand_name, perfumes = self.scrape_brand_perfumes(url, country_name)
                if brand_name and perfumes:
                    brands[brand_name] = perfumes
                self.random_sleep(0.5, 1)
            
            return country_name, brands
            
        except Exception as e:
            print(f"Error scraping country {country_url}: {str(e)}")
            return None, {}

    def scrape_all(self):
        try:
            self.driver.get(f"{self.base_url}/country/")
            self.random_sleep(1, 2)
            
            country_links = self.wait_and_get_elements(".countrylist.cell.small-6.large-4 a")
            country_urls = self.get_urls_from_elements(country_links)
            
            for url in country_urls:
                country_name, brands = self.scrape_country_brands(url)
                if country_name and brands:
                    self.data[country_name] = brands
                self.random_sleep(1, 2)
                
            print("Scraping completed successfully!")
            
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    scraper = FragranticaScraper()
    scraper.scrape_all() 