import os
import scrapy
from selenium import webdriver
import time
import datetime



class NYTimesSpider(scrapy.Spider):
    name = "nytCrawler"
    start_urls = ['https://www.nytimes.com/search?endDate=20190107&query=china&sort=newest&startDate=20190104']
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/google-chrome-unstable'
    options.add_argument('headless')#TBD
    options.add_argument('no-sandbox')
    options.add_argument('disable-gpu')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('window-size=1200x600')
    folder = "./New York Times"
    timestamp = datetime.datetime.now()
    resultsPath = str(folder) + "/" +str(timestamp)

    def __init__(self):
        
        #self.driver = webdriver.Firefox(firefox_options=self.fireFoxOptions)
        self.driver = webdriver.Chrome(chrome_options=self.options)
        #self.driver = webdriver.Firefox()
        #self.driver = webdriver.Chrome('chromedriver')
        self.driver.implicitly_wait(3)
        self.driver.get("https://www.nytimes.com/search?endDate=20190107&query=china&sort=newest&startDate=20190104")
        #print('Now init function finished')
        try:
            os.makedirs(self.resultsPath)
        except:
            print("Folder existed")

    def parse(self, response):
        #self.driver.get(response.url)
        driver = self.driver
        i = 0
        
        # Click load more button until it can't 
        while True:
            #self.driver.find_element_by_xpath('//div[@class="pages-select"]/a[contains(text(), "Next")]').click()
            #more = self.driver.find_element_by_xpath('//div[@class="css-1t62hi8"]/a')
            try:
                driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Have search feedback? Let us know what you think.'])[1]/following::button[1]").click()
                time.sleep(5)
                # i += 1
                # print("\n#####################Click times:%d\n" %i)
                
            except:
                break 

        elements = driver.find_elements_by_class_name('css-138we14')
        #print("url links:%s" %url_links)
        for elem in elements:
            article_url = elem.find_element_by_xpath(".//a").get_attribute("href")
            print("\nCurrent article links:%s\n" %article_url)  
            time.sleep(1)

            #single_article_driver = webdriver.Firefox(firefox_options=self.fireFoxOptions)
            #single_article_driver = webdriver.Chrome('chromedriver',chrome_options=self.chromeOptions)
            single_article_driver = webdriver.Chrome(chrome_options=self.options)
            single_article_driver.get(article_url)
            title = single_article_driver.find_element_by_xpath(".//h1[@itemprop='headline']").text
            content = single_article_driver.find_element_by_xpath(".//section[@name='articleBody']").text
                   
            #title = response.xpath(".//h1[@itemprop='headline']/descendant::text()").extract()
            #content = response.xpath(".//section[@name='articleBody']/descendant::text()").extract()
            yield {
                'title':''.join(title),
                'url':''.join(article_url),
                'content': ''.join(content)
                }
            self.file_write(title, article_url, content)
            single_article_driver.close()
            continue     
        time.sleep(5)

        driver.close()
        # for article_url in response.css('.css-138we14 a ::attr("href")').extract():   
        #         yield response.follow(article_url, callback=self.parse_article)

  
        

    def file_write(self, title, url, content):
        #print("######################file method inside######################")
        fileName = str(title) + ".txt"
            
        file = open(self.resultsPath + "/" +fileName, "w")
        # Write titile, URL, content into the file
        file.write(str(title) + "\n")
        file.write(str(url) + "\n")
        file.write(str(content))
        file.close()