# Python | Automate Google Search using Selenium - GeeksforGeeks

Google search can be automated using Python script in just 2 minutes. This can be done using **`selenium`** (a browser automation tool). Selenium is a portable framework for testing web applications. It can automatically perform the same interactions that any you need to perform manually and this is a small example of it. Mastering Selenium will help you automate your day to day tasks like controlling your tweets, Whatsapp texting and even just googling without actually opening a browser in just 15-30 lines of python code. The limits of automation is endless with selenium.

## Installation

1.  **Selenium**
    
    pip install selenium
    
2.  **Chrome browser**
    
3.  **Chromedriver** Download the chrome browser from [here](https://chromedriver.chromium.org/downloads) (choose the version for your system) After downloading, extract it and then copy the file in the folder of the script.
    

This can be done in two ways, by taking input from the user and by giving input in the command line itself. **\# Method 1** Asking the user for input.

`from` `selenium` `import` `webdriver`

`search_string` `=` `input``(``"Input the URL or string you want to search for:"``)`

`search_string` `=` `search_string.replace(``' '``,` `'+'``)`

`browser` `=` `webdriver.Chrome(``'chromedriver'``)`

`for` `i` `in` `range``(``1``):`

&nbsp;

`search_string` `+` `"&start="` `+` `str``(i))`

After saving the above script in script.py, run it in the command prompt as:

python script.py

**\# Method 2** Taking search string in the command line itself.

`from` `selenium` `import` `webdriver`

`import` `sys`

`def` `convert(s):`

&nbsp;

`str1` `=` `""`

&nbsp;

`return``(str1.join(s))`

`search_string` `=` `sys.argv[``1``:]`

`search_string` `=` `convert(search_string)`

`search_string` `=` `search_string.replace(``' '``,` `'+'``)`

`browser` `=` `webdriver.Chrome(``'chromedriver'``)`

`for` `i` `in` `range``(``1``):`

&nbsp;

`search_string` `+` `"&start="` `+` `str``(i))`

After saving the above script in script.py, run it in the command prompt as:

python script.py "geeksforgeeks"

Don't miss your chance to ride the wave of the data revolution! Every industry is scaling new heights by tapping into the power of data. Sharpen your skills and become a part of the hottest trend in the 21st century.

Dive into the future of technology - explore the [Complete Machine Learning and Data Science Program](https://www.geeksforgeeks.org/courses/data-science-live?utm_source=geeksforgeeks&utm_medium=article_bottom_text&utm_campaign=courses) by GeeksforGeeks and stay ahead of the curve.

Last Updated : 11 May, 2020

Like Article

Save Article

[](#)Share your thoughts in the comments