#! /usr/bin/env python3

import psycopg2

top_articles_query = """
        select title, cast(count(title) as integer) as num
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
        limit 4
        """

top_error_days_query = """
        select to_char(day, 'Mon DD, YYY'), err_pcnt
        from
            (select requests.day as day,
                round(100 * (cast (errors.hits as numeric) / requests.hits), 2) as err_pcnt
            from
                (select date(time) as day, count(*) as hits
                from log
                group by day) as requests,

                (select date(time) as day, count(*) as hits
                from log
                where status like '%404%'
                group by day) as errors
            where requests.day = errors.day
            order by err_pcnt desc) as error_data
        where err_pcnt > 1
        """

def query_db(query):
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


if __name__ == "__main__":

    print("What are the most popular three articles of all time?")
    for a in query_db(top_articles_query):
        print('\t"{}" - {} views'.format(a[0], a[1]))

    print("\nWho are the most popular article authors of all time?")
    for a in query_db(top_authors_query):
        print('\t{} - {} views'.format(a[0], a[1]))

    print("\nOn which days did more than 1% of requests lead to errors?")
    for a in query_db(top_error_days_query):
        # print("\t" + "%s - %d" % (a[0], a[1]) + " percent")
        print('\t{} - {} percent'.format(a[0], a[1]))
