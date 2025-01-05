import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import streamlit as st


# Flipkart Scraper with Selenium
def get_flipkart_price(product_name):
    # Initialize the driver
    driver = webdriver.Edge()

    # Open the Flipkart search URL
    driver.get(f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}")

    # Give the page some time to load completely
    time.sleep(5)

    try:
        # Parse the page using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Locate all price elements
        price_elements = soup.find_all('div', class_='hl05eU')

        # Extracting the first price (discounted price)
        if price_elements:
            discounted_price = price_elements[0].text.strip().split('₹')[1]  # Extract only the discounted price
            return f"Price of '{product_name}' on Flipkart: ₹{discounted_price}"
        else:
            return "Price not found."
    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()

# Function to scrape Amazon using Selenium
def get_amazon_price(product_name):
    driver = webdriver.Edge()
    driver.get("https://www.amazon.in/")
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys(product_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    try:
        price = driver.find_element(By.CLASS_NAME, "a-price-whole").text
        return f"Price of '{product_name}' on Amazon: ₹{price}"
    except:
        return "Product not found on Amazon."
    finally:
        driver.quit()

# Streamlit App
st.title("E-Commerce Price Tracker Chatbot")

product_name = st.text_input("Enter the product you want to search for:")
if st.button("Search Price"):
    flipkart_price = get_flipkart_price(product_name)
    amazon_price = get_amazon_price(product_name)
    
    st.write(flipkart_price)
    st.write(amazon_price)
    
    # Price Comparison
    try:
        f_price = int(flipkart_price.split("₹")[1].replace(",", ""))
        a_price = int(amazon_price.split("₹")[1].replace(",", ""))
        cheapest = "Flipkart" if f_price < a_price else "Amazon"
        st.success(f"Cheapest price is on {cheapest}!")
    except:
        st.warning("Could not compare prices. Ensure both results were fetched.")
