from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import logging
import pandas as pd
import csv
import chardet
import threading
import urllib3

http = urllib3.PoolManager(num_pools=10, maxsize=10, retries=3)

logging.basicConfig(filename='You_Tube.log',level=logging.CRITICAL)

app = Flask(__name__)

@cross_origin()
@app.route("/")
def youtube_data():
    try:
        
        chrome_option = Options()
        chrome_option.add_argument('--disable-extensions')
        chrome_option.add_argument('--diable-infobars')
        chrome_option.headless = True


        driver = webdriver.Chrome(options=chrome_option)
        driver.maximize_window()
        try:
           URL = "https://www.youtube.com/@PW-Foundation/videos"
           driver.get(URL)
        except Exception as e:
           logging.error(e,'There is error in getting URL')
        else:
           logging.info('Sucessfully accessed ' ,URL)
        
        time.sleep(2)

        all_video_URL = driver.find_elements(By.XPATH, '//*[@id="video-title-link"]')
        all_thumbnail_URl = driver.find_elements(By.XPATH, '//*[@id="thumbnail"]/yt-image/img')
        all_video_title = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
        all_video_number_of_views = driver.find_elements(By.XPATH , '//*[@id="metadata-line"]/span[1]')
        all_video_time_of_posting = driver.find_elements(By.XPATH,'//*[@id="metadata-line"]/span[2]')

        video_URL_list = []
        thumbnail_URL_list = []
        video_title = []
        number_of_views = []
        time_of_posting = []
        
        YouTube_Data = pd.DataFrame({})
        def get_video_url():
            for element in all_video_URL:
                try:
                   element.get_attribute('href')
                   
                except Exception as e:
                   logging.error(e,"There is issue in getting video URL")

                else:
                   video_URL_list.append(element.get_attribute('href'))
            
            first_five_video_URL = video_URL_list[:5]
            logging.info("List of first five video URLS")
            logging.info(first_five_video_URL)
            YouTube_Data['Video URL'] = first_five_video_URL
            


        def get_thumbnail_url():
           driver.execute_script("window.scrollBy(0, 500)")
           logging.info('Window scrolled up by 500 px')
           for element in all_thumbnail_URl:
               try:
                  element.get_attribute('src')
               except Exception as e:
                  logging.error(e, "There is issue in getting thumnail URL")
               else:
                  thumbnail_URL_list.append(element.get_attribute('src'))
                  
      
           first_five_thumbnail_URL = thumbnail_URL_list[:5]
           logging.info("List of first five thumbnail URLS")
           logging.info(first_five_thumbnail_URL)
           YouTube_Data['Thumbnail URL'] = first_five_thumbnail_URL
           

        def get_video_title():
            for element in all_video_title:
               try:
                  element.text
               except Exception as e:
                  logging.error(e,'There is issue in getting video title')
               else:
                  video_title.append(element.text)
            first_five_video_title = video_title[:5]
            logging.info("List of first five video titles")
            logging.info(first_five_video_title)
            YouTube_Data['Title of videos'] =first_five_video_title

        def get_number_of_views():
            for element in all_video_number_of_views:
                try:
                   element.text
                except Exception as e:
                   logging.error(e, "There is an issue in getting number of views")
                else:
                  number_of_views.append(element.text)
            number_of_views_first_five_video = number_of_views[:5]
            logging.info(number_of_views_first_five_video)
            logging.info("List of number of views on firt five video ")
            YouTube_Data['Number of view'] = number_of_views_first_five_video

        def get_posting_time():
            for element in all_video_time_of_posting:
                try:
                   element.text
                except Exception as e:
                   logging.error(e, "There is an issue in getting posting time")
                else:
                   time_of_posting.append(element.text)
            posting_time_first_five_videos = time_of_posting[:5]
            logging.info("List of posting time of  first five videos")
            logging.info(posting_time_first_five_videos)
            YouTube_Data['Time of posting the video'] = posting_time_first_five_videos
        
        


        


        t1 = threading.Thread(target=get_video_url)
        t2 = threading.Thread(target=get_thumbnail_url)
        t3 = threading.Thread(target=get_video_title)
        t4 = threading.Thread(target=get_number_of_views)
        t5 = threading.Thread(target=get_posting_time)
       


        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        


        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        
        
        
    
    except Exception as e:
           print(e,"Something Went Wrong")
           logging.error(e)
    
    else:
        
        YouTube_Data.to_csv('YouTube_data.csv')
        logging.info("The data is saved in CSV format")
        
        
        data = []
    
        with open("YouTube_Data.csv", 'rb') as f:
           result = chardet.detect(f.read())
           encoding = result['encoding']
        try:
            with open("YouTube_Data.csv", "r" , encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                   data.append(row)
        except Exception as e:
           logging.error(e,"There is isue in encoding the test")
        
        

        
        
        driver.quit()
    

    return render_template("Result_Page.html" , data = data)

logging.shutdown()

if __name__=="__main__":
    app.run(host="0.0.0.0")   