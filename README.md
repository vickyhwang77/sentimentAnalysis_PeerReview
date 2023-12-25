# Introduction
This script performs sentiment analysis on peer reviews of eLife's and F1000's published preprints. The goal is to calculate sentiment scores from the extracted texts. The sentiment scores are based on a custom analysis that categorizes words and phrases into different levels of positivity and negativity.

# Dependencies
Before running the script, make sure to install the following dependencies: 
- Beautiful Soup: ```pip install beautifulsoup4```
- Requests: ```pip install requests```
- Pandas: ```pip install pandas```
- NLTK: ```pip install nltk```

# How to run
1. Clone the repository: ``````
2. Navigate to the project directory
3. Install the dependencies above
4. Modify the main() function with your specific requirements:
   - ```topic```: specify the topic of interest (topics can be found by going to elifesciences.org)
   - ```num_pages```: specify the number of pages to search through
   - ```rating```: filter by the desired rating ("Any", "Doubtful", "Useful", "Good", "Excellent")

# Output
The script outputs a CSV file named eLife.csv containing the extracted data with columns: "Topic," "Title," "Rating," "Assessment," and "Score." 

