# Email Bot with Google Sheets and Gmail 
You only need to do these steps once, and then you can write and run 
as many email / spreadsheet bots as you'd like. You can also access all other
Google services through Python.

Last updated 3/24/2022.

1. Install Dependencies with pip:

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

2. Head to the [Google Cloud Console](console.cloud.google.com)

3. Click "Select Project"

![Select Project](/images/select_project.png)

4. Create a new project and give it a name. You may need to browse
for a location to put the project under.

![New Project](/images/new_project.png)

5. On the left-hand side, click APIs and Services -> Credentials. Create
a new OAuth 2.0 Credential. You will need to configure a consent screen first.

![Oauth First](/images/create_oauth_key.png)

6. On the consent screen configuration, select "External", but if your Google account is part of 
an organization like Berkeley or LBL, you can press "Internal", and it's easier. 
Fill out the rest of the
information on the first screen. On the "scopes" page, don't select any scopes. 
On the "Test Users" page (which will only appear if you clicked "External"), type in your own email
address.

![Oauth Screen](/images/oauth_consent.png)

7. Go back to Credentials on the left hand pane; you can now create a new Oauth key without
interruption. Name the credential something arbtrary. You will get to a screen as shown below, that
will let you download your credentials as a json. Download the json credentials file
and save it in the same directory as the email / spreadsheet bot with the name "credentials.json".

![Oauth Second](/images/create_oauth_second_time.png)

8. Click "Enabled APIs and Services -> Library" from the left-hand pane. You can also search this in 
the taskbar at the top.

![Library](/images/library.png)

9. Search and enable the Gmail API (first search result, click on it, enable).

![Gmail](/images/gmail_api.png)

10. Search and enable the Google Sheets API (same as above)

![Sheets](/images/sheets_api.png)

11. Run the email bot using Python! You can find the ID of a
Google spreadsheet in the URL bar, as shown in the image below,
right after /d/ and before /view or /edit; it's the long string
of characters (there's an example below the picture). 

![spreadsheet_iud](/images/spreadsheet_id.png)

Once you
run the program from your terminal, you will be prompted to log into
your Google account on a browser (the token is then cached, so
you won't have to do this multiple times. You must reauthenticate
if you add scopes / permissions). This email bot will wait two
seconds between each email to avoid triggering spam detection.

The command below has a publicly available example spreadsheet;
copy this spreadsheet, replace the values, and provide the
new spreadsheet ID to the bot. Here is the 
[example spreadsheet](https://docs.google.com/spreadsheets/d/1MrcX6Go1F4B9ZC7_0FaPyn6PZGwljWht-0gk_tUg8vw/edit?usp=sharing).

```
python3 email_bot.py example_sender@xyz.org 1MrcX6Go1F4B9ZC7_0FaPyn6PZGwljWht-0gk_tUg8vw
```


