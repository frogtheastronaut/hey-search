import requests
import json
import time
import sys
from bs4 import BeautifulSoup # type: ignore
import re

# known websites that have not yet been crawled through
known_websites = []
known_website_data = []

# websites crawler has checked
checked_websites = []
failed_url_requests = []
crawls = 0
last_url_requested = ""

KNOWN_WEBSITE_SCHEMES = (
    "https://",
    "http://"
)

STATUS_CODE_PASS = [
    200,
    201,
    202,
    203,
    204,
    205,
    206,
    207,
    208,
    226,
    300,
    301,
    302,
    303,
    304,
    305,
    306,
    307,
    308,
    100,
    101,
    102,
    103
]

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Crawler:
    def __init__(self):
        global known_website_data
        global checked_websites
        global known_websites
        # init vars
        self.repeats = 0
        self.read_database()
        self.website_keywords = ""

    def read_json(self, filename='crawlres.json'):
        with open(filename, 'r') as file:
            return json.load(file)

    def write_json(self, new_data, filename='crawlres.json'):
        with open(filename, "w") as outfile:
            json.dump(new_data, outfile, indent=4)
    def get_site_info(self, url):
        global crawls
        global known_websites
        global last_url_requested
        if url in checked_websites or url in failed_url_requests:
            print(Colors.BOLD + Colors.WARNING + f"{url} already checked" + Colors.ENDC)
            if crawls == 0:
                print("db seems to have data. crawling last...")
                self.get_site_info(known_websites[-1])
            return 0
        links_in_site = []
        try:
            # get the site info
            print(f"getting url {url}...")
            last_url_requested = url
            request = requests.get(url)
            print(Colors.OKBLUE + "url recieved" + Colors.ENDC)
            soup = BeautifulSoup(request.text, 'html.parser')
            for link in soup.find_all('a'):
                links_in_site.append(link.get('href'))  
            #print(f"{url} links recieved")
            for link2 in links_in_site:
                # link2 has nothing in it
                if link2 == None or len(link2) == 0:
                    pass
                else:
                    if link2.startswith(KNOWN_WEBSITE_SCHEMES):
                        # starts with eg. https://
                        real_link = link2
                    else:
                        # eg. /google/website instead of google.com/google/website
                        real_link = url + link2
                    if real_link in checked_websites or real_link in known_websites or real_link in failed_url_requests:
                        print(Colors.BOLD + real_link + Colors.WARNING + " already checked. skipping..." + Colors.ENDC)
                        pass
                    else:
                        # request real link
                        print(f"requesting found link: {real_link}")
                        last_url_requested = real_link
                        href_request = requests.get(real_link)
                        if href_request.status_code in STATUS_CODE_PASS:
                            print(Colors.OKBLUE + "request success" + Colors.ENDC)
                            sub_soup = BeautifulSoup(href_request.text, 'html.parser')
                            known_websites.append(real_link)
                            og = self.get_og(sub_soup)
                            keywords = self.get_site_keywords(real_link, og['site'], og['title'], og['desc'], og['site_content'])
                            known_website_data.append(
                                [real_link, keywords]
                            )
                        else:
                            print(Colors.FAIL + "request failed" + Colors.ENDC)
                            failed_url_requests.append(real_link)
            checked_websites.append(url)
            self.write_json(
                {
                    "site_known": known_websites,
                    "site_known_data": known_website_data,
                    "site_checked": checked_websites,
                }
            )
            self.repeats = 0
            return links_in_site
        except requests.exceptions.ConnectionError:
            if self.repeats > 3:
                print(Colors.FAIL + "retries exceeded. breaking." + Colors.ENDC)
                failed_url_requests.append(last_url_requested)
                self.repeats = 0
            else:
                print(Colors.WARNING + "connection failed. sleeping..." + Colors.WARNING)
                time.sleep(1)
                print(Colors.WARNING +"reconnecting to last url..." + Colors.WARNING)
                self.repeats += 1
                self.get_site_info(last_url_requested)
    def get_og(self, soup):
        # gets the open graph meta information of a soup
        title = soup.find("meta",  property="og:title")
        desc = soup.find("meta",  property="og:description")
        site = soup.find("meta",  property="og:site_name")
        return {
            "site": None if site == None or 'content' not in site else site['content'],
            "title":  None if title == None or 'content' not in title else title['content'],
            "desc":  None if desc == None or 'content' not in desc else desc['content'],
            "site_content": self.get_site_content(soup)
        }
    def get_site_content(self, soup):
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        return soup.get_text(separator=' ', strip=True)
    def read_database(self):
        global known_website_data
        global known_websites
        global checked_websites
        try:
            json_data = self.read_json()
            known_website_data = json_data["site_known_data"]
            known_websites = json_data["site_known"]
            checked_websites = json_data["site_checked"]
        except:
            print(Colors.WARNING + "warning: json file has not valuable information" + Colors.ENDC)
    def get_site_keywords(self, url, site, title, desc, site_content):
        website_keywords = ""
        keywords_list = []
        keywords_processed = []
        processed_str = ""
        assert url != None
        website_keywords += f"{url} " # add url
        if site != None:
            website_keywords += f"{site} "
        if title != None:
            website_keywords += f"{title} "
        if desc != None:
            website_keywords += f"{desc} "
        if site_content != None:
            website_keywords += f"{site_content} "
        keywords_list = website_keywords.split()
        for word in keywords_list:
            if word not in keywords_processed:
                keywords_processed.append(word)
        processed_str = ' '.join(keywords_processed)
        return processed_str

class CrawlBot:
    def __init__(self):
        self.crawler = Crawler()
        pass
    def crawl(self):
        global crawls
        print(Colors.HEADER + "initiating crawl.." + Colors.ENDC)
        for website in known_websites:
            print(f"crawling {website}")
            self.crawler.get_site_info(website)
            crawls += 1
            

if __name__ == "__main__":
    known_websites = [sys.argv[1]]
    crawlbot = CrawlBot()
    crawlbot.crawl()


