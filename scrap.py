import feedparser
import os
import sendgrid
from sendgrid.helpers.mail import Mail
import dontpad

#configs
sg = sendgrid.SendGridAPIClient('SG-key')
rss_url = 'https://www.abc.com/rss'
from_email = 'abc@abc.com'
to_emails='abc@abc.com'
subject='Subject'
dontpad_url = 'XXXX'

def upwork(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        feed = feedparser.parse(rss_url)

        #last = os.environ.get('title', 'error')
        #os.environ["title"] = new_last

        last = dontpad.read(dontpad_url)
        new_last = feed.entries[0].title

        total = len(feed.entries)

        html = ''
        i = 0
        for x in feed.entries:
            title = x.title
            link = x.link
            if title == last: #if the most recent title is equal to the last title read, do nothing
                break
            else:
                html_row = '<br><a href="' + link + '">' + title + '</a>'
                #print(html_row)
                html += html_row
                i += 1

        #print(i)
        html += '<br> Total updates: ' + str(i)

        if i>0: #only send the email if there are new titles
          message = Mail(from_email=from_email,to_emails=to_emails,subject=subject,html_content=html)
          response = sg.send(message)

        dontpad.write(dontpad_url, new_last)
        return html
