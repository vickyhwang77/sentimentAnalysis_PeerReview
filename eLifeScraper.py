""" 06/08/23 by Victoria Hwang
    This script uses webscraping to extract peer review from eLife's published 
    preprints, with the goal to calculate sentiment scores from these texts. 
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ngrams

def extract_assessment(topic, num_pages, rating):
    # Step 1: Setup 

    # url = the webpage that lists all the papers. 
    url = "https://elifesciences.org/reviewed-preprints"

    # For all the papers, find the link to the paper.
    base_url = "https://elifesciences.org"
    base_url2 = "https://elifesciences.org/reviewed-preprints"
    topics = []
    titles = []
    assessments = []
    scores = []
    ratings = []
    page_no = 0
    paper_no = 0

    for page in range(1, num_pages+1):
        
        result = requests.get(url)
        # create BeautifulSoup object to parse html content of webpage
        soup = BeautifulSoup(result.content, "html.parser")

        # Step 2. Get links to all the papers listed.

        # Get the list containing all the papers.
        papers_list = soup.find("ol", class_="listing-list")
        # Get all the papers in the list.
        papers = papers_list.find_all("li", class_="listing-list__item")
        page_no += 1
        print("Page:", page_no)
        # For each paper, get it's link:
        for paper in papers:

            paper_no += 1

            paper_link = paper.find("a", class_ ="teaser__header_text_link")
            paper_link_url = base_url + paper_link["href"]

            try: 
            # Using the paper link, access paper contents:
                paper_content = requests.get(paper_link_url)
                paper_soup = BeautifulSoup(paper_content.content, "html.parser")

                # Find the paper topic
                paper_topic = paper_soup.find("a", class_="article-flag__link")
                
                # Find the paper title
                paper_title = paper_soup.find("h1", class_="title")
                print(paper_title.text)

                # Find all paragraphs, keep the first one
                eLife_section = paper_soup.find("div", class_="review-content_body")
                
                eLife_paragraphs = eLife_section.find_all("p")
                eLife_assessment = eLife_paragraphs[1]
                paragraph = eLife_assessment.text.strip()  
            

                # Keep only the papers whose scores that match the given score
                paper_score = simpleAnalysis(paragraph)
                paper_rating = giveRating(paper_score)

                if rating == 'Any':
                    if topic == "Any" or topic == paper_topic.text.strip():
                        topics.append(paper_topic.text.strip())
                        titles.append(paper_title.text.strip())
                        assessments.append(paragraph)
                        scores.append(paper_score)
                        ratings.append(paper_rating)

                elif rating == "Doubtful" and paper_score < -0.5:
                    if topic == "Any" or topic == paper_topic.text.strip():
                        topics.append(paper_topic.text.strip())
                        titles.append(paper_title.text.strip())
                        assessments.append(paragraph)
                        scores.append(paper_score)
                        ratings.append(paper_rating)

                elif rating == "Useful" and -0.5 <= paper_score < 0:
                    if topic == "Any" or topic == paper_topic.text.strip():
                        topics.append(paper_topic.text.strip())
                        titles.append(paper_title.text.strip())
                        assessments.append(paragraph)
                        scores.append(paper_score)
                        ratings.append(paper_rating)
                    
                elif rating == "Good" and 0 <= paper_score < 1:
                    if topic == "Any" or topic == paper_topic.text.strip():
                        topics.append(paper_topic.text.strip())
                        titles.append(paper_title.text.strip())
                        assessments.append(paragraph)
                        scores.append(paper_score)
                        ratings.append(paper_rating)
                    
                elif rating == "Excellent" and paper_score == 1:
                    if topic == "Any" or topic == paper_topic.text.strip():
                        topics.append(paper_topic.text.strip())
                        titles.append(paper_title.text.strip())
                        assessments.append(paragraph)
                        scores.append(paper_score)
                        ratings.append(paper_rating)
                
                else:
                    continue
    
                time.sleep(2)

            except AttributeError:
                # Handle the case when the attribute of the webpage is not found
                continue

        # Go to next page of papers
            new_url = base_url2 + "?page=" + str(page+1)     # page numbering begins on page 2
            url = new_url

    # Create Database
    df = pd.DataFrame({"Topic":topics, "Title":titles, "Rating":ratings, "Assessment":assessments, "Score":scores}) 
    print(df)
 
    df.to_csv("eLife.csv", index=False)  # Save Data to CSV file

    print(paper_no)

def simpleAnalysis(paragraph):

    best_words = ["landmark, exceptional"]      # 1
    great_words = [ "fundamental", "compelling"] # 0.75
    good_words = ["important"]                  # 0.5
    pos_words = ["valuable", "convincing"]      # 0.25
    neu_words = ["useful", "solid"]             # 0
    neg_words = ["partially supported", "further strengthened", "require additional"] # -0.25
    bad_words = ["inadequate"]                # -0.5
    worst_words = ["incomplete"]                # -1

    num_best = 0
    num_great = 0
    num_good = 0 
    num_pos = 0
    num_neu = 0
    num_neg = 0
    num_bad = 0
    num_worst = 0
    
    stop_words = set(stopwords.words('english'))        # remove unecessary words
    num_words = 0      # initialize new counter for paragraph after stop words are filtered
    paragraph = paragraph.lower()

    # Generate n-grams from tokenized words
    tokens = word_tokenize(paragraph)
    n = 2  # Change this to the desired n-gram size
    ngrams_list = list(ngrams(tokens, n))

    # Check words:
    for word in tokens:
        if word not in stop_words:
            num_words += 1
            if word in best_words:
                num_best += 1
            elif word in great_words:
                num_great += 1
            elif word in good_words:
                num_good += 1
            elif word in pos_words:
                num_pos += 1
            elif word in neu_words:
                num_neu += 1
            elif word in neg_words:
                num_neg += 1
            elif word in bad_words:
                num_bad += 1
            elif word in worst_words:
                num_worst += 1

    # Check phraes:
    for ngram in ngrams_list:
        phrase = " ".join(ngram)
        if phrase in neg_words:
            num_neg += 1

     
    meaningful_words = num_best+num_great+num_good+num_pos+num_neu+num_neg+num_bad+num_worst
    score = ((num_best)+(0.75*num_great)+(0.5*num_good)+(0.25*num_pos)+\
             (0*num_neu)+(-0.25*num_neg)+(-0.5*num_bad)+(-1*num_worst)) / meaningful_words
    
    return score

def giveRating(paper_score):       # a simple method to convert numerical rating into description
    rating = ""

    if paper_score < -0.5:
        rating = "Doubtful"
    elif -0.5 <= paper_score < 0:
        rating = "Useful"
    elif 0 <= paper_score < 1:
        rating = "Good"
    elif paper_score == 1:
        rating = "Excellent"
    
    return rating 
        
    
def main():
    #format: extract_assessment("Topic, number pages to search, paper rating")
    extract_assessment("Any", 29, "Any")
if __name__ == "__main__":
    main()




