---
title: "Free Hosting a Python API"
source: "https://medium.com/@produde/free-hosting-a-python-api-632968f14b20#8664"
author:
  - "[[Trần Hoàng Long]]"
published: 2023-01-30
created: 2024-11-25
description: "A few months ago, I encountered a problem while trying to deploy my backend API for a demo of my side project. Which free service would host my python backend? If you had some of the similar…"
tags:
  - "clippings"
---
[

![Trần Hoàng Long](https://miro.medium.com/v2/resize:fill:88:88/1*bw1TxmQ7QaCu-KPlRH4qMw.jpeg)

](https://medium.com/@produde?source=post_page---byline--632968f14b20--------------------------------)

![](https://miro.medium.com/v2/resize:fit:788/0*5BywiJHpjTaIXr2a)

My choice for free python hosting 🎖

## Foreword

A few months ago, I encountered a problem while trying to deploy my backend API for a demo of my side project. **Which free service would host my python backend?**

The criterias/downsides that I had were:

- Must be fully free with no credit card requirement (student problem 😭) *→ So no AWS, Google or Azure or any other virtual machine services*
- I have a database so the server must be able to make DB connections instead of just communicating with frontend
- Of course speed is not my concern since we’re going dirt-tier anyways
- Lastly, of course, the server must support python (duh!) (Django to be specific)

If you had some of the similar problems, this blog could be for you. I’ll discuss some of my findings and workarounds below

> *😓 It was suprisingly hard for me to find a completely free python hosting service. Took lots of trial/error. That’s why I write this post for anyone that likes to save their time digging.*

## TOC

· [Foreword](https://medium.com/@produde/#8664)  
· [TOC](https://medium.com/@produde/#2d58)  
· [Project Description](https://medium.com/@produde/#cc4c)  
∘ [Database](https://medium.com/@produde/#2675)  
∘ [Backend](https://medium.com/@produde/#7aa5)  
∘ [Frontend](https://medium.com/@produde/#5d29)  
· [Hosting Service](https://medium.com/@produde/#64b1)  
· [Render Hosting](https://medium.com/@produde/#5363)  
∘ [Build server](https://medium.com/@produde/#c139)  
∘ [Environment Variables](https://medium.com/@produde/#9d0b)  
∘ [Run server](https://medium.com/@produde/#ac4d)  
· [Demo](https://medium.com/@produde/#37aa)  
· [Final words](https://medium.com/@produde/#cd58)

## Project Description

So here’s a quick layout of my project at the time, called `Geo-covid` , which is basically a visualization website for the covid problem in USA, which consists of 3 parts

## Database

MongoDB is my goto database here due to the implementation simplicity and also the `Mongo Atlas` support for free DB hosting

> *‼️ This (db connection from/to the backend) proven itself to be the trickiest part of the server hosting process*

## Backend

My API implemented with `Python` and `Django REST API`

> *Why Django REST and not Fast API? Well cause I just wanna try Django out for once.*

## Frontend

Web visualization with the help of `Tailwind CSS` and `D3.js` (graph) and `Leaflet` (map)

We don’t focus on the frontend here since free hosting for frontend JS is everywhere and it only make simple request back/forth to our API server.

## Hosting Service

After some trial and error, the two contenders that were the most promising were:

1. `render.com`
2. `pythonanywhere.com`

But in the end, `pythonanywhere` fell short of my need, despite being the more comprehensive and dev friendly service. All because of the previously mention DB connection problem 😮‍💨

> *You see on the* **free tier***,* `*pythonanywhere*` *only allow external connection under the* `*https*` *protocol, so my Mongo Atlas connection is of* `*mongodb://*` *protocol which would simply not work (*[*Link*](https://www.pythonanywhere.com/forums/topic/30407/#id_post_98228)*)*

Thankfully, `render` later prove to work properly, which is good enough 🙏

## Render Hosting

The hosting procedure is very detaily describe on `Render`'s documentation ([Django Quickstart Doc](https://render.com/docs/deploy-django)). So I’m just going to point out notable things from my project

The source code for my backend that’s deployed could be found on my [production branch](https://github.com/produdez/geo-covid-backend/tree/production). And in that branch, I din’t modify any code or add files to config deployment. All were done on `Render` itself (due to the simplicity of my project)

Important steps are:

1. Build: Setup python environment and (optional) build static files
2. Setup production environment variables
3. Run server

## Build server

**Python env**

All we need here is a `requirement.txt` file that we’lll use to install packages when building our source code with `pip install -r requirement.txt`

**Static files**

Static files for `Django` server API GUI could be generated with `python manage.py collectstatic`

**Build**

We put all the needed commands for server preping in the `Build Command` option for Render (found in `Settings > Build & Deploy > Build Command`). I set it as

```
pip install -r requirements.txt && python manage.py collectstatic
```

## Environment Variables

Found in `Environment` tab

First option to set is the `PYTHON_VERSION` (I used `3.9.0`)

For other variables related to my backend, I uploaded my `.env` file directly to Render instead.

This includes:

```
DEBUG=FALSEDB_URL="mongodb+srv://<username>:<password>@<cluster_address>.mongodb.net/?retryWrites=true&w=majority"DEPLOY_ENV=production
```

Here’s how the environment settings looks like

![](https://miro.medium.com/v2/resize:fit:788/0*eMoecfsW9OQ-5ldn)

Render’s Project Environment Settings

> *❓For anyone wondering how in the code I connected to* `*Atlas*`*, here’s that snippet*

```
from pymongo import MongoClientclient = MongoClient(    host=DB_URL)
```

## Run server

`Settings > Build & Deploy > Run Command`

```
gunicorn --bind :$PORT --workers 4 -k uvicorn.workers.UvicornWorker geo_covid.asgi:application
```

Key takeaway is that I ran it with `gunicorn` and some extra port, worker settings.

After all the settings, just run deploy with latest commit 🤲

## Demo

After getting the DB up and then the backend API online, I try making connections to it from my frontend and everything is nice/clean 👩‍🍳🥳

The server might not be online anymore but as of now, my frontend is still online and you can visit it at [https://geo-covid-frontend.web.app/](https://geo-covid-frontend.web.app/)

![](https://miro.medium.com/v2/resize:fit:788/0*K-Kht5JA8_peEjHL)

Demo

Backend source code can be found [here](https://github.com/produdez/geo-covid-backend) and front-end [here](https://github.com/produdez/us-geo-covid)

## Final words

Those are my findings while tring to get my side project online. It’s quite messy and erroneous overall but I’m quite happy that it’s online.

I’ll try to get a creditcard soon ☠️

But please, do comment your thought on my topic and clap if it helped in any ways. Would love to hear from you ⭐

Thanks for reading and have a nice day 😎