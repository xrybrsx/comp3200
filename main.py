from unicodedata import name
from xml.etree.ElementInclude import LimitedRecursiveIncludeError
from flask import Flask
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from matplotlib.colors import LightSource
import plotly.express as px
import os
import pandas as pd
import requests
from analysis import sentiment_analysis, authenticate_client, analyze, get_sentiment_percentage
import twitter_api as twitter
from dash.dependencies import Input, Output
from database import store_tweets, get_tweets


# my_dboard.get_preview()
local_storage = []

app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])
server = app.server


data = twitter.process_yaml()
bearer_token = twitter.create_bearer_token(data)

colors = {"background": "#FFFFFF", "text": "#1DA1F2"}


app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.Div([
            "Search: ",
            dcc.Input(id='search_keyword', value='python', type='text')
        ]),
        html.H1(
            children="Tweets",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        html.Div(
            children="text",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        dcc.Graph(id="count"),
        dcc.Graph(id="sentiment"),
        dcc.Graph(id="pie-chart"),
    ],
)


@app.callback(
    Output(component_id="count", component_property="figure"),
    Input(component_id="search_keyword", component_property="value"),

)
# def update_output(keyword):
#     return u'Results for {}'.format(keyword)
def generate_count_graph(search_keyword):
    # url = twitter.search_hashtag_url(search_keyword, 10)
    # dat = twitter.twitter_auth_and_connect(bearer_token, url)
    url = twitter.count_tweets_url(search_keyword, "day")
    res_json = twitter.twitter_auth_and_connect(bearer_token, url)
    print(res_json)
    # print(dat)
    # store(dat['data'])
    df = pd.DataFrame(res_json['data'])
    df['start'] = pd.to_datetime(df['start'])
    final = df[['start', 'tweet_count']]
    print(final)
    fig = px.line(final, x="start", y="tweet_count")

    fig.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
    )
    return fig


@app.callback(
    Output(component_id="sentiment", component_property="figure"),
    Input(component_id="search_keyword", component_property="value"),

)
def generate_sentiment_graph(keyword):
    # tweets = twitter.search_hashtag_url(keyword, 10)
    # store(tweets)
    #
    sentiment_score = analyze(10)
    #df = pd.DataFrame(sentiment_score)
    df = pd.json_normalize(sentiment_score)
    local_storage = df
    df["sentiment"] = df["sentiment.positive"] - df["sentiment.negative"]
    #final = df[['text', 'sentiment']]
    print(df)
    fig = px.bar(df, x=df.index, y='sentiment', hover_data=[
                 'text'], labels={'index': 'tweet'},)
   # fig = px.scatter(df, x="sentiment.positive",
    # y="sentiment.negative")

    fig.update_layout(

        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
    )
    return fig


@app.callback(
    Output(component_id="pie-chart", component_property="figure"),
    Input(component_id="search_keyword", component_property="value"),

)
def generate_pie(keyword):
    df = pd.json_normalize(get_sentiment_percentage(10))
    print(df)
    print(df.values)
    names = ['negative', 'neutral', "positive"]
    fig = px.pie(df, values=df.values[0], names=df.columns,
                 title='Percentage of Sentiment', color_discrete_sequence=px.colors.sequential.Blues)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
    # generate_pie("python")
