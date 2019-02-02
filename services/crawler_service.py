import os

def execute_crawler(request):
    try:
        os.makedirs("./test")
    except:
        print("Folder existed")

    file_write(request['query'], request['source'], request['period'])
    crawler_folder_path = ('/usr/src/app/crawler')
    execute_crawler_cmd = ('scrapy crawl reutersCrawler')
    #print(os.getcwd())

    os.chdir(crawler_folder_path)
    os.system(execute_crawler_cmd)
    
    
def file_write(query, period, source):
        #print("######################file method inside######################")
        fileName = str(query) + ".txt"
            
        file = open("./test/" +fileName, "w")
        # Write titile, URL, content into the file
        file.write(str(query) + "\n")
        file.write(str(period) + "\n")
        file.write(str(source))
        file.close()