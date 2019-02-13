import os
import scrapy
from selenium import webdriver
import time
import time
import datetime


class BloombergSpider(scrapy.Spider):
    name = "bloombergCrawler"
    start_urls = ['https://www.bloomberg.com/search?query=germany&startTime=-1d&sort=time:desc&endTime=2019-01-30T21:31:38.818Z&page=']
    base_url = 'https://www.bloomberg.com/search?query=germany&startTime=-1d&sort=time:desc&endTime=2019-01-30T21:31:38.818Z&page='
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    options = webdriver.ChromeOptions()
    options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    options.add_argument('headless')#TBD
    options.add_argument('no-sandbox')
    options.add_argument('disable-gpu')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('window-size=1200x600')
    folder = "./Bloomberg"
    timestamp = datetime.datetime.now()
    resultsPath = "./Bloomberg" + "/" +str(timestamp)
    next_page = True
    current_page = 1
    #number_of_search_result = 0

    def __init__(self):
        
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless()
        #self.driver = webdriver.Firefox()
        #self.driver = webdriver.Chrome('chromedriver')
        self.driver = webdriver.Chrome(chrome_options=self.options)
        #self.driver = webdriver.Firefox(firefox_options=self.fireFoxOptions)
        self.driver.implicitly_wait(3)
        #driver = self.driver
        self.driver.get("https://www.bloomberg.com/search?query=germany&startTime=-1d&sort=time:desc&endTime=2019-01-30T21:31:38.818Z&page=")

        try:
            os.makedirs(self.resultsPath)
        except:
            print("Folder existed")

    def parse(self, response):

        driver = self.driver
        current_search_result_url = driver.current_url

        while (self.next_page):
        # next_page_url = self.base_url+ "&startat=" + str((current_page+1)*20)
        #     print("\nNext page url:%s\n" %next_page_url)
        #     driver.get(next_page_url)
        #     time.sleep(5)
        #     continue



        # driver.get()
        #time.sleep(5)
        
        # agree_and_close_button = driver.find_element_by_link_text("Agree and Close")
        
        # try:
        #     agree.click()
        #     time.sleep(2)
        # except:
        #     print("Luckliy no dynamic advertisement!")
        #Start to crawl on current page
            elements = driver.find_elements_by_class_name('search-result-story__headline')
            for elem in elements:
                article_url = elem.find_element_by_xpath(".//a").get_attribute("href")
                # agree_and_close_button = 
                # time.sleep(2)
                print("\nArticle link:%s\n" %article_url)
                #single_article_driver = webdriver.Firefox(firefox_options=self.fireFoxOptions)
                #single_article_driver = webdriver.Chrome(chrome_options=self.chromeOptions)
                single_article_driver = webdriver.Chrome(chrome_options=self.options)
                single_article_driver.get(article_url)
                
                try:
                    title = single_article_driver.find_element_by_css_selector('h1.lede-text-v2__hed').text
                    
                    content = single_article_driver.find_element_by_xpath(".//div[@class='body-copy-v2 fence-body']").text
                    #content=driver.find_elements_by_xpath(".//p")
                    print('title is:%s' %title)
                    print('content is:%s' %content)
                
                    yield {
                    'title':''.join(title),
                    'url':''.join(article_url),
                    'content': ''.join(content)
                    }
                    self.file_write(title, article_url, content)
                    single_article_driver.close()
                    continue
                except:
                    print("This is not reglar news! Maybe video!")
                    continue
        #driver.get(current_search_result_url)

        #Config next page url
            try:
                next_page = driver.find_element_by_class_name("content-next-link")
                self.next_page = True
                print("\nThere is next page!\n")
                self.current_page += 1
                next_page_url = self.base_url+ str(self.current_page)
                
                print("\nNext page url:%s\n" %next_page_url)
                
                driver.get(next_page_url)

                time.sleep(5)
                continue


            except:
                self.next_page = False
                print("\nNo more next page\n")

        #Config the next pages's url

        # if(next_page):
        #     print("inside next page function")
        #     next_page.click()
        #     yield response.follow(driver.current_url, callback=self.parse)
        
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