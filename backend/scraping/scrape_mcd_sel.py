from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

from utils.geocode import geocode_and_get_hours

# 👇 Generalized function: accepts state name
def scrape_outlets_by_state(state_name: str):
    # Set Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--window-size=1920,1080")  # Optional: set screen size
    chrome_options.add_argument("--no-sandbox")  # For Linux compatibility
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the driver in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get("https://www.mcdonalds.com.my/locate-us")

    wait = WebDriverWait(driver, 10)

    # Select the desired state from dropdown
    dropdown = wait.until(EC.element_to_be_clickable((By.ID, "states")))
    dropdown.click()

    option_xpath = f"//option[text()='{state_name}']"
    state_option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
    state_option.click()
    time.sleep(2)

    all_outlets = []

    while True:
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "addressTop")))
        outlets = driver.find_elements(By.CLASS_NAME, "addressTop")

        for outlet in outlets:
            try:
                name = outlet.find_element(By.CLASS_NAME, "addressTitle").text
                address = outlet.find_element(By.CLASS_NAME, "addressText").text

                results = geocode_and_get_hours(name)
                waze_link=f'https://waze.com/ul?ll={results["latitude"]},{results["longitude"]}&navigate=yes'
                feature_elements = outlet.find_elements(By.CLASS_NAME, "ed-tooltiptext")
                features = [f.text.strip() for f in feature_elements if f.text.strip() != ""]
                # Get all <p class="addressText"> blocks
                p_tags = outlet.find_elements(By.CLASS_NAME, "addressText")

                # Address is in the first one
                address = p_tags[0].text.strip() if len(p_tags) > 0 else ""

                # Tel/Fax is in the second one
                phone = fax = None
                if len(p_tags) > 1:
                    tel_fax_text = p_tags[1].text
                    lines = tel_fax_text.split("\n")
                    for line in lines:
                        if "Tel:" in line:
                            phone = line.replace("Tel:", "").strip()
                        elif "Fax:" in line:
                            fax = line.replace("Fax:", "").strip()


                all_outlets.append({
                    "name": name,
                    "address": address,
                    "waze_link":waze_link ,
                    "hours": results["hours"],
                    "phone": phone,
                    "fax": fax,
                    "features":features,
                    "longitude": results["longitude"],
                    "latitude": results["latitude"],
                    "state": state_name,  # ✅ Add the state info
                })

            except Exception as e:
                print("Error parsing outlet:", e)

        # Handle pagination
        try:
            next_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Next')]")
            if "disabled" in next_btn.get_attribute("class"):  # type: ignore
                break
            next_btn.click()
            time.sleep(2)
        except:
            break

    driver.quit()
    return all_outlets

# Optional test block
if __name__ == "__main__":
    from db.save_to_db import save_outlets_to_db

    state = "Kuala Lumpur"
    data = scrape_outlets_by_state(state)
    print(f"Scraped {len(data)} outlets for {state}")
    save_outlets_to_db(data)
