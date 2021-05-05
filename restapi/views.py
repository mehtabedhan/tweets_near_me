from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import twint
import json
import pandas as pd
import numpy as np
import os
import re
import matplotlib.pyplot as plt


def getTweets(prms):

    config = twint.Config()
    config.Limit = int(prms["noOfTweets"])

    config.Hide_output = True
    config.Pandas = True

    config.Geo = prms["coords"]+","+prms["radius"]

    config.Search = prms["searchBy"]
    twint.run.Search(config)

    tweets_df = twint.storage.panda.Tweets_df

    data = tweets_df
    # print(data)
    return data


@ api_view(['GET'])
def api_list(request):

    if request.method == 'GET':
        print(request.query_params)
        response = getTweets(request.query_params)
        s = json.dumps(json.loads(
            response.to_json(orient='records')), indent=2)
        print(response)
        responseData = {}
        responseData["status"] = "200"
        responseData["tweets"] = str(s)
        return Response(responseData, status=status.HTTP_200_OK)
