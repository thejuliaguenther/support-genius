# These code snippets use an open-source library. http://unirest.io/python
response = unirest.post("https://japerk-text-processing.p.mashape.com/sentiment/",
  headers={
    "X-Mashape-Key": "VkkUH57V4gmshJoCHqSkfWpERXYop1na3uVjsnTfHjJnxtSqby",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
  },
  params={
    "language": "english",
    "text": "great movie"
  }
)