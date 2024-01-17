import pandas as pd
import html5lib
from bs4 import BeautifulSoup
import os
import urllib.request
import re
import requests
import shutil #for directory
import datetime

# URL of the news website
url = "https://www.pulse.ng"
response = requests.get(url)
contents = response.content
soup = BeautifulSoup(contents, "html.parser")



def find_news_links(soup,category_keyword, min_links=20):
    # Find all 'a' (anchor) tags that might contain the news links
    News_links = soup.find_all("a")

    # Extract and return the links that contain the specified category keyword
    count = 0
    filtered_links = []
    for links in News_links:
        href = links.get("href")
        if  category_keyword in href:  # Filtering links that contain the category keyword
            count += 1
            if count <= min_links:
                filtered_links.append(href)

    return filtered_links

# specific news_link to parse 
category_keyword ="pulse.ng/news/" 
my_news_links = find_news_links(soup,category_keyword)
# Print the news links that will be scraped 
print(my_news_links)
    

def scrape_and_write_to_file(news_links):
    now = datetime.datetime.now()        #function to write current date and time 
    time = now.strftime("NEWS ACQUIRED ON  --> DATE: %Y-%m-%d    "+"TIME " "%H:%M ")

    for i, link in enumerate(news_links, start=1): #parse the news links and find the text in each link 
        news_link = requests.get(link).text
        LINK_SOUP = BeautifulSoup(news_link, 'html5lib')

        you1 = LINK_SOUP.h1.text.strip()
        Title1 = re.sub(r'[^\x00-\x7F]+', '', you1)

        you2 = LINK_SOUP.p.text
        Title2 = re.sub(r'[^\x00-\x7F]+', '', you2)

        you3 = LINK_SOUP.title.text
        Title3 = re.sub(r'[^\x00-\x7F]+', '', you3)

        you4 = LINK_SOUP.h2.text.strip()
        Title4 = re.sub(r'[^\x00-\x7F]+', '', you4)
        

        # Writing to a file for each news link
        with open(os.path.join(r'C:\Users\ELITEBOOK 1030\OneDrive\Desktop\MY_FIRST_JOB_NWES_SCRAPPER\All FILES\new_articles', f"NEWS{i}.txt"), 'a') as fw:
            fw.write("\n")
            fw.write(str(time).center(125)+"\n")
            fw.write("TITLE: " + Title1 + "\n")
            fw.write("HEADER1: " + Title2 + "\n")
            fw.write("LINK TITLE: " + Title3 + "\n")
            fw.write("HEADER 2: " + Title4 + "\n")
            fw.write("BODY:" + "\n")
            

            # Find all divs with class "article-body-text"
            boxes = LINK_SOUP.find_all("div", class_="article-body-text")
            body_written = False  # Flag to track if "BODY" has been written
            for box in boxes:
                paragraphs = box.find_all('p')
                for paragraph in paragraphs:
                    you = paragraph.get_text(strip=True)
                    Title5 = re.sub(r'[^\x00-\x7F]+', '', you) # enabling ASCII code 
                    fw.write("  " + Title5 + "\n")
               
            # print("\n")            

scrape_and_write_to_file(my_news_links)




# Downloading the images of every link 
def download_images(news_links, img_path, file_name):
    img = []
    
    for url in news_links:
        rest = requests.get(url).text
        r_soup = BeautifulSoup(rest, 'html5lib')
        img_tag = r_soup.find_all('img')
        category = "transform"
    
        for img_tags in img_tag:
            src = img_tags.get('src')
            if src and category in src:
                img.append(src)
    
    selected_images = img[0::4]    # getting the specific link to the images 
    print(selected_images)
    
    for i, image_url in enumerate(selected_images):
        try:
            # Generate a unique filename for each image
            image_filename = f"{file_name.split('.')[0]}_{i + 1}.{file_name.split('.')[1]}"
            
            # Combine the path and filename
            full_path = os.path.join(img_path, image_filename)
            
            # Download the image
            urllib.request.urlretrieve(image_url, full_path)
            print(f"Downloaded: {full_path}")
    
        except Exception as e:
            print(f"Error downloading {image_url}: {e}")


# Calling function

img_path = r"C:\Users\ELITEBOOK 1030\OneDrive\Desktop\MY_FIRST_JOB_NWES_SCRAPPER\All FILES\new_images"
file_name = "news_image.jpg"
download_images(my_news_links, img_path, file_name)

























# # moving images to a diffrerent directory 
# import os
# import shutil

# def copy_images(src_path, dest_path):
   
#     # Get a list of all files in the source directory
#     files = os.listdir(src_path)
    
#     # Iterate over each file and copy it to the destination directory
#     for file in files:
#         src_file = os.path.join(src_path, file)
#         dest_file = os.path.join(dest_path, file)
        
#         # Copy the file
#         shutil.move(src_file, dest_file)
#         print(f"MOVED: {dest_file}")

# # Example usage
# src_path = r"C:\Users\ELITEBOOK 1030\Desktop\MY_FIRST_JOB_NWES_SCRAPPER\All FILES\IMAGE_DIR"
# dest_path = r"C:\Users\ELITEBOOK 1030\Desktop\MY_FIRST_JOB_NWES_SCRAPPER\All FILES\IMAGE_DIR1"

# copy_images(src_path, dest_path)


    
