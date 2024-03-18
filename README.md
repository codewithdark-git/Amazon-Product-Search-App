
# Amazon Product Search App

This is a Streamlit web application that allows users to search for products on Amazon and display the search results. Users can either view random products from various categories or search for specific products by entering a search query.

## Features

- **Home Page**: Displays random products from various categories.
- **Search Page**: Allows users to search for specific products by entering a search query.
- **Product Information**: Shows product images, titles, prices, reviews, and whether it's a deal of the day.
- **View on Amazon**: Provides a direct link to view the product on Amazon's website.
- **Exception Handling**: Provides error messages for various exceptions such as connection errors.

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/codewithdark-git/amazon-product-search.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

4. Open your web browser and go to `http://localhost:8501` to access the app.

## Dependencies

- **requests**: For sending HTTP requests to Amazon's website.
- **Beautiful Soup**: For parsing HTML content.
- **Streamlit**: For building the web application.
- **urllib**: For URL parsing.

## Credits

This app was created by [Your Name].

## License

This project is licensed under the [MIT License](LICENSE).
