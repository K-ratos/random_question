import dryscrape
from bs4 import BeautifulSoup
import random
import subprocess
import re

base_url = "https://www.hackerearth.com"
browser = dryscrape.Session()
browser.set_attribute('auto_load__images', False)
browser.set_attribute('javascript_can_open_windows', False)
practice_link = ""
def html_parse_link(link):
    browser.visit(link)
    body = browser.body()
    soup = BeautifulSoup(body, "lxml")
    return soup

def parse_problem_list_page(link):
    soup = html_parse_link(link)
    problem_links = soup.find_all("li", class_="prob")
    problem_link = ""
    try:
        problem_link = problem_links[random.randint(0,len(problem_links)-1)]
    except:
        practice_link = ""
        return
    soup = BeautifulSoup(str(problem_link), "lxml")
    problem_link = soup.find("a", class_="dark")["href"]
    link = base_url + problem_link
    print("           "+problem_link.split("/")[-2].replace("-", " ").upper())
    tmp ="           "
    for i in range(0, len(problem_link.split("/")[-2])):
        tmp+="_"
    print(tmp)
    print("\n LINK to PROBLEM --->")
    print(link+"\n\n")
    print("Enter p to display problem(not always good format) else e")
    answer = input()
    if answer == "p":
        command = 'lynx ' + link + ' -dump'
        x = subprocess.check_output(command, shell=True)
        try:
            s = re.search("Analytics", (x.decode("utf-8", 'ignore'))).end()
            e = re.search("CODE EDITOR", (x.decode("utf-8", 'ignore'))).start()
        except:
            print()
        print(x.decode("utf-8", 'ignore')[s:e])
    else:
        print("Happy Coding!!")



while not practice_link:
    problem_topic = ["/practice/basic-programming", "/practice/data-structures",
    "/practice/algorithms", "/practice/math"]
    problem_link = problem_topic[random.randint(0,3)]
    link = base_url + problem_link
    print("______________________________________________")
    print("                "+problem_link.split("/")[2].replace("-", " ").upper())
    print("______________________________________________")
    print()
    soup = html_parse_link(link)
    ul = soup.find("ul", class_="subtrack-list no-list-style")
    soup = BeautifulSoup(str(ul), "lxml")
    subtopics_links = soup.find_all("a")
    for i in range(0,len(subtopics_links)):
        subtopics_links[i] = subtopics_links[i]["href"]
    subtopic = subtopics_links[random.randint(0,len(subtopics_links)-1)]
    link = base_url + subtopic
    print("----------------------------------------------")
    print("            "+subtopic.split("/")[-2].replace("-"," ").upper())
    print("----------------------------------------------")
    soup = html_parse_link(link)
    practice_link = soup.find("a", id="practice-problems")
    if practice_link:
        link = base_url + practice_link["href"]
        soup = html_parse_link(link)
        step_span = soup.find("span", class_="step-links")
        soup = BeautifulSoup(str(step_span), "lxml")
        a = soup.find_all("a")
        if a:
            href = a[len(a)-1]["href"].split("/")
            no_of_pages = 0
            for each in href:
                if each.isdigit():
                    no_of_pages = int(each)
            random_page = random.randint(0,no_of_pages)
            link += str(random_page)
            parse_problem_list_page(link)
        else:
            parse_problem_list_page(link)
    else:
        print("\n NO PROBLEM FOR THIS TOPIC")
        print("trying again")
