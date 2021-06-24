# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data


def mars_news(browser):

    browser.visit('https://redplanetscience.com/')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find_all(class_='content_title')
    pgraphs = soup.find_all(class_='article_teaser_body')
    news_title=titles[0].text.strip()
    news_p=pgraphs[0].text.strip()

    return news_title, news_p


def featured_image(browser):
    browser.visit('https://spaceimages-mars.com/')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured=soup.find_all(class_='floating_text_area')
    link=featured[0].find('a')   
    href = link['href']
    img_url ='https://spaceimages-mars.com/' + href

    return img_url


def mars_facts():
    df = pd.read_html('https://galaxyfacts-mars.com/')[1].rename(columns={0:'Index',1:'Value'}).to_html(index=False)

    return df


def hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit('https://marshemispheres.com/')
    hemispheres=[]
    for i in range(4):
        hemisphere = {}
        hemisphere['title'] = browser.find_by_css('a.itemLink h3')[i].text
        browser.find_by_css('a.itemLink h3')[i].click()
        hemisphere['img_url'] = browser.find_by_text('Sample')['href']
        hemispheres.append(hemisphere)
        browser.back()
       
    return hemispheres


if __name__ == "__main__":
    print(scrape_all())
