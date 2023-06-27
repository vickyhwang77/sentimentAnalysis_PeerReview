""" 06/08/23 by Victoria Hwang
    This script uses webscraping to extract peer review from F1000's reviewed articles,
    with the goal to calculate sentiment scores from these texts and use them to predict 
    the peer review result
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ngrams


def extract_assessment():
    # Step 1: Setup 

    # url = the webpage that lists all the papers. 
    url = "https://f1000research.com/browse/articles"
    scores = []             # -1 = not approved
                            # 0 = approved w/ reservations
                            # 1 = approved
  
    titles = []
    review_columns = []
    review_texts = []
    data = []
    #for page in range(1, num_pages+1):

    # Step 2. Get links to all the papers listed.
    result = requests.get(url)
    # create BeautifulSoup object to parse html content of webpage
    soup = BeautifulSoup(result.content, "html.parser")

    # Get the list containing all the papers.
    papers_list = soup.find("div", class_="article-listing f1000research")
    papers = papers_list.find_all("div", class_= "article-browse-wrapper f1r-searchable")
  

    # Extract the reviews from reviewed papers:
    for paper in papers: 
        # Each paper may have more than one review:
   
        # and also an accompanying decision: Yes, Maybe, No:  
        num_reviews = 0 
        num_approved = 0
        num_maybe = 0
        num_disproved = 0

        awaiting_review = paper.find("span", class_="peer-review-status")

        # skip papers without reviews
        if awaiting_review: 
            continue 

        else: 
            paper_link = paper.find("a", class_ ="article-link")
            paper_link_url = paper_link["href"]

            # Using the paper link, access paper contents:
            paper_content = requests.get(paper_link_url)
            paper_soup = BeautifulSoup(paper_content.content, "html.parser")
            paper_title = paper_soup.find("h1", class_="js-article-title")
            titles.append(paper_title.text)
          
            
            # Inside the paper, there are multiple peer reviews. For each of them,
            # extract the score and review:
            reviews = paper_soup.find_all("div", \
            class_ ="p-article__sidebar-view u-pl u-hide js-article-sidebar-view")
        
            for review in reviews:

                num_reviews += 1        # for calculating overall report score

                # Get reviewer decision:
                decision = review.find("span", class_= \
                "p-article__report-status t-caption u-upper-spacing u-upper u-ib u-middle u-weight--md")
                

                # Calculate score based on reviewer decision
                if decision.text == "Approved":
                    num_approved += 1
                elif decision.text == "Approved With Reservations":
                    num_maybe += 1
                else: 
                    num_disproved +=1

                #print("Decision: " + decision.text + "\n")


                paragraph = review.find("div", class_= "")
                review_texts.append(paragraph.text)
                
                # To handle possible multiple reviews
                review_columns.append(f"Review {num_reviews}")

            
            reviewer_score = (num_approved + (0*num_maybe) + (-1*num_disproved)) / num_reviews
            scores.append(reviewer_score)

            data.append({
                "Title": paper_title.text.strip(),
                "Reviewer Score": reviewer_score,
                **dict(zip(review_columns, review_texts))
            })

    df = pd.DataFrame(data)
    
    df.to_csv("f1000.csv", index=False)



def main():
    extract_assessment()

if __name__ == "__main__":
    main()
