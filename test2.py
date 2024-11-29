import requests
from bs4 import BeautifulSoup

def scrape_and_create_website(url, output_html):
    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the webpage content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Modify the selector based on the website's structure
        headlines = soup.find_all('h2')  # Assuming headlines are in <h2> tags

        # Filter headlines with at least 4 words
        valid_headlines = [
            headline.get_text(strip=True) for headline in headlines
            if len(headline.get_text(strip=True).split()) >= 4
        ]

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
        
        for headline in valid_headlines:
            html_content += f"                    <li>{headline}</li>\n"

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
url = "https://krishijagran.com/"  # Replace with the desired website
output_html = "index.html"
scrape_and_create_website(url, output_html)
