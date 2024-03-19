import requests
from bs4 import BeautifulSoup
import streamlit as st
import random
import logging
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO)


def get_search_results(search_query):
    try:
        url = f"https://www.amazon.com/s?k={search_query}"

        ua = UserAgent(browsers=['Safari', 'edge', 'chrome'])

        # headers_list = [
        #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        #     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
        #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
        #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        # ]
        #
        # user_agent = random.choice(headers_list)

        headers = {
            "User-Agent": ua.random,
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        logging.info(f"Response status code: {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    except requests.RequestException as e:
        logging.error(f"Error fetching search results: {e}")
        return None


def extract_product_info(search_results):

    try:
        products = []
        results = search_results.find_all("div", class_="s-result-item")
        for result in results:
            title_element = result.find("span", class_="a-size-medium")
            price_element = result.find("span", class_="a-price")

            image_element = result.find("img", class_="s-image")
            review_count_element = result.find("span", class_="a-size-base")
            deal_element = result.find("span", class_="a-badge-text")

            if title_element and price_element and image_element:
                title = title_element.get_text().strip()
                price = price_element.find("span", class_="a-offscreen").get_text().strip()
                image_url = image_element["src"]
                link = result.find("a", class_="a-link-normal")["href"]
                reviews = review_count_element.get_text().strip() if review_count_element else "No reviews"
                is_deal = bool(deal_element)  # Check if deal_element exists
                products.append(
                    {"title": title, "price": price, "image_url": image_url, "link": link, "reviews": reviews,
                     "is_deal": is_deal})
        return products
    except Exception as e:
        st.error(f"Error extracting product info: {e}")
        return []

    except RuntimeError:
        st.error("An error occurred. Please try again.")

    except ConnectionError:
        st.error("A connection error occurred. Please check your internet connection and try again.")


def main():
    try:
        st.title("Amazon Product Search")

        page = st.radio("Navigate", ["Home", "Search Items"])

        if page == "Home":
            # Fetch and display products for a random item category
            random_item_names = [
                "TVs", "Home Audio & Theater", "Camera & Photo", "Cell Phones & Accessories", "Headphones",
                "Bluetooth & Wireless Speakers", "Car Electronics", "Musical Instruments", "Wearable Technology",
                "Electronics Accessories & Supplies", "Amazon Devices", "Portable Audio & Video", "Office Electronics",
                "Sports & Fitness", "Outdoor Recreation", "Sports & Fitness Features", "Sports & Outdoor Play",
                "Exercise & Fitness", "Golf", "Fan Shop", "Sports Collectibles", "Outdoor Clothing",
                "Outdoor Recreation Features", "Camping & Hiking", "Climbing", "Skates, Skateboards & Scooters",
                "Water Sports", "Winter Sports", "Cycling", "Accessories", "Action Cameras & Accessories",
                "Drones & Accessories", "Remote & App Controlled Vehicles & Parts", "Remote & App Controlled Vehicle Parts",
                "Tricycles, Scooters & Wagons", "Ride-On Toys & Accessories",
                "Electrical", "Industrial & Scientific", "Janitorial & Sanitation Supplies", "Food Service Equipment & Supplies",
                "Material Handling Products", "Lab & Scientific Products",
                "Retail Store Fixtures & Equipment", "Commercial Lighting", "Commercial Lighting Fixtures",
                "Commercial Lighting", "Professional Medical Supplies", "Professional Dental Supplies",
            ]

            num_items = random.randint(8, 12)
            selected_item_names = random.sample(random_item_names, num_items)

            for item_name in selected_item_names:
                search_results = get_search_results(item_name)
                if search_results:
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
                                st.write("Deal Available" if product['is_deal'] else "No Deal Available")
                                st.link_button("View on Amazon", f"https://www.amazon.com{product['link']}")
                            st.markdown("---")
                    else:
                        st.write(f"No products found for '{item_name}'.")

                else:
                    st.error("Amazon server is currently unavailable. Please try again later.")


        elif page == "Search Items":
            # Display search input and results
            search_query = st.text_input("Enter your search query:")
            if search_query:
                search_results = get_search_results(search_query)
                if search_results:
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
                                st.write("Deal Available" if product['is_deal'] else "No Deal Available")
                                st.link_button("View on Amazon", f"https://www.amazon.com{product['link']}")
                            st.markdown("---")
                    else:
                        st.write(f"No products found for '{search_query}'.")
                else:
                    st.error("Amazon server is currently unavailable. Please try again later.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

