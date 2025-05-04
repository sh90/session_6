# pip install newspaper3k
"""
An RSS feed (Really Simple Syndication) is a type of web feed that allows users and applications to receive updates 
to websites in a standardized, computer-readable format.

Here’s a breakdown of how it works:

Publishers (like blogs, news sites, or podcasts) create an RSS feed — an XML file containing summaries or full content of their latest updates.

Users subscribe to that feed using an RSS reader (such as Feedly, Inoreader, or an email client).

The reader periodically checks the feed and shows new content, so users can stay updated without visiting each site individually.

Example Use Case:
You follow 10 blogs. Instead of visiting each site daily, you subscribe to their RSS feeds in one app. That app aggregates all new posts in one place.

Would you like to see an example of what an RSS feed file looks like?

"""
import newspaper
import feedparser
import openai
import data_info

openai.api_key = data_info.open_ai_key

def scrape_news_from_feed(feed_url):
    articles = []
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        # create a newspaper article object
        article = newspaper.Article(entry.link)
        # download and parse the article
        article.download()
        article.parse()
        # extract relevant information
        articles.append({
            'title': article.title,
            'author': article.authors,
            'publish_date': article.publish_date,
            'content': article.text
        })
    return articles


feed_url = 'http://feeds.bbci.co.uk/news/rss.xml'
articles = scrape_news_from_feed(feed_url)

# print the extracted articles
for article in articles[0:5]:
    print('Title:', article['title'])
    print('Author:', article['author'])
    print('Publish Date:', article['publish_date'])
    print('Content:', article['content'])
    #Analyze sentiment
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Analyze the sentiment of this financial news."+article['content']}],
        temperature=0.1
    )
    content = response.choices[0].message.content
    print(content)
    # named entity recognition
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Identify the name of the comapnies from the given news"+article['content']}],
        temperature=0.1
    )
    print(response)
    content = response.choices[0].message.content
    print(content)
