import os
import scrapy
from selenium import webdriver
import time
import datetime

## Crawling on Washington Post
class WPSpider(scrapy.Spider):
    name = "washingtonPostCrawler"
    start_urls = ['https://www.washingtonpost.com/newssearch/?datefilter=7%20Days&query=abu&sort=Date']
    base_url = 'https://www.washingtonpost.com/newssearch/?datefilter=7%20Days&query=abu&sort=Date'
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/google-chrome-unstable'
    options.add_argument('headless')#TBD
    options.add_argument('no-sandbox')
    options.add_argument('disable-gpu')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('window-size=1200x600')
    folder = "./WashingtonPost"
    timestamp = datetime.datetime.now()
    resultsPath = "./WashingtonPost" + "/" +str(timestamp)
    next_page = True
    number_pages = 1
    number_of_search_result = 0

    def __init__(self):
        
        
        #self.driver = webdriver.Firefox(firefox_options=self.fireFoxOptions)
        #self.driver = webdriver.Chrome('chromedriver',chrome_options=self.chromeOptions)
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver.implicitly_wait(3)
        self.driver.get(self.base_url)
        # Create folder and subfolder based on command execution timestamp 
        try:
            os.makedirs(self.resultsPath)
        except:
            print("Folder existed")

    def parse(self, response):
        # url_selector ='.pb-feed-headline ng-scope a ::attr("href")'
        # for article_url in response.css(url_selector).extract():
        #     yield response.follow(article_url, callback=self.parse_article)
        
        #driver = self.driver

        #Open the browser to below link
        #print("Top of parse")
        driver = self.driver
        #Deal with the anti-robot page by clicking buttons
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Sign in here'])[1]/following::button[1]").click()
        driver.find_element_by_id("agree").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='I agree'])[1]/following::button[1]").click()
        # Parse for number of search result and calculate number of pages
        self.number_of_search_result = int(driver.find_element_by_xpath(".//span[@class='pb-search-number ng-binding']").text)
        self.number_pages = int(self.number_of_search_result/20) + 1

        print("\nNumber of search result:%d\n"%self.number_of_search_result)
        print("\nNumber of pages:%d\n"%self.number_pages)

        for current_page in range(self.number_pages):
            #Now enter the search result page

            #Start to parse current page's article via links

            elements = driver.find_elements_by_css_selector('a.ng-binding')
            for elem in elements:
                article_url = elem.get_attribute("href")
                print("Article link:%s" %article_url)
                if(article_url != None and article_url != ""):
                    single_article_driver = webdriver.Chrome(chrome_options=self.options)
                    #single_article_driver = webdriver.Firefox(firefox_options=self.fireFoxOptions)
                    #single_article_driver = webdriver.Chrome('chromedriver',chrome_options=self.chromeOptions)
            
                    time.sleep(2)
                    
                    single_article_driver.get(article_url)
                    single_article_driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Sign in here'])[1]/following::button[1]").click()
                    single_article_driver.find_element_by_id("agree").click()
                    single_article_driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='I agree'])[1]/following::button[1]").click()
                    #time.sleep(4)
                    
                    
                    try:
                        
                        title_CSS_SELECTOR = 'div.topper-headline'
                        content_xpath = ".//article[@class='paywall']"
                        #driver.refresh()

                        title = single_article_driver.find_element_by_css_selector(title_CSS_SELECTOR).text
                        
                        content = single_article_driver.find_element_by_xpath(content_xpath).text
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
                        #driver.back()
                        single_article_driver.close()
                        print("This is in except!")
                        continue

            #Config the next pages's url 

            next_page_url = self.base_url+ "&startat=" + str((current_page+1)*20)
            print("\nNext page url:%s\n" %next_page_url)
            driver.get(next_page_url)
            time.sleep(5)
            continue


        #while (self.next_page):
            
            

           
            
            #current_search_result_url = driver.current_url
            #print("Current search result url: %s" %current_search_result_url)

            #driver.get(current_search_result_url)
            # elements = driver.find_elements_by_css_selector('a.ng-binding')
            # for elem in elements:
            #     article_url = elem.get_attribute("href")
            #     print("Article link:%s" %article_url)
            #     if(article_url != None):
            #         #single_article_driver = webdriver.Firefox()
            #         single_article_driver = webdriver.Firefox(firefox_options=self.fireFoxOptions)
                
            #         time.sleep(2)
                    
            #         single_article_driver.get(article_url)
            #         single_article_driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Sign in here'])[1]/following::button[1]").click()
            #         single_article_driver.find_element_by_id("agree").click()
            #         single_article_driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='I agree'])[1]/following::button[1]").click()
            #         #time.sleep(4)
                    
                    
            #         try:
                        
            #             title_CSS_SELECTOR = 'div.topper-headline'
            #             content_xpath = ".//article[@class='paywall']"
            #             #driver.refresh()

            #             title = single_article_driver.find_element_by_css_selector(title_CSS_SELECTOR).text
                        
            #             content = single_article_driver.find_element_by_xpath(content_xpath).text
            #             #content=driver.find_elements_by_xpath(".//p")
            #             print('title is:%s' %title)
            #             print('content is:%s' %content)
                    
            #             yield {
            #             'title':''.join(title),
            #             'url':''.join(article_url),
            #             'content': ''.join(content)
            #             }
            #             single_article_driver.close()
            #             continue
            #         except:
            #             #driver.back()
            #             single_article_driver.close()
            #             print("This is in except!")
            #             continue

            #driver.get(current_search_result_url)
            

            #Check whether there is next page
            # try:
            #         #if(driver.find_element_by_xpath(".//li[@ng-if='::directionLinks']")):
            #         self.next_page = True
            #         self.number_search_result_page+=1
                    
            #         next_page_url = self.base_url+ "&startat=" + str((self.number_search_result_page-1)*20)
            #         #print("Next page url:%s" %next_page_url)
            #         driver.get(next_page_url)
            #         time.sleep(5)

            # except:
            #     current_search_result_url = driver.current_url
            #     print("Current search result url: %s" %current_search_result_url)
            #     print("#############Only %d of search result pages" %self.number_search_result_page)
            #     self.next_page = False
            #     break
            

            # if(next_page):
            #     print("############inside next page function")
            #     next_page.click()
            #     time.sleep(5)
            #     yield response.follow(driver.current_url, callback=self.parse)
                
            
            #for article_url in driver.find_elements_by_xpath(".//div[@class='search-result-story__headline']"):
            # for article_url in response.css('.search-result-story__headline a ::attr("href")').extract():
        driver.close()


    def parse_article(self, response):
        content = response.xpath(".//article[@itemprop='articleBody']/descendant::text()").extract()
        yield {'article': ''.join(content)}

    def file_write(self, title, url, content):
        #print("######################file method inside######################")
        fileName = str(title) + ".txt"
            
        file = open(self.resultsPath + "/" +fileName, "w")
        # Write titile, URL, content into the file
        file.write(str(title) + "\n")
        file.write(str(url) + "\n")
        file.write(str(content))
        file.close()