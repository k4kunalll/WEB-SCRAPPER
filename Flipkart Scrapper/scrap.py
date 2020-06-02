import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pandas as pd

searchstr = input("ENTER THE SEARCH WORD: ")

flipkart_url = "https://www.flipkart.com/search?q=" + searchstr

uClient = uReq(flipkart_url)    #requesting the webpage from internet
flipkartPage = uClient.read()   #reading the webpage
# uClient.close()                 #connection close

flipkart_html = bs(flipkartPage, "html.parser")     #parsing the webpage as html

bigboxers = flipkart_html.findAll("div",{"class":"bhgxx2 col-12-12"})

del bigboxers[0:3]   #remove unnecessary boxes
box = bigboxers[0]

productLink = "https://www.flipkart.com" + box.div.div.div.a["href"]

prodRes = requests.get(productLink)
prodRes.encoding = "utf-8"
prod_html = bs(prodRes.text, "html.parser")

commentBoxes = prod_html.find_all("div",{"class":"_3nrCtb"})

name_list = []
rating_list = []
comment_list = []
heading_list = []


for i in range(0, len(commentBoxes) - 1):

    commentBoxes = prod_html.find_all("div", {"class": "_3nrCtb"})
    commentBox = commentBoxes[i]
    try:
        username = commentBox.find_all("p", {"class": "_3LYOAd _3sxSiS"})[0].text
        name_list.append(username)
    except:
        print("No Customer Username")

    try:
        userHeading = commentBox.find_all("p", {"class": "_2xg6Ul"})[0].text
        heading_list.append(userHeading)
    except:
        print("No Heading")

    try:
        userRating = commentBox.find_all("div", {"class": "hGSR34 E_uFuv"})[0].text
        rating_list.append(userRating)
    except:
        print("No Rating")

    try:
        usercomment = commentBox.find_all("div", {"class": "qwjRop"})[0].text
        comment_list.append(usercomment)
    except:
        print("No Comment")


for i in range(len(name_list)):
    print("\nReview No:", i + 1)

    try:
        print("CUSTOMER NAME: " + name_list[i])
    except:
        print("CUSTOMER NAME: --NO NAME--")
    try:
        print("REVIEW HEADING: ", heading_list[i])
    except:
        print("REVIEW HEADING: --N0 HEADING--")
    try:
        print("RATING : " + rating_list[i])
    except:
        print("RATING : --NO RATING--")
    try:
        print("COMMENT: " + comment_list[i])
    except:
        print("COMMENT: --NO COMMENT--")




# dictionary of lists
dict = {"SEARCHED PRODUCT": searchstr,'CUSTOMER NAMES': name_list, 'HEADINGS': heading_list, 'RATINGS': rating_list, "REVIEWS" : comment_list}

df = pd.DataFrame(dict)

# saving the dataframe
df.to_csv('reviews.csv', mode='a')

