# import os
# import shutil
# from datetime import datetime

# def copy_images(src_path, base_dest_path):
#     # Generate a timestamped folder name
#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#     dest_folder_name = f"IMAGE_DIR_{timestamp}"

#     # Create the destination folder path
#     dest_path = os.path.join(base_dest_path, dest_folder_name)
#     os.makedirs(dest_path)

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
# base_dest_path = r"C:\Users\ELITEBOOK 1030\Desktop\MY_FIRST_JOB_NWES_SCRAPPER\All FILES"

# copy_images(src_path, base_dest_path)
import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib.parse  # For handling relative URLs

# URL of the news website
url = "https://www.pulse.ng/"
response = requests.get(url)
contents = response.content
soup = BeautifulSoup(contents, "html.parser")

def find_news_links(soup, category_keywords, min_links=0):
    # Find all 'a' (anchor) tags that might contain the news links
    news_links = soup.find_all("a")

    # Extract and return the links that contain any of the specified category keywords
    count = 0
    filtered_links = []
    for link in news_links:
        href = link.get("href")
        if href:
            # Convert relative URLs to absolute URLs
            full_url = urllib.parse.urljoin(url, href)
            
            if any(keyword in full_url for keyword in category_keywords):
                count += 1
                if count >= min_links:
                    filtered_links.append(full_url)

    return filtered_links

# Example usage
category_keywords = ["pulse.ng/lifestyle/", "pulse.ng/entertainment/","pulse.ng/"]
my_news_links = find_news_links(soup, category_keywords)
# Print the first 5 news links
print(my_news_links)

