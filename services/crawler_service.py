import os
import datetime
from config.config import FOLDER
from services.pipeline_service import handle_crawler_folder
import logging
import json

def parse_request(projectID, timestamp,request):
    query = request['query']
    source = request['source']
    period = request['period']

    query_url = {
        "Reuters":"",
        "NYT":"",
        "Bloomberg":"",
        "WP":""
    }
    #Since every website have different query format, then it need to customize
    #Reuters query
    if(period == "Past Day"):
        Reuters_period = "pastDay"
    elif(period == "Past Week"):
        Reuters_period = "pastWeek"
    else:
        Reuters_period = "pastMonth"        

    query_url["Reuters"] = 'https://www.reuters.com/search/news?sortBy=date&dateRange='+ Reuters_period +'&blob='+ query
    logging.debug("\nquery:%s\n" %query_url["Reuters"])
    
    # Will append other source's schema here

    #Store into .json file for later use
    data = {
        'projectID':projectID,
        'timestamp': str(timestamp),
        'Reuters_query_url':query_url['Reuters']
    }
    with open("/tmp" + "/project_request.json", "w") as outfile:
        json.dump(data, outfile)

def execute_crawler(request,projectUUID):
    logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename='/tmp/test.log',  
                    filemode='w')  
    
    if not os.path.exists(FOLDER + projectUUID):
            os.makedirs(FOLDER + projectUUID)
    timestamp =  datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    REUTERS_Path = "/data/projects/" + projectUUID + "/crawler" + "/Reuters" + "/" + str(timestamp)
    logging.debug("\nReuters_path:%s\n" %REUTERS_Path)
    crawler_folder_path = ('/usr/src/app/crawler')
    

    # Parse the request and store into file for crawler 
    parse_request(projectUUID, timestamp, request)
    #logging.debug("\nInside the execute crawl funciton parsed_query_url:%s\n" %parsed_query_url["Reuters"])
   
    execute_reuters_crawler_cmd = ('scrapy crawl reutersCrawler')
    #logging.debug(execute_reuters_crawler_cmd)
    os.chdir(crawler_folder_path)
    #Check which crawler should execute
    if("Reuters" in request['source']):
        os.system(execute_reuters_crawler_cmd)
        #logging.debug("\nRetuers is selected, Reuters_path:%s\n" %REUTERS_Path)
        handle_crawler_folder(projectUUID,REUTERS_Path)

    # Remove the parsed request file
    remove_project_request_file_cmd = ('rm -f /tmp/project_request.json')
    os.system(remove_project_request_file_cmd)

def stop_crawler():
    # This will stop  multiple crawlers on this server
    stop_crawler_cmd = ('ps -A | grep scrapy | awk \'{print $1}\' | xargs kill -9 $1')
    os.system(stop_crawler_cmd)
    stop_chomedriver_cmd = ('ps -A | grep chrome | awk \'{print $1}\' | xargs kill -9 $1')
    os.system(stop_chomedriver_cmd)