import os
import scrapy
from selenium import webdriver
import datetime
import time


class ReutersSpider(scrapy.Spider):
    name = "reutersCrawler"
    start_urls = ['https://www.reuters.com/search/news?blob=taiwan&sortBy=date&dateRange=pastDay']
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/google-chrome-unstable'
    options.add_argument('headless')
    options.add_argument('no-sandbox')
    options.add_argument('disable-gpu')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('window-size=1200x600')
    folder = "./Reuters"
    timestamp = datetime.datetime.now()
    resultsPath = str(folder) + "/" +str(timestamp)
    
    def __init__(self):
        
        #self.driver = webdriver.Firefox(firefox_options=self.fireFoxOptions)
        self.driver = webdriver.Chrome(chrome_options=self.options)
        #self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(3)
        try:
            os.makedirs(self.resultsPath)
        except:
            print("Folder existed")

    def parse(self, response):

        driver = self.driver
        subfolder_timestamp = self.timestamp
        driver.get('https://www.reuters.com/search/news?blob=taiwan&sortBy=date&dateRange=pastDay')

        while True:
            try:
                load_more = driver.find_element_by_xpath("//*[contains(text(), 'LOAD MORE RESULTS')]")
                #print("Load More!")
                load_more.click()
            except:
                #print("No More!")
                break

        h3_elements = driver.find_elements_by_class_name('search-result-title')
        for elem in h3_elements:
            
            article_url = elem.find_element_by_xpath(".//a").get_attribute("href")
            
            #article_url='https://www.reuters.com'+ str(article_path)
            print("Article URL:%s" %article_url)
            #single_article_driver = webdriver.Firefox(firefox_options=self.fireFoxOptions)
            single_article_driver = webdriver.Chrome(chrome_options=self.options)
            
            #single_article_driver = webdriver.Firefox()
            single_article_driver.get(article_url)


            try:
                title = single_article_driver.find_element_by_css_selector('h1.ArticleHeader_headline').text
                content = single_article_driver.find_element_by_xpath(".//div[@class='StandardArticleBody_body']").text
                
                yield {
                    'title':''.join(title),
                    'url':''.join(article_url),
                    'content': ''.join(content)
                    }
                self.file_write(title, article_url, content)
                single_article_driver.close()
                continue
            except:
                print("Error happened")
                single_article_driver.close()
                continue
        driver.close()

    def file_write(self, title, url, content):
        #print("######################file method inside######################")
        fileName = str(title) + ".txt"
            
        file = open(self.resultsPath + "/" +fileName, "w")
        # Write titile, URL, content into the file
        file.write(str(title) + "\n")
        file.write(str(url) + "\n")
        file.write(str(content))
        file.close()
