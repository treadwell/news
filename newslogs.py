#! /usr/bin/env python3

import psycopg2

top_articles_query = """
        select title, count(title) as num
        from articles join log
        on articles.slug = substring(log.path, 10)
        group by title
        order by num desc
        limit 3
        """

top_authors_query = """
        select authors.name, count(authors.name) as num
        from authors, articles, log
        where articles.slug = substring(log.path, 10) and
            articles.author = authors.id
        group by authors.name
        order by num desc
        limit 3
        """

top_error_days_query = """
        (select date(time) as day, count(*) as hits
        from log
        group by day) as requests
        """

def query_db(query):
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


if __name__ == "__main__":
    # print(query_db(top_articles_query))
    # print(query_db(top_authors_query))
    print(query_db(top_error_days_query))
