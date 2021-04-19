from decimal import Decimal
import json
import boto3
import datetime 
import time 


def load_movies(movies, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

    table = dynamodb.Table('Movies')
    week = datetime.datetime.today() + datetime.timedelta(days=7)
    expiryDateTime = int(time.mktime(week.timetuple())) 
    for movie in movies:
        year = int(movie['year'])
        title = movie['title']
        movie['ttl'] = str(expiryDateTime)
        expirystr = movie['ttl']
        print("Adding movie with expiration date :", year, title, expirystr)
        table.put_item(Item=movie)


if __name__ == '__main__':
    with open("moviedata.json") as json_file:
        movie_list = json.load(json_file, parse_float=Decimal)
    load_movies(movie_list)
