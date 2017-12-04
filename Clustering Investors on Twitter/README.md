# Clustering Investors on Twitter
## Objective
Recently I started to develop an interest in investments. I decide to follow some famous investors on twitter. But who should I follow and how can I quickly know what they are talking about? I googled "famous investors on twitter" and got several lists. In total I found 145 famous investors on twitter. Each of them has thousands of tweets. I'm not going to read all of their tweets. It's going to kill me. As a data scientist, I decide to quickly know what they are talking about using machine learning algorithms. 

The objective of this project was using LDA(latent dirichlet allocation) and K-means clustering algorithms to find out the major topics for the 143 famous investors on twitter and group them based on their topics.

## Findings - Word Clouds for 6 Groups
### Trading Group
![alt text](https://github.com/tongwu21/Data-Science-Projects/blob/master/Clustering%20Investors%20on%20Twitter/word_cloud/Trading.png)

### Real Estate Group
![alt text](https://github.com/tongwu21/Data-Science-Projects/blob/master/Clustering%20Investors%20on%20Twitter/word_cloud/Real%20Estate.png)

### Global Economics Group
![alt text](https://github.com/tongwu21/Data-Science-Projects/blob/master/Clustering%20Investors%20on%20Twitter/word_cloud/Global%20Economics.png)

### Politics Group
![alt text](https://github.com/tongwu21/Data-Science-Projects/blob/master/Clustering%20Investors%20on%20Twitter/word_cloud/Politics.png)

### Venture Capital Group
![alt text](https://github.com/tongwu21/Data-Science-Projects/blob/master/Clustering%20Investors%20on%20Twitter/word_cloud/Venture%20Capitals.png)

### Mentor Group
![alt text](https://github.com/tongwu21/Data-Science-Projects/blob/master/Clustering%20Investors%20on%20Twitter/word_cloud/Mentors.png)

## Notebooks and Scripts
- [Clustering_Investors_on_Twitter-Master](https://github.com/tongwu21/Data-Science-Projects/blob/master/Clustering%20Investors%20on%20Twitter/Clustering_Investors_on_Twitter-Master.ipynb) - This notebook contains the code that I used to collect, clean, tokenize and lemmatize tweets, developing lda models and clustering models. 

- [Clustering Investors on Twitter.key](https://github.com/tongwu21/Data-Science-Projects/blob/master/Clustering%20Investors%20on%20Twitter/Clustering%20Investors%20on%20Twitter.key) - the final slides for this project.

## Tools
Tweepy, SpaCy, Scikit-learn, LDA, Gensim, K-means
