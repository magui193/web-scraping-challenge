from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    results  = {}
    #Mars News
   # Define news website
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Create BeautifulSoup
    html = browser.html
    mars_news = BeautifulSoup(html, 'html.parser')
    print(mars_news)

    # Retrieve all elements that contain the news information
    news_title = mars_news.body.find('div', class_='content_title').text

    news_parag = mars_news.body.find('div', class_='article_teaser_body').text

    # Print news
    print(f"The title is: {news_title}")
    print(f"The descriptive paragraph is: {news_parag}")

    #Mars Image
    # Define image website
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    # HTML with soup
    html = browser.html
    image_mars = BeautifulSoup(html, 'html.parser')
    print(image_mars)

    button = image_mars.find_all('button')[1].find_parent()["href"]

    full_image_url = f"https://spaceimages-mars.com/{button}"

    #Mars Facts
    facts_url = "https://galaxyfacts-mars.com/"

    # Convert info into DataFrame
    table = pd.read_html(facts_url)

    # Create table
    mars_df = pd.DataFrame(table[0])
    mars_df.columns = ["Description", "Mars", "Earth"]
    mars_df.set_index('Description')

    mars_df.to_html('mars_facts.html')

    # Hemisphere
    # Visit URL
    hem_url = "https://marshemispheres.com/"
    browser.visit(hem_url)

    # Create dictionary
    img_link_dict = {}

    # Create soup
    html = browser.html
    image_hem = BeautifulSoup(html, 'html.parser')
    # print(image_hem)

    # Create lopps to gather images
    links = browser.links.find_by_partial_text("Hemisphere Enhanced")

    for index, link in enumerate(links):
        if index > 0:
            browser.back()
            time.sleep(2)
            links = browser.links.find_by_partial_text("Hemisphere Enhanced")
        link = links[index]
        title = link.text
        link.click()
        time.sleep(1)
        inner_html = browser.html
        inner_soup = BeautifulSoup(inner_html, 'html.parser')
        downloads = inner_soup.find_all('div', class_='downloads')
        for download in downloads:
            # print(download)
            lis = download.find_all("li")
            # print(lis)
            for li in lis:
                if "Original" in li.text:
                    partial_link = li.find('a')['href']
                    img_link_dict[title] = f'{hem_url}{partial_link}'
    results = {
       'latesttitle': news_title,
       'lastestparagraph': news_parag,
       'imagemars': full_image_url,
       'factstable': mars_facts,
       'hemisphere_image_urls': img_link_dict
    }

    # Stop browser
    browser.quit()
    
    return results