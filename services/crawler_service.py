import os
import datetime
from config.config import FOLDER, ROOT_FOLDER
from services.pipeline_service import handle_crawler_folder
import logging
import json

def parse_request(projectID, timestamp, request):
    query = request['query']
    source = request['source']
    period = request['period']

    query_url = {
        "Reuters":"",
        "NYT":"",
        "Bloomberg":"",
        "WP":""
    }
    if('Reuters' in source):
        query_url["Reuters"] = parsed_Reuters_query(query, period)
    elif('New York Times' in source):
        query_url["NYT"] = parsed_NYT_query(query, period)
    #Since every website have different query format, then it need to customize
    # #Reuters query
    # if(period == "Past Day"):
    #     Reuters_period = "pastDay"
    # elif(period == "Past Week"):
    #     Reuters_period = "pastWeek"
    # else:
    #     Reuters_period = "pastMonth"

    # query_url["Reuters"] = 'https://www.reuters.com/search/news?sortBy=date&dateRange='+ Reuters_period +'&blob='+ query
    # logging.debug("\nquery:%s\n" %query_url["Reuters"])

    # # Will append other source's schema here

    #Store into .json file for later use
    data = {
        'projectID':projectID,
        'timestamp': str(timestamp),
        'query_url':query_url
    }
    with open(FOLDER + "tmp/project_request.json", "w") as outfile:
        print("WRITE TMP")
        json.dump(data, outfile)


def parsed_NYT_query(query, period):
    #New York Times query
    end_date = datetime.datetime.now().strftime("%Y%m%d")
    if(period == "Past Day"):
        start_date = (datetime.datetime.now() + datetime.timedelta(-1)).strftime("%Y%m%d")
    elif(period == "Past Week"):
        start_date = (datetime.datetime.now() + datetime.timedelta(-7)).strftime("%Y%m%d")
    else:
        start_date = (datetime.datetime.now() + datetime.timedelta(-30)).strftime("%Y%m%d")

    url = 'https://www.nytimes.com/search?sort=newest&startDate='+ start_date +'&endDate='+ end_date +'&query=' + query
    logging.debug("\nquery:%s\n" % url)

    return url

def parsed_Reuters_query(query, period):
    #Reuters query
    if(period == "Past Day"):
        Reuters_period = "pastDay"
    elif(period == "Past Week"):
        Reuters_period = "pastWeek"
    else:
        Reuters_period = "pastMonth"        

    url = 'https://www.reuters.com/search/news?sortBy=date&dateRange='+ Reuters_period +'&blob='+ query
    logging.debug("\nquery:%s\n" %url)

    return url
    
    # Will append other source's schema here

    #Store into .json file for later use
    # data = {
    #     'projectID':projectID,
    #     'timestamp': str(timestamp),
    #     'Reuters_query_url':query_url['Reuters']
    # }


def execute_crawler(request,project_uuid):
    logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename='/tmp/test.log',  
                    filemode='w')  
    
    if not os.path.exists(FOLDER + project_uuid):
            os.makedirs(FOLDER + project_uuid)
    timestamp =  datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    REUTERS_Path = FOLDER + project_uuid + "/crawler" + "/Reuters" + "/" + str(timestamp)
    NYT_Path = FOLDER + project_uuid + "/crawler" + "/NYT" + "/" + str(timestamp)
    logging.debug("\nReuters_path:%s\n" %REUTERS_Path)
    crawler_folder_path = (ROOT_FOLDER + "crawler")
    

    # Parse the request and store into file for crawler 
    parse_request(project_uuid, timestamp, request)
    logging.debug("\nInside the execute crawl funciton parsed_query_url:%s\n")
   
    execute_reuters_crawler_cmd = ('scrapy crawl reutersCrawler')
    execute_nyt_crawler_cmd = ('scrapy crawl nytCrawler')
    logging.debug(execute_reuters_crawler_cmd)
    os.chdir(crawler_folder_path)
    #Check which crawler should execute
    if("Reuters" in request['source']):
        os.system(execute_reuters_crawler_cmd)
        logging.debug("\nRetuers is selected, Reuters_path:%s\n" %REUTERS_Path)
        handle_crawler_folder(project_uuid,REUTERS_Path)
    if("New York Times" in request['source']):
        os.system(execute_nyt_crawler_cmd)
        logging.debug("\nRetuers is selected, Reuters_path:%s\n" %REUTERS_Path)
        handle_crawler_folder(project_uuid,NYT_Path)

    # Remove the parsed request file
    remove_project_request_file_cmd = ('rm -f '+FOLDER+'tmp/project_request.json')
    os.system(remove_project_request_file_cmd)

def stop_crawler():
    # This will stop  multiple crawlers on this server
    stop_crawler_cmd = ('ps -A | grep scrapy | awk \'{print $1}\' | xargs kill -9 $1')
    os.system(stop_crawler_cmd)
    stop_chomedriver_cmd = ('ps -A | grep chrome | awk \'{print $1}\' | xargs kill -9 $1')
    os.system(stop_chomedriver_cmd)

