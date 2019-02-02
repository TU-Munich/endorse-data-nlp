import os
import scrapy
from selenium import webdriver
import datetime
import time
import json



class ReutersSpider(scrapy.Spider):
    name = "reutersCrawler"
    start_urls = ['https://www.reuters.com/search/news?blob=taiwan&sortBy=date&dateRange=pastDay']
    
    #Define firefox related parameters
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()

    #Define chrome related parameters
    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/google-chrome-unstable'
    options.add_argument('headless')
    options.add_argument('no-sandbox')
    options.add_argument('disable-gpu')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('window-size=1200x600')

    
    def __init__(self, projectID=None, *args, **kwargs):
        super(ReutersSpider, self).__init__(*args, **kwargs)
        #self.driver = webdriver.Firefox(firefox_options=self.fireFoxOptions)
        self.driver = webdriver.Chrome(chrome_options=self.options)
        #self.driver = webdriver.Firefox()
        self.folder = "/data/projects/"+ projectID
        self.resultsPath = str(self.folder) + "/crawler" + "/Reuters"

        self.driver.implicitly_wait(3)
        if not os.path.exists(self.resultsPath):
            try:
                os.makedirs(self.resultsPath)
                print("\nfolder is not existed and i created!\n")
            except Exception as ee:
                print(str(ee))

    def parse(self, response):

        driver = self.driver
        driver.get('https://www.reuters.com/search/news?blob=taiwan&sortBy=date&dateRange=pastDay')

        while True:
            try:
                load_more = driver.find_element_by_xpath("//*[contains(text(), 'LOAD MORE RESULTS')]")
                load_more.click()
            except:
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
                
                current_article = {
                    'title':title,
                    'url': article_url,
                    'content': content
                    }
                yield current_article

                self.file_write(current_article)
                single_article_driver.close()
                continue
            except Exception as ee:
                print(str(ee))
                single_article_driver.close()
                continue
        driver.close()

    
    def file_write(self, article):
        
        fileName = str(article['title']) + ".json"
        with open(self.resultsPath + "/" +fileName, "w") as outfile:
            json.dump(article, outfile)
        
