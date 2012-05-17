#!/usr/bin/python

from time import strftime
import sys
import requests 
import csv
import json

print "...\n"


# Store CSV data as a dictionary for python

data = csv.reader(open("data.csv"), delimiter=';')
parsed_data = []
# Read the column names from the first line of the file
fields = data.next()
for row in data:
        # Zip together the field names and values
    items = zip(fields, row)
    item = {}
        # Add the value to our dictionary
    for (name, value) in items:
        item[name] = value.strip()
    parsed_data += [items]


# Store just ids and urls

ids = []
urls = []

for entry in parsed_data:
    for (name, value) in entry:
        if name == "ID-prefix":
            an_id = value
        if name == "ID-suffix":
            the_id = an_id + "." + value
        if name == "New URL":
            the_url = value

            urls.append(the_url) # form the list of urls
            ids.append(the_id) # form the list of IDs


# Store OAuth2 credentials and other Curl values
api_url_pre = "https://knol-redirects.appspot.com/_ah/api/redirects/v0.1/"

oauth2 = "Bearer ya29. ... " # @TODO replace this with your key!!!

headers = {'content-type': 'application/json'}
headers['Authorization'] = oauth2
payload = {}

response=""

# Loop through the dictionary data and call curl
timenow = strftime("%Y-%m-%d-%H:%M:%S")
log_name = "log-" + timenow + ".log"
log = open(log_name, 'w')

for i, u in zip(ids, urls):
    # prepare
    payload['url'] = u # adds currents url to post
    api_url = api_url_pre + i

    # call curl command
    r = requests.post(api_url, data=json.dumps(payload), headers=headers)
    response = r.content
    status_code = r.status_code

    log.write(str(status_code) + " " + i + " " + u + " " + timenow + '\n')
    print i + " " + u
    print response
    print status_code

    # Error-handling 2nd Try
    if status_code == 404:
        print "\nFile not found\n"

'''
    # Error-handling
    if response == {'response': 'BAD_AUTHENTICATION'}:
        print "\n\rRenew OAuth2 key!\n\r"
    if response != "OK":
        print "ERROR: " + i + "\n"
        # log in error document
        err_log.write("ERROR: " + i + " " + strftime("%Y-%m-%d %H:%M:%S") + '\n')
    break
'''

log.close()

print "...\n\r\n\rDone."

