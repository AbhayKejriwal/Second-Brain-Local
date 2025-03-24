**How to work with the Notion API in Python - Python Engineer**

**Guide on how to work with the Notion API in Python and automate database editing.**

[Python](https://www.python-engineer.com/tags/#python) [API](https://www.python-engineer.com/tags/#api)

https://www.python-engineer.com/posts/notion-api-python/

* * *

Learn how to work with the Notion API in Python. In this guide we go over:

- How to set up the Notion API
- How to set up the Python code
- How to create database entries
- How to query the database
- How to update database entries
- And how to delete entries.

## Setting up the Notion API and a Database[¶](#setting-up-the-notion-api-and-a-database "Permanent link")

First, let's create a full page database in our Notion board. In this tutorial I use a real example from one of my own databases that automatically stores my blog posts whenever I publish a new one. The database has the fields `URL`, `Title`, and `Published`, and demonstates how to edit text and date fields:

<img width="688" height="434" src="../../../../_resources/notion-database_7d946e2671ae405b9371b9133c8405e6.png" class="jop-noMdConv">

Next, follow the official guide to [Create a Notion Integration](https://developers.notion.com/docs/create-a-notion-integration). Following all steps in this page you will:

- Create an integration and get a Token
- Share your database with your integration
- Save the database ID

Now we are ready to automate things in this database with create, read, update, and delete functions.

## Set up the Python code[¶](#set-up-the-python-code "Permanent link")

To work with the API, we work with the `requests` module. We can install it with pip:

`<span style="color: #36464e;">pip</span> <span style="color: #36464e;">install</span> <span style="color: #36464e;">requests</span>`

Define your token, database ID, and the headers like this. You can find the latest Notion version in the [official docs](https://developers.notion.com/reference/post-database-query).

```Python
import requests

NOTION_TOKEN = "YOUR_INTEGRATION_TOKEN"
DATABASE_ID = "YOUR_DATABASE_ID"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}
```

## Creating pages in your Notion database[¶](#creating-pages-in-your-notion-database "Permanent link")

To create a new page, we send a `POST` request:

```Python
def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    # print(res.status_code)
    return res
```

The corresponding data fields have to correspond to your table column names.

The schema might look a bit complicated and differs for different data types (e.g. text, date, boolean etc.). To determine the exact schema, I recommend dumping the data (see next step) and inspecting the JSON file.

In our example, we create data for the `URL`, the `Title`, and the `Published` columns like so:

```Python
from datetime import datetime, timezone

title = "Test Title"
description = "Test Description"
published_date = datetime.now().astimezone(timezone.utc).isoformat()
data = {
    "URL": {"title": [{"text": {"content": description}}]},
    "Title": {"rich_text": [{"text": {"content": title}}]},
    "Published": {"date": {"start": published_date, "end": None}}
}

create_page(data)
```

## Querying Notion database and reading pages[¶](#querying-notion-database-and-reading-pages "Permanent link")

To query your database and read all entries, we can use the following function. It uses pagination to retrieve all entries:

```Python
def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    # Comment this out to dump all data to a file
    # import json
    # with open('db.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results
```

Then we can retrieve all pages, iterate over them, and access the different fields:

```
pages = get_pages()

for page in pages:
    page_id = page["id"]
    props = page["properties"]
    url = props["URL"]["title"][0]["text"]["content"]
    title = props["Title"]["rich_text"][0]["text"]["content"]
    published = props["Published"]["date"]["start"]
    published = datetime.fromisoformat(published)
```

## Updating pages in your Notion databse[¶](#updating-pages-in-your-notion-databse "Permanent link")

To update a page, we have to send a `PATCH` request:

```
def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": data}

    res = requests.patch(url, json=payload, headers=headers)
    return res
```

For example, if we want to update the `Published` field, we send the following data. It is the same schema as for creating the page:

```
page_id = "the page id"

new_date = datetime(2023, 1, 15).astimezone(timezone.utc).isoformat()
update_data = {"Published": {"date": {"start": new_date, "end": None}}}

update_page(page_id, update_data)
```

## Deleting pages in your Notion database[¶](#deleting-pages-in-your-notion-database "Permanent link")

Deleting a page is achieved with the same endpoint as for updating the page, but here we set the `archived` parameter to `True`:

```
def delete_page(page_id: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"archived": True}

    res = requests.patch(url, json=payload, headers=headers)
    return res
```

## Further references[¶](#further-references "Permanent link")

And that's it. To learn more, you can check out the following official Notion links:

- [Geting Started Docs](https://developers.notion.com/docs/getting-started)
- [API Reference](https://developers.notion.com/reference/intro)

* * *

FREE VS Code / PyCharm Extensions I Use

✅ Write cleaner code with Sourcery, instant refactoring suggestions: [Link\*](https://sourcery.ai/?utm_source=youtube&utm_campaign=pythonengineer)

* * *

PySaaS: The Pure Python SaaS Starter Kit

🚀 Build a software business faster with pure Python: [Link\*](https://www.python-engineer.com/go/pysaas)

\* These are affiliate link. By clicking on it you will not have any additional costs. Instead, you will support my project. Thank you! 🙏

* * *