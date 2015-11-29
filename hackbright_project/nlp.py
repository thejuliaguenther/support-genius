
import unirest


def process_text(tickets):
    """
    This method used the Mashape Text-Processing API to perform 
    sentiment analysis on the the support tickets
    """
    responses = []
    for ticket in tickets:
        ticket_text = ticket.ticket_content
        # These code snippets use an open-source library. http://unirest.io/python
        response = unirest.post("https://japerk-text-processing.p.mashape.com/sentiment/",
          headers={
            "X-Mashape-Key": "DYfeuhenzwmshIdCFOypxGFL2dwRp1OxTjCjsn2P4W3Mh4Mopr",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
          },
          params={
            "language": "english",
            "text": ticket_text
          }
    )
        response_parsed = response.body 
        response_label = response_parsed['label']
        # print response_label
        print ticket.ticket_id
        print response_parsed[response_label]['probability']

    #     responses.append(response)
    # print responses
    # return responses 

# process_text()




   