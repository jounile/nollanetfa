import datetime
import logging
import os
from urllib.request import urlopen
from html.parser import HTMLParser
import json

import azure.functions as func

# https://dashboard.phantomjscloud.com
PHANTOMJS_CLOUD_API_KEY = 'ak-p5k6d-qz6ht-q83rv-pkjdv-gmy5e'

def main(mytimer: func.TimerRequest, outputBlob: func.Out[str]) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    request = {
        "url":"https://www.supla.fi/audio/3061793",
        "renderType":"html"
    }

    if mytimer.past_due:
        logging.info('The timer is past due!')
  
        url = 'http://PhantomJScloud.com/api/browser/v2/' + PHANTOMJS_CLOUD_API_KEY + '/'
        headers = {'content-type':'application/json'}
        req = Request(url, request, headers)
        response = urlopen(req)
        html = response.read()

        parser = AdvancedHTMLParser.AdvancedHTMLParser()
        parser.parseStr(html)
        lis = parser.getElementsByTag('li')
        
        items = []
        item = {}

        for li in lis:
            item['thumbnail'] = li.span.span.img.get('src')
            item['title'] = li.a.get('title')
            item['link'] = li.a.get('href')
            items.append(item)
            print(items)

        logging.info(f"Blob trigger executed!")

        output = "Hello World!"
        outputBlob.set(output)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
