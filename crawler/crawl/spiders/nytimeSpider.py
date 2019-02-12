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
    # folder = "./New York Times"
    # timestamp = datetime.datetime.now()
    # resultsPath = str(folder) + "/" +str(timestamp)

    def __init__(self):
        
        #Initialize the spider
        self.driver = webdriver.Chrome(chrome_options=self.options)

        # Get the projectID and parsed request for this spider
        with open('/tmp/project_request.json') as f:
            data = json.load(f)
        self.projectID = data['projectID']
        self.request_url = data['query_url']['NYT']
        self.timestamp = data['timestamp']
        self.logger.info('\nprojectID= %s\n', self.projectID)
        self.logger.info('\nrequest_url= %s\n', self.request_url)
        self.logger.info('\ntimestamp= %s\n', self.timestamp)

        # Finalize the path for store files
        self.folder = "/data/projects/"+ self.projectID
        self.resultsPath = str(str(self.folder) + "/crawler" + "/NYT" + "/" + self.timestamp)
        self.logger.info('\n Resultpath= %s\n', self.resultsPath)
        
        self.driver.implicitly_wait(3)
        if not os.path.exists(self.resultsPath):
            try:
                os.makedirs(self.resultsPath)
            except Exception as ee:
                print(str(ee))

        # #self.driver = webdriver.Firefox(firefox_options=self.fireFoxOptions)
        # self.driver = webdriver.Chrome(chrome_options=self.options)
        # #self.driver = webdriver.Firefox()
        # #self.driver = webdriver.Chrome('chromedriver')
        # self.driver.implicitly_wait(3)
        # self.driver.get("https://www.nytimes.com/search?endDate=20190107&query=china&sort=newest&startDate=20190104")
        # #print('Now init function finished')
        # try:
        #     os.makedirs(self.resultsPath)
        # except:
        #     print("Folder existed")

    def parse(self, response):
        #self.driver.get(response.url)
        driver = self.driver
        driver.get(self.request_url)
        #i = 0
        
        # Click load more button until it can't 
        while True:
            #self.driver.find_element_by_xpath('//div[@class="pages-select"]/a[contains(text(), "Next")]').click()
            #more = self.driver.find_element_by_xpath('//div[@class="css-1t62hi8"]/a')
            try:
                driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Have search feedback? Let us know what you think.'])[1]/following::button[1]").click()
                time.sleep(5)
                
            except:
                break 

        elements = driver.find_elements_by_class_name('css-138we14')
        #print("url links:%s" %url_links)
        for elem in elements:
            article_url = elem.find_element_by_xpath(".//a").get_attribute("href")
            print("NYT Article URL:%s" %article_url) 
            time.sleep(1)

            single_article_driver = webdriver.Chrome(chrome_options=self.options)
            single_article_driver.get(article_url)
                   
            #title = response.xpath(".//h1[@itemprop='headline']/descendant::text()").extract()
            #content = response.xpath(".//section[@name='articleBody']/descendant::text()").extract()
            try:
                title = single_article_driver.find_element_by_xpath(".//h1[@itemprop='headline']").text
                content = single_article_driver.find_element_by_xpath(".//section[@name='articleBody']").text
            
                current_article = {
                        'title':title,
                        'source': 'New York Times',
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
        # for article_url in response.css('.css-138we14 a ::attr("href")').extract():   
        #         yield response.follow(article_url, callback=self.parse_article)

    def file_write(self, article):
        
        fileName = str(article['title']) + ".json"
        with open(self.resultsPath + "/" +fileName, "w") as outfile:
            json.dump(article, outfile)