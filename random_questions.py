import dryscrape
from bs4 import BeautifulSoup
import random

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
        soup = html_parse_link(link)
        problem_statement = soup.find("div", class_="starwars-lab")
        problem_soup= BeautifulSoup(str(problem_statement), "lxml")
        problem_statement = problem_soup.find_all("p")
        statement = ""
        for i in problem_statement:
            for j in i.contents:
                if str(j.string)=="None":
                    statement+="\n"
                else:
                    j = str(j.string)
                    if j.endswith(":-"):
                        statement+="\n\n"+j+"\n\n"
                    else:
                        statement+=j
        print(statement)
        input_output = soup.find_all("pre")
        print("Example:\n")
        print("INPUT")
        print(input_output[0].string)
        print("OUTPUT")
        print(input_output[1].string)
        explaination = soup.find_all("span", class_="weight-600 form-label")
        end_stuff = soup.find_all("div", class_="less-margin")
        if explaination:
            print("Explaination")
            statement = ""
            for i in end_stuff[1].contents:
                if str(i.string)!="None":
                        statement+=str(i.string)
                else:
                    for j in i.contents:
                        if str(j.string)=="None":
                            statement+="\n"
                        else:
                            j = str(j.string)
                            if j.endswith(":-") or j.endswith(":"):
                                statement+="\n\n"+j+"\n\n"
                            else:
                                statement+=j
            print(statement)
            end_stuff = soup.find("div", class_="standard-margin light small problem-guidelines")
            soup =  BeautifulSoup(str(end_stuff), "lxml")
            end_stuff = soup.find_all("div")
            statement = ""
            for i in range(1,4):
                for each in end_stuff[i].contents:
                    if str(each.string) != "None":
                        statement+=each.string
                    else:
                        for j in each.contents:
                            statement+=str(j.string).strip("\n")
            print(statement)
        else:
            end_stuff = soup.find_all("div", class_="standard-margin light small problem-guidelines")
            soup =  BeautifulSoup(str(end_stuff), "lxml")
            end_stuff = soup.find_all("div")
            statement = ""
            for i in range(1,4):
                if str(each.string) != "None":
                    statement+=each.string
                else:
                    for j in each.contents:
                        statement+=j.string
            print(statement)
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
