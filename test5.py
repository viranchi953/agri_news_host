#working
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_and_create_website(url, output_html):
    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the webpage content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all containers that have links, images, and headlines
        articles = soup.find_all('a', class_='img')  # Update based on inspection

        # Collect headlines, images, and their links
        data = []
        for article in articles:
            # Extract the link to the news article
            href = article.get('href')
            full_link = urljoin(url, href) if href else None

            # Extract the image URL
            img_tag = article.find('img')
            img_url = img_tag.get('data-src') or img_tag.get('src') if img_tag else None

            # Extract the headline from the 'alt' attribute of the image
            headline = img_tag.get('alt') if img_tag else None

            # Debugging: Print extracted headline, image URL, and link
            print(f"Headline: {headline}")
            print(f"Image URL: {img_url}")
            print(f"Link: {full_link}")

            # Validate headline and ensure it has at least 4 words
            if headline and len(headline.split()) >= 4:
                data.append({'headline': headline, 'image': img_url, 'link': full_link})

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
                    background-color: #f9f9f9;
                }}
                header {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                header h1 {{
                    margin: 0;
                    font-size: 2.5rem;
                }}
                section {{
                    padding: 20px;
                }}
                h2 {{
                    font-size: 1.8rem;
                    margin-bottom: 20px;
                }}
                ul {{
                    list-style-type: none;
                    padding: 0;
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                }}
                li {{
                    background: white;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    transition: transform 0.2s, box-shadow 0.2s;
                }}
                li:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
                }}
                img {{
                    width: 100%;
                    height: 200px;
                    object-fit: cover;
                    border-bottom: 1px solid #ddd;
                }}
                a {{
                    text-decoration: none;
                    color: #333;
                    display: block;
                    padding: 15px;
                }}
                a:hover {{
                    color: #4CAF50;
                }}
                p {{
                    font-size: 1rem;
                    line-height: 1.5;
                    margin: 0;
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
                # Wrap the image and headline in a hyperlink
                html_content += f"                        <a href='{item['link']}'>\n"
                html_content += f"                            <img src='{item['image']}' alt='Image for {item['headline']}'>\n"
                html_content += f"                            <p>{item['headline']}</p>\n"
                html_content += f"                        </a>\n"
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
output_html = "index.html"
scrape_and_create_website(url, output_html)
