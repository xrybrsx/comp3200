import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html

import plotly.express as px

import pandas as pd

from analysis import  analyse, get_sentiment_percentage, common_words
import twitter_api as twitter
from dash.dependencies import Input, Output, State
from database import store_tweets, get_tweets, get_users, store_users



# my_dboard.get_preview()
local_storage = []

app = dash.Dash(external_stylesheets=[dbc.themes.MORPH])
#app = dash.Dash()
server = app.server


# data = twitter.process_yaml()
bearer_token = 'AAAAAAAAAAAAAAAAAAAAACJWYQEAAAAAJ8L97yf%2FLbDoTTQLW77TcQLT8HQ%3D7GqMszwYUwK8lx8GFuhROYpIym8AyWQB0t6e7pEBeSbBBjTgny'


__twitter_count = 0

app.layout = html.Div(
    # style={"backgroundColor": colors["background"]},
    children=[
       
        html.Div([
            "Search: ",
            dcc.Input(id='search_keyword',
                      type='text'),
                      html.Button("Search", id='submit-button', type='submit' ),
                      html.H6(id='output-div', className='search-output')
                      
        ]),
       
       

        html.Div(
            [
                dbc.Row([

                    dbc.Col(dbc.Card(
                        [
                            html.P("No. of Tweets"),
                            html.H6(
                                id="number_of_tweets",
                                className="info_text",
                              
                            )
                        ]),  md = 2),

                    dbc.Col(dbc.Card(
                        [
                            html.P("No. of Users"),
                            html.H6(
                                id="number_of_users",
                                className="info_text",
                               
                            )
                        ],
                        
                    ),  md = 2),

                    dbc.Col(dbc.Card(
                        [
                            html.P("No. of Likes"),
                            html.H6(
                                id="number_of_likes",
                                className="info_text",
                              
                            )
                        ]),  md = 2),

                    dbc.Col(dbc.Card(
                        [
                            html.P("No. of Retweets"),
                            html.H6(
                                id="number_of_retweets",
                                className="info_text",
                               
                            )
                        ]),  md = 2),

                    dbc.Col(dbc.Card(
                        [
                            html.P("No. of Tweets"),
                            html.H6(
                                id="number_of_todo",
                                className="info_text",
                               
                            )
                        ]),  md = 2),
                 
                ]), 

            ],
            id="infoContainer",
            className="row-center"
        ),

        html.H1(
            children="Twitter Sentiment Dashboard", className="text-center"
            # style={"textAlign": "center", "color": colors["text"]},
        ),
        html.Div(
            children="This is project towards a BSc Computer Science degree aiming to do a research on the public's opinion.",
           className="text-center"
        ),
        dbc.Row([
            
             dbc.Col(dcc.Graph(id="sentiment_plot"), md=8),
             dbc.Col(dcc.Graph(id="pie-chart"),  md=4),
            ], ),
            dcc.Graph(id="count"),

             dbc.Row([
            
             dbc.Col(dcc.Graph(id="sunburst_chart"), md=4),
             dbc.Col(dcc.Graph(id="common_words_bar_chart"),  md=8),
            ], ),
            dcc.Graph(id="pie-sunburst-locations")
           # dcc.Graph(id="sentiment")
    #     dcc.Graph(id="count"),
        
    #     dcc.Graph(id="sunburst_chart"),
    #   ##  dcc.Graph(id="pie-chart-locations"),
    #     dcc.Graph(id="pie-sunburst-locations")
        #dcc.Graph(id="common_words_bar_chart")
    ],
)



# app.css.append_css({
#     "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
# })

@app.callback(
    Output('output-div','children' ), 
    [Input('submit-button', 'n_clicks')],
    [State('search_keyword', 'value')], 
    
    )
def update_output(clicks, input_value):
        if clicks is not None:
            
            # url = twitter.tweets_full_info_url(input_value,10)
            # tweets = twitter.twitter_auth_and_connect(bearer_token, url)
            # store_tweets(tweets, input_value)
            # store_users(tweets,input_value)
            return input_value

@ app.callback(
    Output(component_id="count", component_property="figure"),
    Output(component_id="number_of_tweets", component_property="children"),
    Input(component_id="output-div", component_property="children"),

)
# def update_output(keyword):
#     return u'Results for {}'.format(keyword)
def generate_count_graph(search_keyword):
 if len(search_keyword) > 1 :
    # url = twitter.search_hashtag_url(search_keyword, 10)
    # dat = twitter.twitter_auth_and_connect(bearer_token, url)
    url = twitter.count_tweets_url(search_keyword, "day")
    res_json = twitter.twitter_auth_and_connect(bearer_token, url)
    #print(res_json)
    # print(res_json['meta'])
    # print(res_json['meta']['total_tweet_count'])
    # # print(dat)
    # store(dat['data'])
    __twitter_count = int(res_json['meta']['total_tweet_count'])
   # print(__twitter_count)

    df = pd.DataFrame(res_json['data'])
    df['start'] = pd.to_datetime(df['start'])
    final = df[['start', 'tweet_count']]
   # print(final)
    fig = px.line(final, x="start", y="tweet_count")

    # fig.update_layout(
    #     plot_bgcolor=colors["background"],
    #     paper_bgcolor=colors["background"],
    #     font_color=colors["text"],
    # )
    return fig, __twitter_count



@ app.callback(
    
    Output(component_id="sentiment", component_property="figure"),
    Input(component_id="output-div", component_property="children"),
    


)
def generate_sentiment_graph(keyword):
 if len(keyword) > 1 :
    # tweets = twitter.search_hashtag_url(keyword, 10)
    # store(tweets)
    #
    data = get_tweets(10, keyword)
   
   
    sentiment_score = analyse(data)
    
    # df = pd.DataFrame(sentiment_score)
    df = pd.json_normalize(sentiment_score)
    print(df)
    local_storage = df
    df["sentiment"] = df["sentiment.positive"] - df["sentiment.negative"]
    # final = df[['text', 'sentiment']]
    print(df)
    fig = px.bar(df, x=df.index, y='sentiment', hover_data=[
        'text'], labels={'index': '#'}, color="sentiment", color_continuous_scale=px.colors.sequential.RdBu)
   # fig = px.scatter(df, x="sentiment.positive",
    # y="sentiment.negative")

    # fig.update_layout(

    #     plot_bgcolor=colors["background"],
    #     paper_bgcolor=colors["background"],
    #     font_color=colors["text"],
    # )
    return fig


@ app.callback(
    
    Output(component_id="sentiment_plot", component_property="figure"),
    Input(component_id="output-div", component_property="children"),
)

def generate_sentiment_plot(keyword):
 if len(keyword) > 1 :
    # tweets = twitter.search_hashtag_url(keyword, 10)
    # store(tweets)
    #
    data = get_tweets(10, keyword)
   
   
    sentiment_score = analyse(data)
    
    # df = pd.DataFrame(sentiment_score)
    df = pd.json_normalize(sentiment_score)
    print(df)
    local_storage = df
    #df["sentiment"] = df["sentiment.positive"] - df["sentiment.negative"]
    # final = df[['text', 'sentiment']]
    print(df)
    fig = px.scatter(df, x=df["sentiment.positive"], y=df["sentiment.negative"], hover_data=[
        'text'], labels={'sentiment.positive': 'positive weight', 'sentiment.negative': 'negative weight', "sentiment.compound": "compound"}, color=df["sentiment.compound"], color_continuous_scale=px.colors.sequential.RdBu)
   # fig = px.scatter(df, x="sentiment.positive",
    # y="sentiment.negative")

    # fig.update_layout(

    #     plot_bgcolor=colors["background"],
    #     paper_bgcolor=colors["background"],
    #     font_color=colors["text"],
    # )
    return fig
@ app.callback(
    Output(component_id="pie-chart", component_property="figure"),
    Input(component_id="output-div", component_property="children"),
   

)
def generate_pie(keyword):
 if len(keyword) > 1:
    data = get_tweets(10, keyword)
    json_sentiment  = get_sentiment_percentage(data)
    data = json_sentiment
    df = pd.json_normalize(json_sentiment)

    print(df)

    #print(df.values)
    names = ['negative', 'neutral', "positive"]
    fig = px.pie(df, values=df.values[0], names=df.columns,
                 title='Percentage of Sentiment', color_discrete_sequence=px.colors.sequential.Blues)

    return fig


@ app.callback(
    Output(component_id="sunburst_chart", component_property="figure"),
    Input(component_id="output-div", component_property="children"),

)
def generate_sunburst(keyword):
  if len(keyword) > 1:
    context = {}
    context["domain"] = []
    context["entity"] = []
    df = pd.json_normalize(get_tweets(10, keyword))
    for i in df['context']:
        if isinstance(i, list):
            # print(i)
            for j in i:
                # print(j['domain'])
                context["domain"].append(j['domain']['name'])
                # print(j['entity'])
                context["entity"].append(j['entity']['name'])

    data = pd.DataFrame(context)
    # data["domain_name"] = []
    # data["entity_name"] = []
    # for i in data.domain:
    #     data["domain_name"].append(i)
    # for i in data.entity:
    #     data["entity_name"].append(i)
    print(data)
   # print(data.size)
    # fig = go.Figure()
    # fig.add_trace(go.Sunburst(
    #     ids=data.index,
    #     labels=data.entity,
    #     parents=data.domain,
    #     domain=dict(column=0),
    #     maxdepth=2,
    #     insidetextorientation='radial'
    # ))
    # fig.show()
    fig = px.sunburst(
        data, path=['domain', 'entity'], values=[1]*len(data), labels={"value": "number"})
    fig.update_traces(insidetextorientation='radial')
    #fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    #   plot_bgcolor=colors["background"],
    #   paper_bgcolor=colors["background"],
    #   font_color=colors["text"])

    return fig
@ app.callback(
    Output(component_id="pie-chart-locations", component_property="figure"),
    Output(component_id="number_of_users", component_property="children"),
    Input(component_id="output-div", component_property="children"),

)
def generate_pie(keyword):
 if len(keyword) > 1 :
    
    df = pd.json_normalize(get_users(10, keyword))
    print(df)
    
    
    j = 0 
    for i in df['location']:
        
        if isinstance(i,str) == False:
           
            df.at[j, "location"] = "Unknown"
        j = j+1
    # locations = df['location']
    # df["location"].fillna(0)
    
    fig = px.pie(df, values=[1]*len( df["location"]), names= df["location"],
                 title='Location of Users', color_discrete_sequence=px.colors.sequential.Blues)

    return fig, len(df["user"])
@ app.callback(
    Output(component_id="pie-sunburst-locations", component_property="figure"),
    Input(component_id="output-div", component_property="children"),

)
def generate_sunburst_locations(keyword):
 if len(keyword) >1 :
    df = pd.json_normalize(get_users(10, keyword))
    
    j = 0 
    for i in df['location']:
        
        if isinstance(i,str) == False:
           
             df.at[j, "location"] = "Unknown"
        j = j+1
    # locations = df['location']
    # df["location"].fillna(0)
    
    
    print(df)
    
    fig = px.sunburst(df, path=['location', 'username'], values=[1]*len(df["location"]),labels={"null": "Unknown", "value": "# of users"},
                 title='Location of Users', color_discrete_sequence=px.colors.sequential.Blues)
    fig.update_traces(insidetextorientation='radial')
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig

@ app.callback(
    Output(component_id="common_words_bar_chart", component_property="figure"),
    Input(component_id="output-div", component_property="children"),

)
def common_words_bar_chart(keyword):
 if len(keyword) >1 :
    data = get_tweets(10, keyword)
    print(data)
    tuples = common_words(data, 10)
    df = pd.DataFrame(tuples)
    df.rename(columns = {0 : 'Words', 1 : 'Occurances'}, inplace = True)
    print(df)
  
    
    fig = px.bar(df, x=df["Occurances"], y=df['Words'])

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
    # generate_pie("python")
