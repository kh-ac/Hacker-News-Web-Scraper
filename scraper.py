
import requests
import re
from bs4 import BeautifulSoup
import csv

if __name__ == "__main__":

    articles = []

    url = 'https://news.ycombinator.com/news'

    # Requesting the html page
    response = requests.get(url)

    # Creating BeautifulSoup Object
    htmlSoup = BeautifulSoup(response.text, "html.parser")

    #
    for item in htmlSoup.findAll(name="tr" , attrs= {"class" : "athing"}) :
        
        aTag = item.find("span" , {"class" : "titleline"}).find("a")
        itemLink = aTag.get("href") if aTag else None 
        

        itemText = aTag.getText(strip=True) if aTag else None
      

        nextRow = item.findNextSibling("tr") if item else None
        

        itemScore = nextRow.find("span" , {"class" : "score"}) 
        itemScore = itemScore.getText(strip = True) if itemScore else "0 points"

         # We use regex here to find the correct element
        itemComments = nextRow.find("a" , string = re.compile("\d+(&nbsp;|\s)comment(s?)"))
        itemComments = itemComments.getText(strip = True).replace("\xa0"," ") if itemComments else "0 comments"

        articles.append({
            "title" : itemText,
            "link" : itemLink,
            "score" : itemScore,
            "comments" : itemComments,
        })

    
        
    # Saving data on a CSV file
    
    csvColunms = ["title" , "link" , "score" , "comments"]

    csvFile = "hackerNews.csv"

    try:

        with open(csvFile , "w"  , encoding="UTF-8") as file:
            writer = csv.DictWriter(file,fieldnames=csvColunms )
            writer.writeheader()
            for article in articles:
                writer.writerow(article)


    except IOError:
        print("I/O error")
        

