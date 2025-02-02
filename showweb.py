from flask import Flask, Response
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Route to fetch and modify the website content
@app.route('/proxy')
def proxy():
    target_url = 'https://www.moneycontrol.com/earnings-calendar'
    
    # Fetch the external website content
    response = requests.get(target_url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Hide the div with class 'abc'
    target_div = soup.find('div', class_='clearfix logo_wrapper')
    if target_div:
        target_div['style'] = 'display:none;'  # Hide the div

        target_div_bottom = soup.find('div', class_='bottom_nav')
    if target_div_bottom:
        target_div_bottom['style'] = 'display:none;'  # Hide the div
    
        target_div_header_desktop = soup.find('div', class_='header_desktop')
    if target_div_header_desktop:
        target_div_header_desktop['style'] = 'display:none;'  # Hide the div

        innerPageStrip_forMobNone = soup.find('div', class_='innerPageStrip forMobNone')
    if innerPageStrip_forMobNone:
        innerPageStrip_forMobNone['style'] = 'display:none;'  # Hide the div
    # Return modified HTML content
    return Response(str(soup), content_type='text/html')


# Main app to load iframe
@app.route('/')
def index():
    # Serve the iframe pointing to the proxy route
    return '''
    <html>
    <head><title>Embedded Modified Website</title></head>
    <body style="text-align:center; background-color:#f4f4f9; padding:50px;">
        <h1 style="color:#333;">Modified Embedded Website</h1>
        <iframe src="/proxy" style="width:100%; height:90vh; border:none;"></iframe>
    </body>
    </html>
    '''

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
