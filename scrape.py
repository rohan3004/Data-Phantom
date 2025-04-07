from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def save_html():
    url = "https://codolio.com/profile/rohan3004"

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # updated for Chrome 115+
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        time.sleep(5)
        with open("output.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        print("HTML saved to output.html")
    except Exception as e:
        print("Error during scraping:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    save_html()
