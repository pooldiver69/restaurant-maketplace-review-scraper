# restaurant-maketplace-review-scraper
## how to run
### create virtural python env
```
python -m venv venv
```
### activate virtural python env
```
Windows:
.\venv\Scripts\activate.bat

Mac:
soruce venv/bin/activate
```
### install packages from requirement.txt
```
pip install -r requirements.txt
```
### running server
```
uvicorn app.main:app --reload
```
should see server running, and printing on console!
```
INFO:     Will watch for changes in these directories: ['E:\\projects\\acelerate-assignment']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [1200] using WatchFiles
INFO:     Started server process [3728]
INFO:     Waiting for application startup.
refresh!
INFO:     Application startup complete.
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [3728]
INFO:     Stopping reloader process [1200]
```

## APIs
 
APIs docs also hosted on server: http://localhost:8000/docs#/

### list all restaurants in the database
```
GET /restaurants
```
sample output
```
[
    {
        "name": "Napoli Pizza",
        "gh_url": "https://www.grubhub.com/restaurant/napoli-pizza-1045-polk-st-san-francisco/2058686",
        "dd_url": null,
        "ue_url": null,
        "id": 1
    }
]
```

### scrape target restaurant
```
/scrape/restaurant/{id}
```
refersh reviews in upsert methods, so no duplicated data will be inserted
sample output
```
ok

or 

"restaurant not exists", 404
```

### get all reviews of target restaurant
```
/restaurant/{id}/reviews
```
sample output
```
[
    {
        "reviewer": "Joshua",
        "date": "Apr 23, 2023",
        "review": "TLDR: Don't order from here expecting anything special. Although my pickup order was on-time and correct, the high GrubHub rating and positive reviews led me to anticipate much better food than I received. The pizza was just OK. Adequate cheese & topping quality/quantity. I have no idea why other reviews rave about the crust - it is nothing special. To be clear, the pizza wasn't gross. The garlic cheese bread was kinda gross, though: a toasted sesame seed hoagie bun with some kind of oil and a bit of mozz.",
        "rating": 2,
        "source": "grubhub",
        "restaurant_id": 1,
        "new": true,
        "id": 1
    },
    {
        "reviewer": "Dominic",
        "date": "Oct 21, 2022",
        "review": "Lasagna was really bad - trust me don’t order it. San Francisco pizza had barely any feta cheese on it and the crust was a bit doughy.",
        "rating": 2,
        "source": "grubhub",
        "restaurant_id": 1,
        "new": true,
        "id": 2
    },
    ...
]
```

### get insights data of restaurant
```
/restaurant/{id}/insights
```
sample output
```
{
    "most_popular_item": "2 Toppings Pizza",
    "most_loved_item": "2 Toppings Pizza",
    "least_loved_item": "Baked Lasagna"
}
```

## Schedule Task
This server also run a scheduled task every 24 hours, auto scraping every restaurant stored in the database.