import marimo

__generated_with = "0.9.20"
app = marimo.App(
    width="medium",
    app_title="Yelp Analysis",
    auto_download=["html"],
)


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""# Mini Project 1 -Extra""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Author: *Y. Huang*

        GitHub: *https://github.com/celesteisyy*

        # Intro

        ---

        This notebook demonstrates the **conversion of existing SQL code into Python code** for execution and analysis. The original SQL logic remains intact and has been adapted into Python, ensuring consistency in data processing and results.

        After implementing the Python code, additional business analysis statements were included to provide simple insights based on the outcomes of the original SQL queries. These insights are directly derived from the data without altering the initial logic.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""# Loading Data from Kaggle""")
    return


@app.cell(hide_code=True)
def __():
    #import kaggle
    #import zipfile
    import json
    from pandas import json_normalize
    import pandas as pd
    import numpy as np
    import os
    import marimo as mo
    import altair as alt
    import narwhals as pl
    import io
    alt.renderers.set_embed_options(actions=True)
    return alt, io, json, json_normalize, mo, np, os, pd, pl


@app.cell(hide_code=True)
def __():
    #!kaggle datasets files yelp-dataset/yelp-dataset
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""To use the data, you may need to download and unzip data from Kaggle: (yelp dataset is relatively large so it might take some time to process for the first time)""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""Here I keep 10,000 rows for faster processing""")
    return


@app.cell(hide_code=True)
def __(pd):
    files = ["business.csv", "checkin.csv", "review.csv", "tip.csv"]
    base_url = "https://raw.githubusercontent.com/celesteisyy/SQL-Server/refs/heads/main/"

    dataframes = {}

    for file in files:
        url = base_url + file
        try:
            df = pd.read_csv(url, nrows=10000)
            dataframes[file.split(".")[0]] = df 
            print(f"{file} set！")
        except Exception as e:
            print(f"{file} loaded failed：{e}")
    return base_url, dataframes, df, file, files, url


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## Dataset Infos""")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        As convension, let's check the statistical overview of the data:

        --------
        """
    )
    return


@app.cell(hide_code=True)
def __(pd):
    pd.set_option('display.max_colwidth', None) # especially for the "text" in Review table and "attributes" in Business table
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""### Checkin""")
    return


@app.cell(hide_code=True)
def __(dataframes):
    checkin = dataframes["checkin"]
    checkin.info()
    return (checkin,)


@app.cell(hide_code=True)
def __(checkin):
    checkin.head()
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""### Review""")
    return


@app.cell(hide_code=True)
def __(dataframes, json_normalize, pd):
    review = dataframes["review"]
    review_flat = json_normalize(review['text'])
    review_1 = pd.concat([review, review_flat], axis=1)
    return review, review_1, review_flat


@app.cell(hide_code=True)
def __(review_1):
    review_1.info()
    return


@app.cell(hide_code=True)
def __(review_1):
    review_1['stars'] = review_1['stars'].astype(float)
    review_2 = review_1.rename(columns={'stars': 'stars_r'})
    return (review_2,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""### Business""")
    return


@app.cell(hide_code=True)
def __(dataframes):
    business_1 = dataframes["business"]
    return (business_1,)


@app.cell(hide_code=True)
def __(business_1):
    business_1.info()
    return


@app.cell(hide_code=True)
def __(business_1):
    business_1.head()
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""### Tip""")
    return


@app.cell(hide_code=True)
def __(dataframes):
    tip = dataframes["tip"]
    tip.info()
    return (tip,)


@app.cell(hide_code=True)
def __(tip):
    tip.head()
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""# Get into Business Insights ✨""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""This part is a replicate process from our team's queries, but we'll analyse this using Python this time""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""First, let's have an overview of First 100 rated businesses and their ratings:""")
    return


@app.cell(hide_code=True)
def __(df1, mo):
    business_select = mo.ui.dropdown.from_series(
        df1['name'][:100],
        label="Business",
        value=None,
    )
    business_select
    return (business_select,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""Choose an icon you prefer!""")
    return


@app.cell(hide_code=True)
def __(mo):
    icon = mo.ui.dropdown(["🍃", "🌊", "✨"], value="✨")
    icon
    return (icon,)


@app.cell(hide_code=True)
def __(business_select, df1):
    if business_select.value in df1['name'].values:
        repetitions = df1.loc[df1['name'] == business_select.value, 'stars'].values[0]
    else:
        repetitions = 0
    repetitions = int(repetitions)
    return (repetitions,)


@app.cell(hide_code=True)
def __(icon, mo, repetitions):
    mo.md("#" + icon.value * repetitions)
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## First Query to Python""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Origianl SQl Query:
        This is the query that help us find most high-rating businesses as well as their locations
        ```
        %%sql
        SELECT TOP 100
            AVG(review.stars) AS avg_rating,
            business.name,
            business.city,
            COUNT(review.business_id) AS review_count
        FROM review
        JOIN business ON review.business_id = business.business_id
        GROUP BY business.name, business.city
        ORDER BY avg_rating DESC, review_count DESC;
        ```
        """
    )
    return


@app.cell(hide_code=True)
def __(business_1, pd, review_2):
    df1 = pd.merge(review_2, business_1, on='business_id')
    df1_m = df1.groupby(['name', 'city'])
    df1_m.head()
    return df1, df1_m


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""Notice that there are some discrepancies between `stars` in Review table and Business table. For consistency with SQL, 'stars_r', which is the ratings from Review table, is used for calculation. (It might be more reasonable to use the average of both ratings as the indicator)""")
    return


@app.cell(hide_code=True)
def __(df1_m):
    avg_ratings = df1_m['stars_r'].mean()
    review_count = df1_m['review_count'].sum()
    print(review_count)
    return avg_ratings, review_count


@app.cell(hide_code=True)
def __(avg_ratings, pd, review_count):
    result = pd.DataFrame({
        'avg_ratings': avg_ratings,
        'review_count': review_count
    })
    result = result.sort_values(['avg_ratings', 'review_count'], ascending=[False, False])
    return (result,)


@app.cell(hide_code=True)
def __(mo, result):
    mo.ui.table(result.head(100), pagination = True)
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""Explanations: As shown in the table, though Beauty Spas and Cafe shops show promising performance in our initial review, we'll need to conduct a detailed analysis to determine which business categories receive the highest engagement on Yelp.""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## Second Query to Python""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Origianl SQl Query: This query helps us determine the most Popular Business Categories on Yelp

        ```
        %%sql
        SELECT TOP 10 categories, COUNT(*) AS category_count
        FROM business
        GROUP BY categories
        ORDER BY category_count DESC;
        ```
        """
    )
    return


@app.cell(hide_code=True)
def __(business_1, mo):
    cat = business_1.groupby('categories').size()
    cat = cat.sort_values(ascending=False)
    cat = cat.reset_index(name='count')
    mo.ui.table(cat.head(10))
    return (cat,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Explanations:

        The above reveals that Pizza restaurants and Beauty salons are among the most prevalent business types on the platform.

        Although the high frequency of these establishments may indicate strong customer demand and potential profitability in these sectors, excessive competition could limit the market share and customer traffic we can secure. Therefore, selecting a category with relatively high demand but requiring lower operational costs might be a more suitable choice.

        While this data provides valuable market insights, further analysis of factors such as competition and market saturation. This follows the third query:
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## Third Query to Python""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Origianl SQL Query: We want to be niche. There are too many pizzarias. Additionally, based on the former analysis, Cafe shops may also have a promising customer group. Therefore, this third query will help us determine which cities have the most cafes.

        ```
        %%sql
        SELECT TOP 5 city, COUNT(*) AS business_count
        FROM business
        WHERE name LIKE '%coffee%'
        GROUP BY city
        ORDER BY business_count DESC;
        ```
        """
    )
    return


@app.cell(hide_code=True)
def __(business_1, mo):
    cities = business_1[business_1['categories'].fillna('').str.contains('coffee', case=False)]
    cities = cities.groupby('city').size()
    cities = cities.sort_values(ascending=False)
    cities = cities.reset_index(name='count')
    mo.ui.table(cities)
    return (cities,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Explanations:

        The table shows the number of coffee shops in different cities. It can be seen that Philadelphia has the highest number of coffee shops, with 57, followed by cities like Edmonton, Nashville, and Tampa, approximately 25. The remaining cities have around one coffee shop, which could be due to insufficient data collection or the smaller size of these cities, resulting in lower demand.

        As mentioned earlier, having too many or too few competitors in the same category may negatively impact the establishment of our business. Therefore, we can choose a city in the second tier of coffee shop numbers as the settlement location. Here, we select New Orleans, a city with a moderate number of coffee shops.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## Forth Query to Python:""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Origianl SQL Query: This code will help us research the cafe place in New Orleans that has a combination of the highest average user score while at the same time the highest number of user scores.

        ```
        %%sql
        SELECT TOP 5
            business.name,
            AVG(review.stars) AS avg_rating,
            COUNT(review.business_id) AS review_count
        FROM review
        JOIN business ON review.business_id = business.business_id
        WHERE business.city = 'New Orleans' AND business.name LIKE '%coffee%' OR business.name LIKE '%cafe'
        GROUP BY business.name
        ORDER BY avg_rating DESC, review_count DESC;
        ```
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""Here I made minor adjustment by searching key words `coffee` and `cafe` in `categories` instead of `name` for broader research:""")
    return


@app.cell(hide_code=True)
def __(df1):
    df1_f = df1[(df1['city'] == 'New Orleans') &
            (df1['categories'].str.contains('coffee', case=False) | df1['categories'].str.contains('cafe', case=False))]
    return (df1_f,)


@app.cell(hide_code=True)
def __(df1_f, mo):
    df1_coffee = df1_f[['categories','name','stars_r','review_count']]
    mo.ui.table(df1_coffee.head())
    return (df1_coffee,)


@app.cell(hide_code=True)
def __(df1_coffee):
    df1_coffee_1 = df1_coffee.groupby('name')
    avg_ratings4 = df1_coffee_1['stars_r'].mean()
    review_count4 = df1_coffee_1['review_count'].sum()
    return avg_ratings4, df1_coffee_1, review_count4


@app.cell(hide_code=True)
def __(avg_ratings4, pd, review_count4):
    result4 = pd.DataFrame({
        'ratings': avg_ratings4,
        'review_count': review_count4
    })
    result4 = result4.sort_values(['ratings', 'review_count'], ascending=[False, False])
    return (result4,)


@app.cell(hide_code=True)
def __(mo, result4):
    mo.ui.table(result4.head())
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Explanation:

        The above table displays the top 5 rating scores as well as review counts of the businesses in New Orleans.

        It can be seen that De Ville Coffee House & Creperie, SWEGS Kitchen - Mid-City and Chateau Cafestand out with a perfect average rating of five stars and an impressive number of reviews. Possible factors contributing to their success, such as menu offerings, customer service quality, and marketing strategies, can be dug into in the following steps.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"""## Fifth Query to Python:""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Origianl SQL Query: This fifth query will help us see which cafes have the most reviews in New Orleans.

        ```
        %%sql
        SELECT TOP 10 name, stars, attributes, review_count
        FROM business
        WHERE categories LIKE '%coffee%'
            AND name LIKE '%coffee%' OR name LIKE '%cafe%'
            AND city = 'New Orleans'
        ORDER BY review_count DESC;
        ```
        """
    )
    return


@app.cell(hide_code=True)
def __(df1_coffee_1, mo):
    fifth = df1_coffee_1['review_count'].sum().reset_index()
    fifth = fifth.sort_values(by='review_count', ascending=False)
    mo.ui.table(fifth.head())
    return (fifth,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Explanations:
        The table ranks the top five coffee-related businesses by review count, demonstrating their popularity and customer engagement.

        High-performing businesses likely benefit from effective marketing and strong customer satisfaction, while lower-ranked ones may improve with targeted promotions and enhanced service.

        Among the coffe shops in New Orleans, District Donuts Sliders Brew leads with 88,666 reviews, followed by **Surrey's Café & Juice Bar** (79,192) and **Mr. B's Bistro** (74,304).
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## Sixth Query to Python:""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Origianl SQL Query: Now we're curious which cafes have the most reviews overall

        ```
        %%sql
        SELECT TOP 10 name, stars, attributes, review_count
        FROM business
        WHERE categories LIKE '%coffee%'
            AND name LIKE '%coffee%' OR name LIKE '%cafe%'
        ORDER BY review_count DESC;
        ```
        """
    )
    return


@app.cell(hide_code=True)
def __(df1):
    coffee_shops = df1[
        ((df1['categories'].str.contains('coffee', case=False, na=False)) | df1['categories'].str.contains('cafe', case=False, na=False)) &
        ((df1['name'].str.contains('coffee', case=False, na=False)) |(df1['name'].str.contains('cafe', case=False, na=False)))
    ]
    return (coffee_shops,)


@app.cell(hide_code=True)
def __(coffee_shops, mo):
    result6 = coffee_shops[['name', 'stars', 'review_count']]

    result6 = result6.sort_values('review_count', ascending=False).drop_duplicates()
    mo.ui.table(result6.head(10))
    return (result6,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Explanations:

        The table highlights the top coffee shops based on review count, reflecting customer engagement and popularity. High review counts indicate strong customer traction, while lower review counts with high ratings suggest potential growth opportunities.


        **Cafe Fleur De Lis** leads with 1,865 reviews and a 4-star rating, followed by **Cafe Beignet on Bourbon Street** with 1,066 reviews and a 3.5-star rating.

        Additionally, **Lilly's Cafe** balance popularity and customer satisfaction, with an average ratings of 4.5 stars and 777 reviews, making them strong competitors in the market.

        By having this table, we can have insights support our expansion strategies after having considerable operational income.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## Seventh Query to Python:""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Origianl SQL Query: This will help us see which cafes are performing the best in New Orleans and help us guide our market research.

        ```
        %%sql
        SELECT TOP 10 name, stars, attributes, review_count, city
        FROM business
        WHERE stars > 3.5
            AND categories LIKE '%coffee%'
            AND name LIKE '%coffee%' OR name LIKE '%cafe%'
            AND city = 'New Orleans'
        ORDER BY stars DESC, review_count DESC;
        ```
        """
    )
    return


@app.cell(hide_code=True)
def __(df1):
    coffee_NOr = df1[
        (df1['stars_r'] > 3.5) &
        (df1['categories'].str.contains('coffee', case=False, na=False)|
         ((df1['name'].str.contains('coffee', case=False, na=False)) | (df1['name'].str.contains('cafe', case=False, na=False)))) &
        (df1['city'] == 'New Orleans')
    ]
    return (coffee_NOr,)


@app.cell(hide_code=True)
def __(coffee_NOr, mo):
    result7 = coffee_NOr[['name', 'stars_r', 'review_count']]
    result7 = result7.sort_values(['stars_r', 'review_count'], ascending=[False, False]).reset_index(drop=True).drop_duplicates('name')
    mo.ui.table(result7)
    return (result7,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Explanation:

        The above table identifies top-rated coffee shops in New Orleans based on customer ratings greater than 3.5 and review counts.

        Many coffee shops achieve a perfect 5.0-star rating, presenting the high standard of coffee establishments in New Orleans. For example, **District Donuts Sliders Brew** stands out with the highest number of reviews (2062). Also, **Cafe Fleur De Lis** follows with 1865 reviews,suggesting strong brand visibilities and customer engagements among these stores.

        Other shops include **Cafe Pontalba** (4.0 stars, 560 reviews), which also reflects significant popularity despite slightly lower ratings
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## Eighth Query to Python:""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Origianl SQL Query: This code will show us reviews that are positive about some cafes in New Orleans, providing us insight into what people may like or want.

        ```
        %%sql
        SELECT TOP 25 business.name, business.stars, review.text
        FROM review
        JOIN business ON review.business_id = business.business_id
        WHERE business.city = 'New Orleans'
          AND business.categories LIKE '%coffee%' OR categories LIKE '%cafe%'
          AND business.stars >= 4
        ORDER BY business.stars DESC;
        ```
        """
    )
    return


@app.cell(hide_code=True)
def __(df1):
    coffee8 = df1[
        (df1['stars'] >= 4) & # rather than 'stars_r', this is the rating from business table
        (df1['categories'].str.contains('coffee', case=False, na=False)|
         ((df1['name'].str.contains('coffee', case=False, na=False)) | (df1['name'].str.contains('cafe', case=False, na=False)))) &
        (df1['city'] == 'New Orleans')
    ]
    return (coffee8,)


@app.cell(hide_code=True)
def __(coffee8, mo):
    result8 = (
        coffee8[["name", "stars", "text"]]
        .sort_values("stars", ascending=False)
        .reset_index(drop=True)
    )
    mo.ui.table(result8.head(25))
    return (result8,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Explanation:

        The above table analyzes high-rated coffee shops in New Orleans, focusing on customer feedback to understand key drivers of satisfaction.

        As can be seen, **District Donuts Sliders Brew** consistently receives high praise for its innovative menu and engaging atmosphere, which may suggest that customers appreciate the variety and creativity in offerings.

        Additionally, **Treme Coffeehouse** is noted for its cozy environment, colorful decor, and welcoming baristas. This may suggest that the amendities in the store may also be an important indicators for customers.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## Ninth Query to Python:""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Origianl SQL Query: This code will help us determine which months our business will do best, therefore potentially prompting us to open during a certain month or predict sales per month.

        ```
        %%sql
        SELECT MONTH(date) AS month, COUNT(review_id) AS review_count
        FROM review
        JOIN business ON review.business_id = business.business_id
        WHERE business.city = 'New Orleans'
          AND business.categories LIKE '%cafe%' OR business.categories LIKE '%coffee%'
        GROUP BY MONTH(date)
        ORDER BY month;
        ```
        """
    )
    return


@app.cell(hide_code=True)
def __(df1_f):
    coffee9 = df1_f[['name','date','review_id',"city",'stars_r']]
    coffee9.head()
    return (coffee9,)


@app.cell(hide_code=True)
def __(df1_f):
    months = df1_f[['name','date','review_id','stars_r']]
    months.head()
    return (months,)


@app.cell(hide_code=True)
def __(months, pd):
    months['date'] = pd.to_datetime(months['date'], format='%Y-%m-%d %H:%M:%S')
    months['month'] = months['date'].dt.month
    months.head()
    return


@app.cell(hide_code=True)
def __(months):
    df9 = months.groupby('month')
    return (df9,)


@app.cell(hide_code=True)
def __(df9):
    result9 = df9['review_id'].count().reset_index()
    result9 = result9.rename(columns={'review_id': 'review_count'})

    # Sort by month
    result9 = result9.sort_values('review_count', ascending= False)
    return (result9,)


@app.cell(hide_code=True)
def __(result9):
    result9
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Explanation:
        The above table displays identifies the month with the highest number of reviews.

        As can be seen, months with **high** review counts (e.g., January, May, and August) could indicate periods of **increased** customer activity or demand. These may correspond to local events, tourist seasons, or marketing campaigns.

        Meanwhile, months with **lower** review counts (e.g., October and June) might indicate a **slower** business period. Businesses could explore strategies to boost engagement during these months, such as promotions or new product launches.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## Tenth Query to Python:""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Original SQL Query: This identifies the top 5 most influential userswho have reviewed cafes or coffee-related businesses in New Orleans, helping to target potential brand ambassadors or key customer segments.

        ```
        %%sql
        SELECT TOP 5 [user].fans, review.business_id, [user].name
        FROM [user]
        JOIN review ON review.user_id = [user].user_id
        JOIN business ON review.business_id = business.business_id
        WHERE business.city = 'New Orleans'
          AND (business.categories LIKE '%cafe%' OR business.categories LIKE '%coffee%')
        ORDER BY [user].fans DESC;
        ```
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        """
        Because 'user' table was too big to load, it is skipped in this marimo notebook 

        But you can check it in the mini1+.ipynb in my GitHub!
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        Explanation:

        The above table studies the reviews and ratings given by users with the highest fan counts to understand their impact on businesses.

        By identifying active reviewers, we can have insights that help us in understanding loyal customers and improving services.

        Additionallu, the most popular reviewers could represent influencers or active community members, and thus be our potential brand ambassadors or key customer segments.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        ## Conlusion
        ---
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""The analysis reveals that success stems from more than just coffee – distinctive menu offerings and attentive service emerge as crucial differentiators in this competitive market. Strategic opportunities exist for businesses to capitalize on peak seasonal trends, particularly during high-traffic months (Jan, May and Aug) when thoughtful operational planning can maintain service excellence along with increased demand. Throughout the analysis, it also suggests that proactive engagement with influential reviewers and systematic incorporation of customer feedback creates a virtuous cycle, driving both business growth and sustained customer loyalty in this vibrant market.""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        ---
        **End of this Notebook**
        """
    )
    return


if __name__ == "__main__":
    app.run()
