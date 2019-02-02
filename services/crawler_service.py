import os
from config.config import FOLDER
from services.pipeline_service import handle_crawler_folder

def execute_crawler(request,projectUUID):
    if not os.path.exists(FOLDER + projectUUID):
            os.makedirs(FOLDER + projectUUID)
    
    REUTERS_Path = "/data/projects/" + projectUUID + "/crawler" + "/Reuters"
    # filename = secure_filename(file.filename)
    # file_path = os.path.join(FOLDER + projectUUID, filename)
    # file.save(file_path)
    # cwd_enter = os.getcwd()
    # os.system(print("\nEnter the execute_crawler:%s\n"%cwd_enter))
    # try:
    #     os.mkdir("test")
    # except Exception as ee:
    #     print(str(ee))

    # try:
    #     file_write(request['query'], request['source'], request['period'])
    # except Exception as ee:
    #     print(str(ee))
    crawler_folder_path = ('/usr/src/app/crawler')
    #之後這裡要放入修改query的function




    #執行對應的爬蟲
    execute_crawler_cmd = ('scrapy crawl reutersCrawler -a projectID=%s' %projectUUID)
    # after_write = os.getcwd()
    # os.system(print("\nafter file write:%s\n"%cwd_enter))
    # os.getcwd()
    os.chdir(crawler_folder_path)
    
    os.system(execute_crawler_cmd)
    handle_crawler_folder(projectUUID,REUTERS_Path) 
    
def file_write(query, period, source):
        #print("######################file method inside######################")
        fileName = str(query) + ".txt"
            
        file = open("test/" +fileName, "w")
        # Write titile, URL, content into the file
        file.write(str(query) + "\n")
        file.write(str(period) + "\n")
        file.write(str(source))
        file.close()