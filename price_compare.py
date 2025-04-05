import requests
from bs4 import BeautifulSoup
import streamlit as st

# Flipkart Scraper using requests + BeautifulSoup
def get_flipkart_price(product_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    search_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '+')}"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        price_tag = soup.find("div", class_="_30jeq3 _1_WHN1")
        if price_tag:
            return f"Price of '{product_name}' on Flipkart: {price_tag.text}"
        else:
            return "Price not found on Flipkart."
    except Exception as e:
        return f"Error fetching Flipkart price: {e}"

# Amazon Scraper using requests + BeautifulSoup
def get_amazon_price(product_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    search_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Find the first price
        price_whole = soup.find("span", class_="a-price-whole")
        price_fraction = soup.find("span", class_="a-price-fraction")
        if price_whole and price_fraction:
            price = price_whole.text.strip() + price_fraction.text.strip()
            return f"Price of '{product_name}' on Amazon: ₹{price}"
        else:
            return "Price not found on Amazon."
    except Exception as e:
        return f"Error fetching Amazon price: {e}"

# Streamlit App
st.title("🛒 E-Commerce Price Tracker Chatbot")

product_name = st.text_input("Enter the product you want to search for:")
if st.button("Search Price"):
    flipkart_price = get_flipkart_price(product_name)
    amazon_price = get_amazon_price(product_name)
    
    st.write(flipkart_price)
    st.write(amazon_price)
    
    # Price Comparison
    try:
        f_price = int(flipkart_price.split("₹")[1].replace(",", "").split()[0])
        a_price = int(amazon_price.split("₹")[1].replace(",", "").split()[0])
        cheapest = "Flipkart" if f_price < a_price else "Amazon"
        st.success(f"Cheapest price is on {cheapest}!")
    except:
        st.warning("Could not compare prices. Ensure both results were fetched.")
