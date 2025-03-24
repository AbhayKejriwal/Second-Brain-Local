&nbsp;

https://www.geeksforgeeks.org/how-to-read-emails-from-gmail-using-gmail-api-in-python/

In this article, we will see how to read Emails from your Gmail using Gmail API in Python. Gmail API is a RESTful API that allows users to interact with your Gmail account and use its features with a Python script.

So, let’s go ahead and write a simple Python script to read emails.

### Requirements

- Python (2.6 or higher)
- A Google account with Gmail enabled
- Beautiful Soup library
- Google API client and Google OAuth libraries

### Installation

Install the required libraries by running these commands:

> pip install –upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

Run this to install Beautiful Soup:

> pip install beautifulsoup4

Now, you have to set up your Google Cloud console to interact with the Gmail API. So, follow these steps:

- Sign in to [Google Cloud console](https://console.cloud.google.com/) and create a **New Project** or continue with an existing project.

![](1-300x234_25e9d1215a5f49219be8a40b2d62f54e.jpg)

Create a New Project

- Go to **APIs and Services**.

![](2-300x169_a0c4993ab0e54dc4aa112bbac2b8ba60.jpg)

Go to APIs and Services

- Enable **Gmail API** for the selected project.

![](3-300x173_5da8372a3a8a4f828eb19ce68f13be7c.jpg)

Go to Enable APIs and Services

![](4-300x181_e5d5cbd1190b48b0a0911a9086823edc.jpg)

Enable Gmail API

- Now, configure the Consent screen by clicking on **OAuth Consent Screen** if it is not already configured.

![](5-300x165_f2bb38350ae5467e8b0a8de02ca89d33.jpg)

Configure Consent screen

- Enter the Application name and save it.

![](6-300x190_da11f714b7a248f0a4832c7d00e79483.jpg)

Enter Application name

- Now go to **Credentials**.

![](7-300x193_aa8ea055afa74b279eea361ea95f1d3e.jpg)

Go to Credentials

- Click on **Create credentials**, and go to **OAuth Client ID**.

![](8-300x172_359926d66a314f5a84fe467cb7be8a25.jpg)

Create an OAuth Client ID

- Choose application type as Desktop Application.
- Enter the Application name, and click on the Create button.
- The Client ID will be created. Download it to your computer and save it as **credentials.json**

![](9-300x187_c0ce6300a8e64785bdfcfc53b134a1ab.jpg)

**Please keep your Client ID and Client Secrets confidential.**

Now, everything is set up, and we are ready to write the code. So, let’s go.

### Code

**Approach :**

The file ‘**token.pickle**‘ contains the User’s access token, so, first, we will check if it exists or not. If it does not exist or is invalid, our program will open up the browser and ask for access to the User’s Gmail and save it for next time. If it exists, we will check if the token needs to be refreshed and refresh if needed.

Now, we will connect to the **Gmail API** with the access token. Once connected, we will request a list of messages. This will return a list of **ID**s of the last 100 emails (default value) for that Gmail account. We can ask for any number of Emails by passing an optional argument ‘**maxResults**‘.

The output of this request is a dictionary in which the value of the key ‘**messages**‘ is a list of dictionaries. Each dictionary contains the **ID** of an Email and the **Thread** **ID**.

Now, We will go through all of these dictionaries and request the Email’s content through their **IDs**.

This again returns a dictionary in which the key ‘**payload**‘ contains the main content of Email in form of Dictionary.

This dictionary contains ‘**headers**‘, ‘**parts**‘, ‘**filename**‘ etc. So, we can now easily find headers such as **sender**, **subject**, etc. from here. The key ‘**parts**‘ which is a list of dictionaries contains all the parts of the Email’s body such as **text**, **HTML**, Attached file details, etc. So, we can get the body of the Email from here. It is generally in the first element of the list.

The body is encoded in **Base 64** encoding. So, we have to convert it to a readable format. After decoding it, the obtained text is in ‘**lxml**‘. So, we will parse it using the **BeautifulSoup** library and convert it to text format.

At last, we will print the **Subject**, **Sender**, and **Email**.

- Python3

## Python3

```Python
# import the required libraries 
from googleapiclient.discovery import build 
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request 
import pickle 
import os.path 
import base64 
import email 
from bs4 import BeautifulSoup 

# Define the SCOPES. If modifying it, delete the token.pickle file. 
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'] 

def getEmails(): 
    # Variable creds will store the user access token. 
    # If no valid token found, we will create one. 
    creds = None

    # The file token.pickle contains the user access token. 
    # Check if it exists 
    if os.path.exists('token.pickle'): 

        # Read the token from the file and store it in the variable creds 
        with open('token.pickle', 'rb') as token: 
            creds = pickle.load(token) 

    # If credentials are not available or are invalid, ask the user to log in. 
    if not creds or not creds.valid: 
        if creds and creds.expired and creds.refresh_token: 
            creds.refresh(Request()) 
        else: 
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES) 
            creds = flow.run_local_server(port=0) 

        # Save the access token in token.pickle file for the next run 
        with open('token.pickle', 'wb') as token: 
            pickle.dump(creds, token) 

    # Connect to the Gmail API 
    service = build('gmail', 'v1', credentials=creds) 

    # request a list of all the messages 
    result = service.users().messages().list(userId='me').execute() 

    # We can also pass maxResults to get any number of emails. Like this: 
    # result = service.users().messages().list(maxResults=200, userId='me').execute() 
    messages = result.get('messages') 

    # messages is a list of dictionaries where each dictionary contains a message id. 

    # iterate through all the messages 
    for msg in messages: 
        # Get the message from its id 
        txt = service.users().messages().get(userId='me', id=msg['id']).execute() 

        # Use try-except to avoid any Errors 
        try: 
            # Get value of 'payload' from dictionary 'txt' 
            payload = txt['payload'] 
            headers = payload['headers'] 

            # Look for Subject and Sender Email in the headers 
            for d in headers: 
                if d['name'] == 'Subject': 
                    subject = d['value'] 
                if d['name'] == 'From': 
                    sender = d['value'] 

            # The Body of the message is in Encrypted format. So, we have to decode it. 
            # Get the data and decode it with base 64 decoder. 
            parts = payload.get('parts')[0] 
            data = parts['body']['data'] 
            data = data.replace("-","+").replace("_","/") 
            decoded_data = base64.b64decode(data) 

            # Now, the data obtained is in lxml. So, we will parse 
            # it with BeautifulSoup library 
            soup = BeautifulSoup(decoded_data , "lxml") 
            body = soup.body() 

            # Printing the subject, sender's email and message 
            print("Subject: ", subject) 
            print("From: ", sender) 
            print("Message: ", body) 
            print('\n') 
        except: 
            pass


getEmails()
```

Now, run the script with

python3 email_reader.py

This will attempt to open a new window in your default browser. If it fails, copy the URL from the console and manually open it in your browser.

Now, Log in to your Google account if you aren’t already logged in. If there are multiple accounts, you will be asked to choose one of them. Then, click on the **Allow** button.

![](10-233x300_4b057209ccbf4314a3277fb0caef7191.jpg)

Your Application asking for Permission

After the authentication has been completed, your browser will display a message: “The authentication flow has been completed. You may close this window”.

The script will start printing the Email data in the console.

You can also extend this and save the emails in separate text or csv files to make a collection of Emails from a particular sender.

Don't miss your chance to ride the wave of the data revolution! Every industry is scaling new heights by tapping into the power of data. Sharpen your skills and become a part of the hottest trend in the 21st century.

Dive into the future of technology - explore the [Complete Machine Learning and Data Science Program](https://www.geeksforgeeks.org/courses/data-science-live?utm_source=geeksforgeeks&utm_medium=article_bottom_text&utm_campaign=courses) by GeeksforGeeks and stay ahead of the curve.

Last Updated : 01 Oct, 2020

Like Article

Save Article

[](#)Share your thoughts in the comments