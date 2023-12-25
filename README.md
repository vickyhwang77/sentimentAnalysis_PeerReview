# Introduction
This script performs sentiment analysis on peer reviews of eLife's and F1000's published preprints. The goal is to calculate sentiment scores from the extracted texts. The sentiment scores for eLife are based on a custom analysis that categorizes words and phrases into different levels of positivity and negativity. For F1000, a prediction is generated based on reviewer decisions such as "Approved," "Approved With Reservations," and other possible outcomes.

# Dependencies
Before running the script, make sure to install the following dependencies: 
- Beautiful Soup: ```pip install beautifulsoup4```
- Requests: ```pip install requests```
- Pandas: ```pip install pandas```
- NLTK: ```pip install nltk```

# How to run the Scrapers
1. Clone the repository: 
2. Navigate to the project directory
3. Install the dependencies above
4. Modify the main() function with your specific requirements:
   - For eLife:
      - ```topic```: specify the topic of interest (topics can be found by going to elifesciences.org)
      - ```num_pages```: specify the number of pages to search through
      - ```rating```: filter by the desired rating ("Any", "Doubtful", "Useful", "Good", "Excellent")
   - For F1000:
      - ```num_pages```: specify the number of pages to search through
5. Output:
   - The elife script outputs a CSV file named eLife.csv containing the extracted data with columns: "Topic," "Title,"       "Rating," "Assessment," and "Score."
  
   - The F1000 script outputs a CSV file named f1000.csv containing the extracted data with columns: "Title," "Reviewer Score," and "Mega-Review." Additionally, individual reviews are included as separate columns (e.g., "Review 1," "Review 2," etc.).
  
# Further Sentiment Analysis
The F1000 texts can be use to fine-tune a pre-trained Sentiment Analysis Model. Here is a link to a colab notebook which uses distilBERT as the model, but any variation of BERT can be used: https://colab.research.google.com/drive/116tjoA9ZCcx9bEJ7zIBegmiD96jwbGxE?usp=sharing


