# Dependencies: Import Splinter and BeautifulSoup
import time
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize the chrome browser in splinter
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    #browser

# Using python to scrape website
def scrape():
    browser = init_browser()
    mars_data = {}

    # Open the Nasa Mars Webpage (must be open to code)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # HTML object
    html = browser.html

    # Parse ('lxml') HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve the latest news title and paragraph 
    # Use 0 bc retrieval is a list and starts at 0, not one
    news_t = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text
    mars_data['news_t'] = news_t
    mars_data['news_p'] = news_p

    # JPL Mars Space Images - Featured Image
    #HTML object
    image_html = Browser.html

    #Parse HTML with Beautiful Soup
    image_soup = bs(image_html, 'html.parser')

    #find first Mars image url
    img_path = image_soup.find('img', class_='thumb')['src']

    #combine url to get image path
    featured_image_url = f'https://www.jpl.nasa.gov{img_path}'

    print(f'featured_image_url = {featured_img_url}')

    # Visit Mars facts page and use Pandas to scrape the table
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    time.sleep(1)

    #HTML object
    mars_facts = browser.html

    #Parse HTML with Beautiful Soup
    soup_f = bs(mars_facts, 'html.parser')

    fact_table = soup_f.find('section', class_='sidebar widget-area clearfix')
    column1 = fact_table.find_all('td', class_='column-1')
    column2 = fact_table.find_all('td', class_='column-2')

    # Empty List to hold the scraped data
    descriptions = []
    values = []

    #  Note: row.text.strip(): Return a copy of the string with the leading and trailing characters removed
    for row in column1:
        description = row.text.strip()
        descriptions.append(description)
    
    for row in column2:
        value = row.text.strip()
        values.append(value)

    # Convert scraped lists to a pandas DF 
    mars_facts = pd.DataFrame({"Description":descriptions,"Value":values})

    # Convert DF to html 
    mars_facts_html = mars_facts.to_html(header=False, index=False)
    mars_data['mars_facts'] = mars_facts_html

# Mars Hemispheres
    # Visit the USGS Astrogeology site 
    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemi_url)
    time.sleep(1)