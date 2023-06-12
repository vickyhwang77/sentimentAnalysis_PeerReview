""" 06/08/23 by Victoria Hwang
    This script uses webscraping to extract peer review from eLife's published 
    preprints, with the goal to calculate sentiment scores from these texts. 
"""

from bs4 import BeautifulSoup
import requests

# structure of the website: list of reviewed papers listed on 22 pages, click on 
# any paper link, and the actual review is under a link within the paper


# Step 1: Setup 

# url = the webpage that lists all the papers. 
url = "https://elifesciences.org/reviewed-preprints"
result = requests.get(url)
# create BeautifulSoup object to parse html content of webpage
soup = BeautifulSoup(result.content, "html.parser")

# Step 2. Get links to all the papers listed.

# Get the list containing all the papers.
papers_list = soup.find("ol", class_="listing-list")
# Get all the papers in the list.
papers = papers_list.find_all("li", class_="listing-list__item")

# It is possible to do multiple pages, or all at this point. 
# Finding all papers is an (nearly) endless loop.  

# For all the papers, find the link to the paper.
base_url = "https://elifesciences.org"

for paper in papers:

    paper_link = paper.find("a", class_ ="teaser__header_text_link")
    paper_link_url = base_url + paper_link["href"]

    paper_content = requests.get(paper_link_url)
    paper_soup = BeautifulSoup(paper_content.content, "html.parser")
    # Find all paragraphs, keep the first one
    eLife_section = paper_soup.find("div", class_="review-content_body")
    eLife_paragraphs = eLife_section.find_all("p")
    eLife_assessment = eLife_paragraphs[1]
    print(eLife_assessment.text.strip())
    print("\n")
   




# 3. Iterate over each paper link and extract the Peer review paragraph
"""for paper_link in paper_links:
    
    # Get the linked page for curr paper
    curr_paper = requests.get(paper_link['href'])
    
    paper_soup = BeautifulSoup(curr_paper.content, "html.parser")

    # Locate the Peer review tab on linked page
    tab = paper_soup.find("a", text="Peer review")

    if tab:
        peer_review_paragraph = tab.find_next("p").text
        print(peer_review_paragraph)
    else:
        print("Paragraph not found.")"""





