import os
import scrapy
from selenium import webdriver
import datetime
import time
import json
import logging



class ReutersSpider(scrapy.Spider):
    name = "reutersCrawler"
    #start_url is not use but need to place in here
    start_urls = ['https://www.reuters.com/search/news?blob=taiwan&sortBy=date&dateRange=pastDay']
    #start_urls = request_url

    #Define chrome related parameters
    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/google-chrome-unstable'
    options.add_argument('headless')
    options.add_argument('no-sandbox')
    options.add_argument('disable-gpu')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('window-size=1200x600')

    def __init__(self, *args, **kwargs):
        #Initialize the spider
        self.driver = webdriver.Chrome(chrome_options=self.options)

        # Get the projectID and parsed request for this spider
        with open('/tmp/project_request.json') as f:
            data = json.load(f)
        self.projectID = data['projectID']
        self.request_url = data['query_url']['Reuters']
        self.timestamp = data['timestamp']
        self.logger.info('\nprojectID= %s\n', self.projectID)
        self.logger.info('\nrequest_url= %s\n', self.request_url)
        self.logger.info('\ntimestamp= %s\n', self.timestamp)

        # Finalize the path for store files
        self.folder = "/data/projects/"+ self.projectID
        self.resultsPath = str(str(self.folder) + "/crawler" + "/Reuters" + "/" + self.timestamp)
        self.logger.info('\n Resultpath= %s\n', self.resultsPath)
        
        self.driver.implicitly_wait(3)
        if not os.path.exists(self.resultsPath):
            try:
                os.makedirs(self.resultsPath)
            except Exception as ee:
                print(str(ee))
    
    def parse(self, response):

        driver = self.driver
        driver.get(self.request_url)
        while True:
            try:
                load_more = driver.find_element_by_xpath("//*[contains(text(), 'LOAD MORE RESULTS')]")
                load_more.click()
            except:
                break

        h3_elements = driver.find_elements_by_class_name('search-result-title')
        for elem in h3_elements:
            
            article_url = elem.find_element_by_xpath(".//a").get_attribute("href")
        
            print("Reuters Article URL:%s" %article_url)
            single_article_driver = webdriver.Chrome(chrome_options=self.options)
            single_article_driver.get(article_url)


            try:
                title = single_article_driver.find_element_by_css_selector('h1.ArticleHeader_headline').text
                content = single_article_driver.find_element_by_xpath(".//div[@class='StandardArticleBody_body']").text
                
                current_article = {
                    'title':title,
                    'source': 'Reuters',
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
        
