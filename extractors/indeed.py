# selenium 사용하여 크롤링
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from chromedriver import Options
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(ChromeDriverManager().install())
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
browser = webdriver.Chrome(options=options)


#페이지 전부 확인
def get_page_count(keyword):
  browser.get(f"https://www.indeed.com/jobs?q={keyword}&limit=50")
  soup_test = browser.page_source
  soup = BeautifulSoup(soup_test, "html.parser")
  pagination = soup.find("ul", class_="pagination-list")
  if pagination == None:
    return 1
  pages = pagination.find_all("li", recursive=False)
  count = len(pages)
  # 5개만 가져오기
  if count >= 5:
    return 5
  else:
    return count


# print(get_page_count("python"))
# print(get_page_count("nextjs"))
# print(get_page_count("django"))
# print(get_page_count("nestjs"))
# print(get_page_count("java"))


def extract_indeed_jobs(keyword):
  pages = get_page_count(keyword)
  print("Found", pages, "pages")
  for page in range(pages):
    final_url = f"https://www.indeed.com/jobs?q={keyword}&start={page*10}&limit=50"
    browser.get(final_url)
    print("Requesting", final_url)
    #  base_url = "https://kr.indeed.com/jobs?q="
    soup_test = browser.page_source
    soup = BeautifulSoup(soup_test, "html.parser")
    job_list = soup.find("ul", class_="jobsearch-ResultsList")
    jobs = job_list.find_all('li', recursive=False)
    #print(jobs)
    results = []
    for job in jobs:
      zone = job.find("div", class_="mosaic-zone")
      if zone == None:
        anchor = job.select_one("h2 a")
        title = anchor['aria-label']
        link = anchor['href']
        company = job.find("span", class_="companyName")
        location = job.find("div", class_="companyLocation")
        job_data = {
          'link': f"https://kr.indee.com{link}",
          'company': company.string.replace(",", " "),
          'location': location.string,
          'position': title.replace(",", " ")
        }
        results.append(job_data)
  return results
