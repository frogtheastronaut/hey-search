import requests
import json
import time
import sys, os
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time
import random
import threading


known_websites = set()
known_website_data = {} 
checking_websites = set()
checked_websites = set()
failed_url_requests = set()
crawls = 0
last_url_requested = ""
stop = False # whether the crawler should stop

# website locks
websites_lock = threading.Lock()
data_lock = threading.Lock()
crawls_lock = threading.Lock()

KNOWN_WEBSITE_SCHEMES = (
    "https://",
    "http://"
)
KNOWN_WEBSITE_DOMAINS = (
    "com",
    "org",
    "net",
    "edu",
    "gov",
    "mil",
    "int",

    "io",
    "co",
)

STATUS_CODE_PASS = [
    200, 201, 202, 203, 204, 205, 206, 207, 208, 226,
    300, 301, 302, 303, 304, 305, 306, 307, 308,
    100, 101, 102, 103
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
        self.website_keywords = ""
        self.cwd = os.getcwd()
        self.read_database()

    def read_json(self, filename='crawlres.json'):
        filepath = os.path.join(self.cwd, filename)
        print(f"reading JSON from: {filepath}")
        
        with open(filepath, 'r') as file:
            res = json.load(file)
            # print first 2 items
            if 'site_known' in res and len(res['site_known']) > 0:
                print(f"first entries: {list(res['site_known'])[:2]}")
            return res

    def write_json(self, filename='crawlres.json'):
        with websites_lock:
            sites_known = list(known_websites)
            sites_checked = list(checked_websites)
        
        with data_lock:
            sites_data = known_website_data.copy()
        
        data = {
            "site_known": sites_known,
            "site_known_data": sites_data,
            "site_checked": sites_checked,
        }
        
        with open(f"{self.cwd}/{filename}", "w") as outfile:
            json.dump(data, outfile, indent=4)
        print(Colors.OKGREEN + f"wrote to {self.cwd}/{filename}" + Colors.ENDC)

    def get_site_info(self, url):
        if stop == True:
            print(Colors.OKCYAN + "stopping crawler bot..." + Colors.ENDC)
            return
        global crawls, known_websites, last_url_requested
        # process URL first
        url = self.process_url(url)
        
        with websites_lock:
            if url in checked_websites or url in failed_url_requests:
                print(Colors.BOLD + Colors.WARNING + f"{url} already checked ##" + Colors.ENDC)
                return 0
            
            if url in checking_websites:
                print(Colors.WARNING + f"already checking {url}, skipping..." + Colors.ENDC)
                return
            
            checking_websites.add(url)

        links_in_site = []
        try:
            print(f"getting url {url}...")
            last_url_requested = url
            request = requests.get(url, timeout=10)
            print(Colors.OKBLUE + "url received" + Colors.ENDC)
            
            soup = BeautifulSoup(request.text, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    links_in_site.append(href)
            
            for link2 in links_in_site:
                if stop == True:
                    print(Colors.OKCYAN + "stopping crawler bot..." + Colors.ENDC)
                    return
                if link2 == None or len(link2) == 0:
                    continue
                
                if link2.startswith(KNOWN_WEBSITE_SCHEMES):
                    real_link = link2
                else:
                    real_link = url + link2
                real_link = self.process_url(real_link)
                
                with websites_lock:
                    if real_link in checked_websites or real_link in known_websites or real_link in failed_url_requests:
                        print(Colors.BOLD + real_link + Colors.WARNING + " already checked. skipping..." + Colors.ENDC)
                        continue
                    
                    if real_link in checking_websites:
                        print(Colors.WARNING + f"already checking {real_link}, skipping.." + Colors.ENDC)
                        continue
                    
                    checking_websites.add(real_link)
                
                try:
                    print(f"requesting found link")
                    last_url_requested = real_link
                    href_request = requests.get(real_link, timeout=5)
                    
                    if href_request.status_code in STATUS_CODE_PASS:
                        print(Colors.OKBLUE + f"request success: {real_link}" + Colors.ENDC)
                        sub_soup = BeautifulSoup(href_request.text, 'html.parser')
                        
                        with websites_lock:
                            known_websites.add(real_link)
                            checking_websites.discard(real_link)
                        # these are the keywords we want to extract
                        og = self.get_og(sub_soup)
                        keywords = self.get_site_keywords(self.get_url_keywords(real_link), og['site'], og['title'], og['desc'], og['site_content'])

                        with data_lock:
                            # put the keywords into known_website_data
                            known_website_data[real_link] = keywords
                    else:
                        print(Colors.FAIL + f"request failed: {real_link}" + Colors.ENDC)
                        with websites_lock:
                            failed_url_requests.add(real_link)
                            checking_websites.discard(real_link)
                            
                except Exception:
                    with websites_lock:
                        failed_url_requests.add(real_link)
                        checking_websites.discard(real_link)
            
            with websites_lock:
                checked_websites.add(url)
                checking_websites.discard(url)
            
            self.repeats = 0
            return links_in_site
            
        except Exception as e:
            with websites_lock:
                checking_websites.discard(url)
            
            if isinstance(e, requests.exceptions.ConnectionError):
                print(Colors.FAIL + "connection error" + Colors.ENDC)
                if self.repeats < 3:
                    self.repeats += 1
                    time.sleep(1)
                    return self.get_site_info(url)
                else:
                    with websites_lock:
                        failed_url_requests.add(last_url_requested)
                    self.repeats = 0
            else:
                with websites_lock:
                    failed_url_requests.add(last_url_requested)
            return []

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
        global known_website_data, known_websites, checked_websites
        try:
            json_data = self.read_json()
            
            with data_lock:
                # Handle both old list format and new dict format
                if isinstance(json_data.get("site_known_data", []), list):
                    # Convert old format [url, keywords] to dict
                    known_website_data = {item[0]: item[1] for item in json_data["site_known_data"] if len(item) >= 2}
                else:
                    known_website_data = json_data.get("site_known_data", {})
            
            with websites_lock:
                known_websites = set(json_data.get("site_known", []))
                checked_websites = set(json_data.get("site_checked", []))
                
        except:
            print(Colors.WARNING + "warning: json file has no valuable information" + Colors.ENDC)

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

    def process_url(self, url):
        # remove excess slashes, eg. https://example.com//path//to//resource to https://example.com/path/to/resource
        segments = url.split('/')
        correct_segments = []
        for segment in segments:
            if segment != '':
                correct_segments.append(segment)
        first_segment = str(correct_segments[0])
        if first_segment.find('http') == -1:
            correct_segments = ['http:'] + correct_segments
        correct_segments[0] = correct_segments[0] + '/'
        normalized_url = '/'.join(correct_segments)

        # then remove ? mark
        if '?' in normalized_url:
            normalized_url = normalized_url.split('?')[0]
        # then remove # mark
        if '#' in normalized_url:
            normalized_url = normalized_url.split('#')[0]
        # remove trailing slash
        if normalized_url.endswith('/'):
            normalized_url = normalized_url[:-1]
        return normalized_url
    def get_url_keywords(self, url):
        # remove non ascii characters in url
        for char in url:
            if char not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789':
                url = url.replace(char, ' ')
        
        # split url into small sections
        url_sections = url.split(' ')
        
        filtered_sections = []
        for section in url_sections:
            section = section.strip()  # remove leading and trailing spaces
            
            if (section == "https" or 
                section == "http" or 
                section == "www" or 
                section in KNOWN_WEBSITE_DOMAINS or 
                section == ""):
                # skip
                continue
            else:
                filtered_sections.append(section)

        # ok thats about it
        return ' '.join(filtered_sections).strip()  # remove leading and trailing spaces


class CrawlBot:
    def __init__(self):
        self.crawler = Crawler()

    def crawl(self):
        global crawls
        print(Colors.HEADER + "initiating crawl.." + Colors.ENDC)
        
        while not stop:
            website = None
            
            with websites_lock:
                uncrawled = known_websites - checked_websites - failed_url_requests
                if uncrawled:
                    website = random.choice(list(uncrawled))
            
            if website:
                with websites_lock:
                    if website in checked_websites or website in failed_url_requests:
                        continue
                
                print(f"crawling {website}")
                self.crawler.get_site_info(website)
                
                with crawls_lock:
                    crawls += 1
                    current_crawls = crawls
                
                # write to json every 10 crawls
                if current_crawls % 10 == 0:
                    self.crawler.write_json()

                time.sleep(0.1)
            else:
                time.sleep(1)
        print(Colors.OKCYAN + "this process stopped. bye!" + Colors.ENDC)

if __name__ == "__main__":
    initial_site = sys.argv[1] if len(sys.argv) > 1 else "https://google.com"
    with websites_lock:
        known_websites.add(initial_site)
    
    crawlbot = CrawlBot()
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(crawlbot.crawl) for _ in range(10)]
        
        try:
            for future in futures:
                future.result()
        except KeyboardInterrupt:
            stop = True
            print(Colors.OKCYAN + "stopping crawler..." + Colors.ENDC)
            print(Colors.OKCYAN + "writing to json file one last time..." + Colors.ENDC)
            crawlbot.crawler.write_json()
