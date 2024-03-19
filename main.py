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
    products = []
    if search_results is None:
        return products  # Return an empty list if search results are not available

    try:
        results = search_results.find_all("div", class_="s-result-item")
        for result in results:
            title_element = result.find("span", class_="a-size-medium")
            price_element = result.find("span", class_="a-price")
            image_element = result.find("img", class_="s-image")
            review_count = result.find("span", class_="a-size-base")
            deal_element = result.find("span", class_="a-badge-text")
            if title_element and price_element and image_element:
                title = title_element.get_text().strip()
                price = price_element.find("span", class_="a-offscreen").get_text().strip()
                image_url = image_element["src"]
                link = result.find("a", class_="a-link-normal")["href"]
                reviews = review_count.get_text().strip() if review_count else "No reviews"
                is_deal = bool(deal_element)  # Check if deal_element exists
                products.append({"title": title, "price": price, "image_url": image_url, "link": link, "reviews": reviews, "is_deal": is_deal})

    except Exception as e:
        st.error(f"Error extracting product info: {e}")

    return products




def main():
    try:
        st.title("Amazon Product Search")

        page = st.radio("Navigate", ["Home", "Search Items"])

        if page == "Home":
            # Fetch and display products for a random item category
            item_categories = [
                "TVs", "Home Audio & Theater", "Camera & Photo", "Cell Phones & Accessories", "Headphones",
                "Bluetooth & Wireless Speakers", "Car Electronics", "Musical Instruments", "Wearable Technology",
                "Electronics Accessories & Supplies", "Amazon Devices", "Portable Audio & Video", "Office Electronics",
                "Sports & Fitness", "Outdoor Recreation", "Sports & Fitness Features", "Sports & Outdoor Play",
                "Exercise & Fitness", "Golf", "Fan Shop", "Sports Collectibles", "Outdoor Clothing",
                "Outdoor Recreation Features", "Camping & Hiking", "Climbing", "Skates, Skateboards & Scooters",
                "Water Sports", "Winter Sports", "Cycling", "Accessories", "Action Cameras & Accessories",
                "Drones & Accessories", "Remote & App Controlled Vehicles & Parts", "Remote & App Controlled Vehicle Parts",
                "Remote & App Controlled Vehicles", "Tricycles, Scooters & Wagons", "Ride-On Toys & Accessories",
                "Electrical", "Industrial & Scientific", "Janitorial & Sanitation Supplies", "Food Service Equipment & Supplies",
                "Material Handling Products", "Lab & Scientific Products", "Abrasive & Finishing Products",
                "Retail Store Fixtures & Equipment", "Commercial Lighting", "Commercial Lighting Fixtures",
                "Commercial Lighting", "Professional Medical Supplies", "Professional Dental Supplies",
            ]

            num_items = random.randint(8, 12)
            selected_item_names = random.sample(item_categories, num_items)

            found_products = {category: False for category in item_categories}

            # Fetch and display products for each item category
            for item_category in item_categories:
                search_results = get_search_results(item_category)
                products = extract_product_info(search_results)
                if products:
                    found_products[item_category] = True  # Update found_products dictionary
                    st.header(item_category)
                    for product in products:
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
                    if not found_products[item_category]:  # Display "No products found" message only if no products are found
                        st.write(f"No products found for '{item_category}'. Please try Again.")

        elif page == "Search Items":
            # Display search input and results
            search_query = st.text_input("Enter your search query:")
            if search_query:
                search_results = get_search_results(search_query)
                products = extract_product_info(search_results)
                if products:
                    # Display the search results
                    st.title("Search Results:")
                    for product in products:
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
                    if not found_products[item_category]:
                        st.write(f"No products found for '{item_category}'. Please try Again.")
    except Exception as e:
        st.error(f"Error Accur {e}")

if __name__ == "__main__":
    main()

