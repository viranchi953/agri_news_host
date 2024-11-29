import requests
from bs4 import BeautifulSoup

def scrape_and_create_website(url, output_html):
    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the webpage content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all containers that have images and headlines
        articles = soup.find_all('img', class_='img-fluid')  # Adjust based on inspection

        # Collect headlines and their associated images
        data = []
        for img_tag in articles:
            # Extract the headline from the 'alt' attribute
            headline = img_tag.get('alt')
            
            # Extract the image URL
            img_url = img_tag.get('data-src') or img_tag.get('src')

            # Debugging: Print extracted headline and image URL
            print(f"Headline: {headline}")
            print(f"Image URL: {img_url}")

            # Validate headline and ensure it has at least 4 words
            if headline and len(headline.split()) >= 4:
                data.append({'headline': headline, 'image': img_url})

        # Ensure data is being captured
        if not data:
            print("No articles found. Please check your selectors.")

        # Create the HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Agriculture News</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f5f5f5;
                }}
                header {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    text-align: center;
                }}
                section {{
                    padding: 20px;
                }}
                h1 {{
                    font-size: 2rem;
                }}
                ul {{
                    list-style-type: none;
                    padding: 0;
                }}
                li {{
                    background: white;
                    margin: 10px 0;
                    padding: 15px;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <header>
                <h1>Agriculture News</h1>
            </header>
            <section>
                <h2>Latest Headlines:</h2>
                <ul>
        """
        
        for item in data:
            html_content += "                    <li>\n"
            if item['image']:
                html_content += f"                        <img src='{item['image']}' alt='Image for {item['headline']}'>\n"
            html_content += f"                        <p>{item['headline']}</p>\n"
            html_content += "                    </li>\n"

        html_content += """
                </ul>
            </section>
        </body>
        </html>
        """

        # Write the HTML content to a file
        with open(output_html, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f"Website created successfully: {output_html}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

# URL of the agriculture news website
url = "https://krishijagran.com/commodity-news"  # Replace with the desired website
output_html = "index2.html"
scrape_and_create_website(url, output_html)
