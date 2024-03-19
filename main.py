import requests
from bs4 import BeautifulSoup
import streamlit as st
import random
from urllib.parse import urlparse


def get_search_results(search_query):
    url = f"https://www.amazon.com/s?k={search_query}"

    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def extract_product_info(search_results):
    products = []
    results = search_results.find_all("div", class_="s-result-item")
    for result in results:
        title_element = result.find("span", class_="a-size-medium")
        price_element = result.find("span", class_="a-price")
        image_element = result.find("img", class_="s-image")
        review_count = result.find("span", class_="a-size-base")
        deal_element = result.find("span", class_="a-badge-text", text="Deal of the Day")
        if title_element and price_element and image_element:
            title = title_element.get_text().strip()
            price = price_element.find("span", class_="a-offscreen").get_text().strip()
            image_url = image_element["src"]
            link = result.find("a", class_="a-link-normal")["href"]
            reviews = review_count.get_text().strip() if review_count else "No reviews"
            is_deal = bool(deal_element)  # Check if deal_element exists
            products.append({"title": title, "price": price, "image_url": image_url, "link": link, "reviews": reviews, "is_deal": is_deal})
    return products


def main():
    try:
        st.title("Amazon Product Search")

        page = st.radio("Navigate", ["Home", "Search Items"])

        if page == "Home":
            # Fetch and display products for a random item category
            random_item_names = [
                    "TVs",
                    "Home Audio & Theater",
                    "Camera & Photo",
                    "Cell Phones & Accessories",
                    "Headphones",
                    "Bluetooth & Wireless Speakers",
                    "Car Electronics",
                    "Musical Instruments",
                    "Wearable Technology",
                    "Electronics Accessories & Supplies",
                    "Amazon Devices",
                    "Portable Audio & Video",
                    "Office Electronics",
                    "Sports & Fitness",
                    "Outdoor Recreation",
                    "Sports & Fitness Features",
                    "Sports & Outdoor Play",
                    "Exercise & Fitness",
                    "Golf",
                    "Fan Shop",
                    "Sports Collectibles",
                    "Outdoor Clothing",
                    "Outdoor Recreation Features",
                    "Camping & Hiking",
                    "Climbing",
                    "Skates, Skateboards & Scooters",
                    "Water Sports",
                    "Winter Sports",
                    "Cycling",
                    "Accessories",
                    "Action Cameras & Accessories",
                    "Drones & Accessories",
                    "Remote & App Controlled Vehicles & Parts",
                    "Remote & App Controlled Vehicle Parts",
                    "Remote & App Controlled Vehicles",
                    "Tricycles, Scooters & Wagons",
                    "Ride-On Toys & Accessories",
                    "Electrical",
                    "Industrial & Scientific",
                    "Janitorial & Sanitation Supplies",
                    "Food Service Equipment & Supplies",
                    "Material Handling Products",
                    "Lab & Scientific Products",
                    "Abrasive & Finishing Products",
                    "Retail Store Fixtures & Equipment",
                    "Commercial Lighting",
                    "Commercial Lighting Fixtures",
                    "Commercial Lighting",
                    "Professional Medical Supplies",
                    "Professional Dental Supplies",]

            num_items = random.randint(10, 15)
            selected_item_names = random.sample(random_item_names, num_items)

            for item_name in selected_item_names:
                search_results = get_search_results(item_name)
                products = extract_product_info(search_results)
                if products:
                    for idx, product in enumerate(products, start=1):
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.image(product['image_url'])
                        with col2:
                            st.markdown(f"{product['title']}")
                            st.subheader(f"{product['price']}")
                            st.write(f"**Reviews:** {product['reviews']}")
                            st.write(f"{product['is_deal']}")
                            st.link_button("View on Amazon", f"https://www.amazon.com{product['link']}")
                        st.markdown("---")
                else:
                    st.write(f"No products found for '{item_name}'.")

        elif page == "Search Items":
                # Display search input and results
            search_query = st.text_input("Enter your search query:")
            if search_query:
                search_results = get_search_results(search_query)
                products = extract_product_info(search_results)

                if products:
                        # Display the search results
                    st.title("Search Results:")
                    for idx, product in enumerate(products, start=1):
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.image(product['image_url'])
                        with col2:
                            st.markdown(f"{product['title']}")
                            st.subheader(f"{product['price']}")
                            st.write(f"**Reviews:** {product['reviews']}")
                            st.write(f"{product['is_deal']}")
                            st.link_button("View on Amazon", f"https://www.amazon.com{product['link']}")
                        st.markdown("---")
                else:
                    st.write(f"No products found for '{search_query}'.")
    except Exception as e:
        st.error(f"Please Try Again {e}")

    except RuntimeError:
        st.error(f"Please Try Again Check Your Connection")

    except ConnectionError:
        st.error(f"Please Try Again Check Your Connection")


if __name__ == "__main__":
    main()
