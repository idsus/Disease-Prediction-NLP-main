# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Setting up Chrome options
options = Options()
# options.headless = True 
driver = webdriver.Chrome(options=options)

# Base URL
base_url = "https://www.drugs.com/comments/sertraline/zoloft.html?page={}"

# Data storage
data = []

# Loop through the pages
for page_num in range(0, 26):
    driver.get(base_url.format(page_num))
    
    # Wait for the reviews to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ddc-comment"))
    )
    
    # Find all review cards
    reviews = driver.find_elements(By.CLASS_NAME, "ddc-comment")
    
    # Extract data from each review
    for review in reviews:
        review_data = {}
        review_data["Medicine Name"] = "Zoloft"  # Static value
        
        # Using XPath to navigate the structure as it's more flexible for this use case
        review_data["Condition"] = review.find_element(By.XPATH, ".//b").text
        review_data["Review"] = review.find_element(By.CLASS_NAME, "ddc-comment-content").text
        rating = review.find_element(By.XPATH, ".//div[contains(@class, 'ddc-rating-summary')]/span").text.split('/')[0]
        review_data["Rating"] = int(rating) if rating.isdigit() else None
        review_data["Date"] = review.find_element(By.CLASS_NAME, "comment-date").text.strip()
        usefulCount = review.find_element(By.XPATH, ".//a[contains(@data-vote, '1')]").get_attribute('data-like-count')
        review_data["Useful Count"] = int(usefulCount) if usefulCount and usefulCount.isdigit() else None
        
        data.append(review_data)

# Converting data to DataFrame
df = pd.DataFrame(data)

# Display the first few rows to check
print(df.head())

# Save to CSV
df.to_csv('Zoloft_Reviews.csv', index=False)

# Close the driver
driver.quit()
