from selenium import webdriver
import chromedriver_autoinstaller
import pandas as pd
from fuzzywuzzy import fuzz
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from keys import url
from amazon_affiliate_generator import convert_to_affiliate_link


chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path



def amazonQuery(query = "kitchen accessories"):
    try:
        driver = webdriver.Chrome() 
        split_text = query.split()
        split_text.insert(0, "tiktok")
        url_section = '+'.join(split_text)

        new_url = url.replace("kitchen+accessories", url_section)
        driver = webdriver.Chrome()
        driver.get(new_url)
        elements = driver.find_elements_by_class_name('a-size-mini.a-spacing-none.a-color-base.s-line-clamp-4')

        # Print the text content of each element
        elements = driver.find_elements_by_class_name('a-size-mini.a-spacing-none.a-color-base.s-line-clamp-4')

        # Store the results in an array
        results = []

        # Process each element
        for element in elements:
            text = element.find_element_by_tag_name('span').text
            href = element.find_element_by_tag_name('a').get_attribute('href')
            results.append((text, href))

        # Print the results
        for result in results:
            print(f"Text: {result[0]}")
            print(f"Href: {result[1]}")
            print()

        # Close the browser
        driver.quit()

        return results
    except Exception as e:
        print("Issue with amazon query")
        return "failed"

def youtube_results(results):
    
    driver = webdriver.Chrome()
    driver.get('https://www.youtube.com')
    results_dict = {}
    try:
        for result in tqdm(results, desc="Processing results"):
            try:
                video_title = result[0][:50]  # Retrieve the first 50 characters of the title
                amazon_product_link = result[1]

                if not video_title:
                    print("Skipping result with no title.")
                    continue

                # Find the search box and enter the video title
                search_box = driver.find_element_by_name('search_query')
                search_box.clear()
                search_box.send_keys(video_title + "  #shorts")
                search_box.submit()

                # Wait for the search results to load
                driver.implicitly_wait(5)  # Adjust the wait time as needed

                # Find all video elements
                video_elements = driver.find_elements_by_css_selector('ytd-video-renderer')

                # Check if there are search results
                if len(video_elements) == 0:
                    print("No search results found for title:", video_title)
                    continue

                # Process each video element
                for video_element in video_elements:
                    video_url = video_element.find_element_by_css_selector('#video-title').get_attribute('href')
                    video_title = video_element.find_element_by_css_selector('#video-title').text

                    # Check if the URL contains the word "shorts"
                    if "shorts" not in video_url.lower():
                        continue

                    # Calculate similarity between video title and result title
                    similarity_ratio = fuzz.token_set_ratio(result[0], video_title)

                    # Specify a threshold for similarity ratio (adjust as needed)
                    if similarity_ratio >= 70:
                        # Skip if the video title is already present in the results_dict
                        if any(result[0] == entry['Title'] for entry in results_dict.values()):
                            continue

                        # Skip if the video URL is already present in the results_dict
                        if video_url in results_dict:
                            continue

                        # Store the information in the results_dict
                        results_dict[video_url] = {
                            'Title': result[0],
                            'Amazon Product Link': convert_to_affiliate_link(amazon_product_link),
                            'YouTube Link': video_url
                        }
            except Exception as e:
                print("Oppsie with video")

        # Print the results
        for url, info in results_dict.items():
            print("Title:", info['Title'])
            print("Amazon Product Link:", info['Amazon Product Link'])
            print("YouTube Link:", info['YouTube Link'])
            print()

        # Close the browser
        driver.quit()

        return results_dict
    except Exception as e:
        print("Issue with youtube query")
        return "failed"
