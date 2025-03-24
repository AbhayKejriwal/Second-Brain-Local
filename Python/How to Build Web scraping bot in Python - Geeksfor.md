https://www.geeksforgeeks.org/how-to-build-web-scraping-bot-in-python/

In this article, we are going to see how to build a web scraping bot in Python.

Web Scraping is a process of extracting data from websites. A Bot is a piece of code that will automate our task. Therefore, A web scraping bot is a program that will automatically scrape a website for data, based on our requirements.

## Module needed

- [**bs4**](https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/)**:** Beautiful Soup(bs4) is a Python library for pulling data out of HTML and XML files. This module does not come built-in with Python. To install this type the below command in the terminal.

> pip install bs4

- [**requests**](https://www.geeksforgeeks.org/python-requests-tutorial/)**:** Request allows you to send HTTP/1.1 requests extremely easily. This module also does not come built-in with Python. To install this type the below command in the terminal.

> pip install requests

- [**Selenium**](https://www.geeksforgeeks.org/selenium-basics-components-features-uses-and-limitations/)**:** Selenium is one of the most popular automation testing tools. It can be used to automate browsers like Chrome, Firefox, Safari, etc.

> pip install selenium

## **Method 1:** **Using Selenium**

We need to install a [chrome driver](https://chromedriver.chromium.org/home) to automate using selenium, our task is to create a bot that will be continuously scraping the google news website and display all the headlines every 10mins.

### Stepwise **implementation:**

**Step 1:** First we will import some required modules.

- Python3

> `import` `time`
> 
> `from` `selenium` `import` `webdriver`
> 
> `from` `datetime` `import` `datetime`

**Step 2:** The next step is to open the required website.

> - Python3
>     
>     `# path of the chromedriver we have just downloaded`  
>     `PATH = r"D:\chromedriver"`  
>     `driver = webdriver.Chrome(PATH) # to open the browser`
>     
>     `# url of google news website`  
>     `url = 'https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en'`
>     
>     `# to open the url in the browser`  
>     `driver.get(url)`
>     

**Output:**

![](Capture-558x660_d3a2b8826d8b483b8776ea7a325e6662.png)

**Step 3:** Extracting the news title from the webpage, to extract a specific part of the page, we need its XPath, which can be accessed by right-clicking on the required element and selecting Inspect in the dropdown bar.

<img width="770" height="495" src="../../../../_resources/2021082900h2028_d395da46416e49ec988d52bafd904b9b.png" class="jop-noMdConv">

After clicking Inspect a window appears. From there, we have to copy the elements full XPath to access it:

<img width="770" height="291" src="../../../../_resources/2021082900h2351_e1790d388fc24988b3f9ddc18176bfbb.jpg" class="jop-noMdConv">

**Note:** You might not always get the exact element that you want by inspecting (depends on the structure of the website), so you may have to surf the HTML code for a while to get the exact element you want.  And now, just copy that path and paste that into your code. After running all these lines of code, you will get the title of the first heading printed on your terminal.

- Python3

> `news_path` `=` `'``/``html``/``body``/``c``-``wiz``/``div``/``div[``2``]``/``div[``2``]``/``\`
> 
> `div``/``main``/``c``-``wiz``/``div[``1``]``/``div[``3``]``/``div``/``div``/``article``/``h3``/``a'`
> 
> `link` `=` `driver.find_element_by_xpath(news_path)`
> 
> `print``(link.text)`

**Output:**

> ‘Attack on Afghan territory’: Taliban on US airstrike that killed 2 ISIS-K men

**Step 4:** Now, the target is to get the X_Paths of all the headlines present.

One way is that we can copy all the XPaths of all the headlines (about 6 headlines will be there in google news every time) and we can fetch all those, but that method is not suited if there are a large number of things to be scrapped. So, the elegant way is to find the pattern of the XPaths of the titles which will make our tasks way easier and efficient.  Below are the XPaths of all the headlines on the website, and let’s figure out the pattern.

> /html/body/c-wiz/div/div\[2\]/div\[2\]/div/main/c-wiz/div\[1\]/div\[**3**\]/div/div/article/h3/a
> 
> /html/body/c-wiz/div/div\[2\]/div\[2\]/div/main/c-wiz/div\[1\]/div\[**4**\]/div/div/article/h3/a
> 
> /html/body/c-wiz/div/div\[2\]/div\[2\]/div/main/c-wiz/div\[1\]/div\[**5**\]/div/div/article/h3/a
> 
> /html/body/c-wiz/div/div\[2\]/div\[2\]/div/main/c-wiz/div\[1\]/div\[**6**\]/div/div/article/h3/a
> 
> /html/body/c-wiz/div/div\[2\]/div\[2\]/div/main/c-wiz/div\[1\]/div\[**7**\]/div/div/article/h3/a
> 
> /html/body/c-wiz/div/div\[2\]/div\[2\]/div/main/c-wiz/div\[1\]/div\[**8**\]/div/div/article/h3/a

So, by seeing these XPath’s, we can see that only the 5th div is changing (bolded ones). So based upon this, we can generate the XPaths of all the headlines. We will get all the titles from the page by accessing them with their XPath. So to extract all these, we have the code as

- Python3

`c` `=` `1`

`for` `x` `in` `range``(``3``,` `9``):`

&nbsp;

`print``(f``"Heading {c}: "``)`

&nbsp;

`c` `+``=` `1`

&nbsp;

`curr_path` `=` `f'``/``html``/``body``/``c``-``wiz``/``div``/``div[``2``]``/``div[``2``]``/``div``/``main\`

&nbsp;

`/``c``-``wiz``/``div[``1``]``/``div[{x}]``/``div``/``div``/``article``/``h3``/``a'`

&nbsp;

`title` `=` `driver.find_element_by_xpath(curr_path)`

&nbsp;

`print``(title.text)`

**Output:**

![](Capture-660x195_690ecafa3f574af69b3d59046cb92768.png)

Now, the code is almost complete, the last thing we have to do is that the code should get headlines for every 10 mins. So we will run a while loop and sleep for 10 mins after getting all the headlines.

**Below is the full implementation**

- Python3

`import` `time`

`from` `selenium` `import` `webdriver`

`from` `datetime` `import` `datetime`

`PATH` `=` `r``"D:\chromedriver"`

`driver` `=` `webdriver.Chrome(PATH)`

`driver.get(url)`

`while``(``True``):`

&nbsp;

`now` `=` `datetime.now()`

&nbsp;

`current_time` `=` `now.strftime(``"%H:%M:%S"``)`

&nbsp;

`print``(f``'At time : {current_time} IST'``)`

&nbsp;

`c` `=` `1`

&nbsp;

`for` `x` `in` `range``(``3``,` `9``):`

&nbsp;

`curr_path` `=` `''`

&nbsp;

`try``:`

&nbsp;

`curr_path` `=` `f'``/``html``/``body``/``c``-``wiz``/``div``/``div[``2``]``/``div[``2``]``/``\`

&nbsp;

`div``/``main``/``c``-``wiz``/``div[``1``]``/``div[{x}]``/``div``/``div``/``article``/``h3``/``a'`

&nbsp;

`title` `=` `driver.find_element_by_xpath(curr_path)`

&nbsp;

`except``:`

&nbsp;

`continue`

&nbsp;

`print``(f``"Heading {c}: "``)`

&nbsp;

`c` `+``=` `1`

&nbsp;

`print``(title.text)`

&nbsp;

`time.sleep(``600``)`

**Output:**

![](Capture-660x177_bcf36427298343b1be031a2a45267e74.png)

## Method 2: Using Requests and BeautifulSoup

The requests module gets the raw HTML data from websites and beautiful soup is used to parse that information clearly to get the exact data we require. Unlike Selenium, there is no browser installation involved and it is even lighter because it directly accesses the web without the help of a browser.

### **Stepwise implementation:**

**Step 1:** Import module.

- Python3

`import` `requests`

`from` `bs4` `import` `BeautifulSoup`

`import` `time`

**Step 2:** The next thing to do is to get the URL data and then parse the HTML code

- Python3

**Step 3:** First, we shall get all the headings from the table.

- Python3

`headings` `=` `data.find_all(``'tr'``)[``0``]`

`headings_list` `=` `[]`

`for` `x` `in` `headings:`

&nbsp;

`headings_list.append(x.text)`

`headings_list` `=` `headings_list[:``10``]`

`print``(``'Headings are: '``)`

`for` `column` `in` `headings_list:`

&nbsp;

`print``(column)`

**Output:**

![](Capture_541cca419b5548aab1dd6ebfbaf7a314.png)

**Step 4:** In the same way, all the values in each row can be obtained

- Python3

`for` `x` `in` `range``(``1``,` `6``):`

&nbsp;

`table` `=` `data.find_all(``'tr'``)[x]`

&nbsp;

`c` `=` `table.find_all(``'td'``)`

&nbsp;

`for` `x` `in` `c:`

&nbsp;

`print``(x.text, end``=``' '``)`

&nbsp;

`print``('')`

**Output:**

![](Capture_1285e25e3dd44ab2b319ffbf36850051.png)

**Below is the full implementation:**

- Python3

`import` `requests`

`from` `bs4` `import` `BeautifulSoup`

`from` `datetime` `import` `datetime`

`import` `time`

`while``(``True``):`

&nbsp;

`now` `=` `datetime.now()`

&nbsp;

`current_time` `=` `now.strftime(``"%H:%M:%S"``)`

&nbsp;

`print``(f``'At time : {current_time} IST'``)`

&nbsp;

`text` `=` `response.text`

&nbsp;

`html_data` `=` `BeautifulSoup(text,` `'html.parser'``)`

&nbsp;

`headings` `=` `html_data.find_all(``'tr'``)[``0``]`

&nbsp;

`headings_list` `=` `[]`

&nbsp;

`for` `x` `in` `headings:`

&nbsp;

`headings_list.append(x.text)`

&nbsp;

`headings_list` `=` `headings_list[:``10``]`

&nbsp;

`data` `=` `[]`

&nbsp;

`for` `x` `in` `range``(``1``,` `6``):`

&nbsp;

`row` `=` `html_data.find_all(``'tr'``)[x]`

&nbsp;

`column_value` `=` `row.find_all(``'td'``)`

&nbsp;

`dict` `=` `{}`

&nbsp;

`for` `i` `in` `range``(``10``):`

&nbsp;

`dict``[headings_list[i]]` `=` `column_value[i].text`

&nbsp;

`data.append(``dict``)`

&nbsp;

`for` `coin` `in` `data:`

&nbsp;

`print``(coin)`

&nbsp;

`print``('')`

&nbsp;

`time.sleep(``600``)`

**Output:**

<img width="770" height="270" src="../../../../_resources/Capture_890b6ace83cc418381dfe04d7149462d.png" class="jop-noMdConv">

## Hosting the Bot

This is a specific method, used to run the bot continuously online without the need for any human intervention.  replit.com is an online compiler, where we will be running the code. We will be creating a mini webserver with the help of a flask module in python that helps in the continuous running of the code. Please create an account on that website and create a new repl.

<img width="770" height="337" src="../../../../_resources/2021083012h5150_807dab9360a8454bbd713e22013ad323.png" class="jop-noMdConv">

After creating the repl, Create two files, one to run the bot code and the other to create the web server using flask.

**Code for cryptotracker.py:**

- Python3

`import` `requests`

`from` `bs4` `import` `BeautifulSoup`

`from` `datetime` `import` `datetime`

`import` `time`

`from` `keep_alive` `import` `keep_alive`

`import` `pytz`

`keep_alive()`

`while``(``True``):`

&nbsp;

`tz_NY` `=` `pytz.timezone(``'Asia/Kolkata'``)`

&nbsp;

`datetime_NY` `=` `datetime.now(tz_NY)`

&nbsp;

`current_time` `=` `datetime_NY.strftime(``"%H:%M:%S - (%d/%m)"``)`

&nbsp;

`print``(f``'At time : {current_time} IST'``)`

&nbsp;

`text` `=` `response.text`

&nbsp;

`html_data` `=` `BeautifulSoup(text,` `'html.parser'``)`

&nbsp;

`headings` `=` `html_data.find_all(``'tr'``)[``0``]`

&nbsp;

`headings_list` `=` `[]`

&nbsp;

`for` `x` `in` `headings:`

&nbsp;

`headings_list.append(x.text)`

&nbsp;

`headings_list` `=` `headings_list[:``10``]`

&nbsp;

`data` `=` `[]`

&nbsp;

`for` `x` `in` `range``(``1``,` `6``):`

&nbsp;

`row` `=` `html_data.find_all(``'tr'``)[x]`

&nbsp;

`column_value` `=` `row.find_all(``'td'``)`

&nbsp;

`dict` `=` `{}`

&nbsp;

`for` `i` `in` `range``(``10``):`

&nbsp;

`dict``[headings_list[i]]` `=` `column_value[i].text`

&nbsp;

`data.append(``dict``)`

&nbsp;

`for` `coin` `in` `data:`

&nbsp;

`print``(coin)`

&nbsp;

`time.sleep(``60``)`

**Code for the keep_alive.py (webserver):**

- Python3

`from` `flask` `import` `Flask`

`from` `threading` `import` `Thread`

`app` `=` `Flask('')`

`@app``.route(``'/'``)`

`def` `home():`

&nbsp;

`return` `"Hello. the bot is alive!"`

`def` `run():`

&nbsp;

`app.run(host``=``'0.0.0.0'``,port``=``8080``)`

`def` `keep_alive():`

&nbsp;

`t` `=` `Thread(target``=``run)`

&nbsp;

`t.start()`

Keep-alive is a method in networking that is used to prevent a certain link from breaking. Here the purpose of the keep-alive code is to create a web server using flask, that will keep the thread of the code (crypto-tracker code) to be active so that it can give the updates continuously.

<img width="770" height="353" src="../../../../_resources/2021083013h0038_247de46118f84b05bbf6c5519e016bb2.jpg" class="jop-noMdConv">

Now, we have a web server create, and now, we need something to ping it continuously so that the server does not go down and the code keeps on running continuously. There is a website uptimerobot.com that does this job. Create an account in it

<img width="770" height="437" src="../../../../_resources/2021083014h0833_be76d4afe02547b1b95c9918a55caa00.jpg" class="jop-noMdConv">

Running the Crypto tracker code in Replit. Thus, We have successfully created a web scraping bot that will scrap the particular website continuously for every 10 mins and print the data to the terminal.

Don't miss your chance to ride the wave of the data revolution! Every industry is scaling new heights by tapping into the power of data. Sharpen your skills and become a part of the hottest trend in the 21st century.

Dive into the future of technology - explore the [Complete Machine Learning and Data Science Program](https://www.geeksforgeeks.org/courses/data-science-live?utm_source=geeksforgeeks&utm_medium=article_bottom_text&utm_campaign=courses) by GeeksforGeeks and stay ahead of the curve.

Last Updated : 02 Feb, 2022

Like Article

Save Article

[](#)Share your thoughts in the comments