# How to Use PyScript – A Python Frontend Framework

<img width="1060" height="316" src="../../../../_resources/Screenshot-2022-05-26-at-13.28.4_0b79ebd6f1d74098b.png" class="jop-noMdConv">

Python has grown in popularity immensely in recent years. It has a wide range of applications, from its most popular use in Artificial Intelligence, to Data Science, Robotics, and Scripting.

In the web development field, Python is used mainly on the backend with frameworks such as Django and Flask.

Before now, Python didn't have much support on the front-end side like other languages such as JavaScript. But thankfully, Python developers have built some libraries (such as [Brython](https://brython.info/)) to support their favourite language on the web.

And this year, during the [PyCon 2022 conference](https://youtube.com/playlist?list=PL2Uw4_HvXqvYeXy8ab7iRHjA-9HiYhRQl), Anaconda announced a framework named PyScript that allows you to use Python on the web using standard HTML.

You can check out this tweet about the launch:

## Prerequisites

You'll need the following tools and knowledge to code along with this article:

- A text editor or IDE of your choice.
- Knowledge of Python.
- Knowledge of HTML.
- A browser (Google Chrome is the recommended browser for PyScript).

## What is PyScript?

![Image from PyScript's website.](Screenshot-2022-05-22-at-18.29.4_00554d57346347c4b.png)

Source: [PyScript official website](https://pyscript.net/)

PyScript is a Python front-end framework that enables users to construct Python programs using an HTML interface in the browser.

It was developed using the power of [Emscripten](https://emscripten.org/), [Pyodide](https://pyodide.org/en/stable/), [WASM](https://webassembly.org/), and other modern web technologies to provide the following abilities in line with its goals:

- To provide a simplistic and clean API.
- To provide a system of pluggable and extensible components.
- To support and extend standard HTML to read opinionated and dependable custom components in order to reach the mission “Programming for the 99%.”

<img width="720" height="252" src="../../../../_resources/Screenshot-2022-05-26-at-11.27.0_38ece412ee2c49aca.png" class="jop-noMdConv">

Source: [Anaconda Blog](https://www.anaconda.com/blog/pyscript-python-in-the-browser)

In the last couple of decades, Python and advanced UI languages like modern HTML, CSS, and JavaScript have not worked in collaboration. Python lacked a simple mechanism to create appealing UIs for simply packaging and deploying apps, while current HTML, CSS, and JavaScript can have a steep learning curve.

Allowing Python to utilize HTML, CSS, and JavaScript conventions solves not only those two problems but also those related to web application development, packaging, distribution, and deployment.

PyScript isn't meant to take the role of JavaScript in the browser, though – rather, it's meant to give Python developers, particularly data scientists, more flexibility and power.

## Why PyScript?

PyScript gives you a programming language with consistent styling conventions, more expressiveness, and ease of learning by providing the following:

- **Support on the browser:** PyScript enables support for Python and hosting without the need for servers or configuration.
- **Interoperability:** Programs can communicate bi-directionally between Python and JavaScript objects and namespaces.
- **Ecosystem support:** PyScript allows the use of popular Python packages such as Pandas, NumPy, and many more.
- **Framework flexibility:** PyScript is a flexible framework that developers can build on to create extensible components directly in Python easily.
- **Environment Management:** PyScript allows developers to define the files and packages to include in their page code to run.
- **UI Development:** With PyScript, developers can easily build with available UI components such as buttons and containers, and many more.

## How to Get Started with PyScript

PyScript is fairly easy and straightforward to learn. To get started, you can either follow the instructions on the [website](https://pyscript.net/) or download the [.zip](https://github.com/pyscript/pyscript/archive/refs/heads/main.zip) file.

In this article, we'll be using and learning how to use PyScript via the [website](https://pyscript.net/). You can do this by linking the components in your HTML file. Let’s print our first “Hello World” with PyScript.

### Create an HTML file

To begin, you'll need to create an HTML file to display text on your browser using the text editor/IDE of your choice.

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Title: PyScript</title>
</head>
<body>

</body>
</html>
```

### Link PyScript

After creating the HTML file, we'll need to link PyScript in your HTML file to have access to the PyScript interface. This will be placed in the `<head>` tag.

```
<link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css" />
<script defer src="https://pyscript.net/alpha/pyscript.js"></script>
```

### Print to browser

Now that you've linked PyScript to the HTML file, you can print your “Hello World”.

You can do this with the `<py-script>` tag. The `<py-script>` tag allows you to run multi-line Python programs and have them printed on the browser page. Place the tag in between the `<body>` tags.

```
<body> <py-script> print("Hello, World!") </py-script> </body>
```

The full code for the HTML file is below:

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Title: PyScript</title>
</head>
<body>
    <py-script> print("Hello, World!") </py-script>
</body>
</html>
```

On your browser, you should see this:

![Image of the "Hello, World" on browser.](Screenshot-2022-05-23-at-18.19.4_6bd81ad544ad4714a.png)

**Tip:** If you're using the VSCode editor, you can use the Live Server add-on in [VSCode](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) to reload the page as you update the HTML file.

## More Operations with PyScript

There are more operations you can perform with the PyScript framework. Let's look at some of them now.

### Attach labels to labeled elements

While using PyScript, you might want to pass variables from your Python code to HTML. You can do this with the `write` method from the `pyscript` module within the `<pyscript>` tag. Using the `id` attribute , you get to pass strings displayed as regular text.

The write method accepts two variables: the `id` value and the variable that will be provided.

```
<html>
    <head>
      <link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css" />
      <script defer src="https://pyscript.net/alpha/pyscript.js"></script>
    </head>

  <body>
    <b><p>Today is <u><label id='today'></label></u></p></b>
    <py-script>
import datetime as dt
pyscript.write('today', dt.date.today().strftime('%A %B %d, %Y'))
    </py-script>
  </body>
</html>
```

And the output becomes:

![Image showing the output of a date.](Screenshot-2022-05-24-at-11.07.1_6838bfea18544d69b.png)

### Run REPL in the browser

PyScript provides an interface for running Python code in browsers.

To be able to do this, PyScript uses the `<py-repl>` tag. The `<py-repl>` tag adds a REPL component to the page, which acts as a code editor and allows you to write executable code inline.

```
<html>
  <head>
    <link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css" />
    <script defer src="https://pyscript.net/alpha/pyscript.js"></script>
  </head>
  <py-repl id="my-repl" auto-generate=true> </py-repl>
</html>
```

Trying it out in browser (preferably Chrome), you should get this:

![Python's REPL in browser.](Screenshot-2022-05-24-at-16.14.3_b5f1e0147bc44a2a8.png)

### Import Files, Modules, and Libraries

One of the functions PyScript provides is flexibility. In PyScript you can import local files, inbuilt modules, or third-party libraries. This process uses the `<py-env>` tag. This tag is for declaring the dependencies needed.

For local Python files on your system, you can place the code in a `.py` file and the paths to local modules are provided in the paths: key in the `<py-env>` tag.

Let’s create a Python file `example.py` to contain some functions:

```
from random import randint

def add_two_numbers(x, y):
    return x + y

def generate_random_number():
    x = randint(0, 10)
    return x
```

Then the Python file will be imported into the HTML with the `<py-env>` tag. You should place this tag in the the `<head>` tag, above the `<body>` tag.

```
<html>
    <head>
      <link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css" />
      <script defer src="https://pyscript.net/alpha/pyscript.js"></script>
      <py-env>
        - paths:
          - /example.py
      </py-env>
    </head>

  <body>
    <h1>Let's print random numbers</h1>
    <b>Doe's lucky number is <label id="lucky"></label></b>
    <py-script>
      from example import generate_random_number
      pyscript.write('lucky', generate_random_number())
    </py-script>
  </body>
</html>
```

This will return:

![Printing out random numbers with Python.](Screenshot-2022-05-24-at-23.20.3_f75a2837764b47cb9.png)

For third-party libraries that are not part of the standard library, PyScript supports them.

```
<html>
    <head>
      <link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css" />
      <script defer src="https://pyscript.net/alpha/pyscript.js"></script>
      <py-env>
            - numpy
            - requests
      </py-env>
    </head>

  <body>
    <py-script>
    import numpy as np
    import requests
    </py-script>
  </body>
</html>
```

### Configure metadata

You can set and configure general metadata about your PyScript application in YAML format using the `<py config>` tag. You can use this tag in this format:

```
<py-config>
  - autoclose_loader: false
  - runtimes:
    -
      src: "https://cdn.jsdelivr.net/pyodide/v0.20.0/full/pyodide.js"
      name: pyodide-0.20
      lang: python
</py-config>
```

These are the optional values that the `<py-config>` tag provides. They include:

- **autoclose_loader (boolean):** If this is set to false, PyScript will not close the loading splash screen.
- **name (string):** Name of the user application.
- **version (string):** Version of the user application.
- **runtimes (List of Runtimes):** List of runtime configurations which would have the following fields: src, name, and lang.

## Conclusion

In this article, you learned what PyScript is all about and how to use it in HTML files to run Python code on the browser. You also learned about the various operations/functionalities you can do with PyScript.

With PyScript, it’s easier to run and perform Python operations on the web, as this wasn’t easy before. This is a great tool for anyone who's looking forward to using Python on the web.

PyScript is still in its early stages and under heavy development. It is still in its alpha stage and faces known issues like the load time which can affect usability (some other operations can’t be shown at the time of this writing due to performance issues). So you shouldn't use it in production yet as there will likely be a lot of breaking changes.

## References

- [The PyScript official website](https://pyscript.net/).
- [Anaconda blog](https://www.anaconda.com/blog/pyscript-python-in-the-browser).
- [PyScript source code](https://github.com/pyscript/pyscript).
- [Guide on getting started with PyScript](https://github.com/pyscript/pyscript/blob/main/docs/tutorials/getting-started.md).

* * *

* * *

Learn to code for free. freeCodeCamp's open source curriculum has helped more than 40,000 people get jobs as developers. [](#)[Get started](https://www.freecodecamp.org/learn/)