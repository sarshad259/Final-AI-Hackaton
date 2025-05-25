from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

def get_job_data_selenium():
    options = Options()
    options.headless = True  # Run Chrome headless (no GUI)
    driver = webdriver.Chrome(options=options)  # Make sure chromedriver is in PATH
    
    # URL for IT/Software jobs - change this as needed
    driver.get("https://www.rozee.pk/search/jobs?search[category]=it-software")
    time.sleep(5)  # Wait for page to load
    
    jobs = []

    # Inspect this selector in your browser for current job card titles
    job_elements = driver.find_elements(By.CSS_SELECTOR, "div.job-card__title")
    
    for job_elem in job_elements:
        title = job_elem.text.strip()

        # Find parent element to get location, skills, date from the same card
        parent = job_elem.find_element(By.XPATH, "..")  # up one level

        try:
            location = parent.find_element(By.CSS_SELECTOR, "span.job-card__location").text.strip()
        except:
            location = ""
        try:
            skills = parent.find_element(By.CSS_SELECTOR, "span.job-card__skills").text.strip()
        except:
            skills = ""
        try:
            date = parent.find_element(By.CSS_SELECTOR, "span.job-card__date").text.strip()
        except:
            date = ""

        jobs.append({
            "title": title,
            "location": location,
            "skills": skills,
            "date": date
        })
    
    driver.quit()
    df = pd.DataFrame(jobs)
    return df
