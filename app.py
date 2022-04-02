import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import nltk




import plotly.express as px

import pandas as pd

from analysis import  analyse, get_sentiment_percentage, common_words
import twitter_api as twitter
from dash.dependencies import Input, Output, State
from database import store_tweets, get_tweets, get_users, store_users



# my_dboard.get_preview()
__local_storage = []

dash_app = dash.Dash(external_stylesheets=[dbc.themes.MORPH])
#dash_app
# = dash.Dash()
app = dash_app.server


# data = twitter.process_yaml()
bearer_token = 'AAAAAAAAAAAAAAAAAAAAACJWYQEAAAAAJ8L97yf%2FLbDoTTQLW77TcQLT8HQ%3D7GqMszwYUwK8lx8GFuhROYpIym8AyWQB0t6e7pEBeSbBBjTgny'


__twitter_count = 0

dash_app.layout = html.Div(
    # style={"backgroundColor": colors["background"]},
    children=[
     dcc.Store(id='memory-output'),

    dbc.Navbar(
    dbc.Container(
        [
           
           
            dbc.Collapse(
                dbc.Row(
    [
        dbc.Col(dcc.Input(id='search_keyword', type="search", placeholder="Search a word")),
        dbc.Col(children=[
            dbc.Button(
                "Search",id='submit-button', color="primary", className="ms-1", n_clicks=0
            ),
             html.H6(id='output-div', className='search-output', style={"visibility": "hidden", "font-size": "1px"})],
           
        ),
    ],
    
    align="center",
),              is_open=False,
                navbar=True,
    
)]), color="light",
    dark=True, 
    className="justify-content-center"),
       
        dbc.Container(
            [ 
               
                dbc.Row([
                    dbc.Col(html.P("Overall last 7 days:", style={'margin-left':'110px'})),
                    dbc.Col( html.P("Most recent 100 tweets:", style={'margin-left':'0px'}))
                  
]),
                dbc.Row([
                   
                    dbc.Col(dbc.Card(
                        [
                            html.P("No. of Tweets"),
                            html.H6(
                                id="number_of_tweets",
                                 className="card-text",
                              
                            )
                        ]), md = 2, style={'margin-right':'50px'}),

                   
                       
                    dbc.Col(dbc.Card(
                        [
                            html.P("No. of Users"),
                            html.H6(
                                id="number_of_users",
                                 className="card-text",
                               
                            )
                        ],
                        
                    ),  md = 2),

                    dbc.Col(dbc.Card(
                        [
                            html.P("No. of Likes"),
                            html.H6(
                                id="number_of_likes",
                                 className="card-text",
                              
                            )
                        ]),  md = 2 ),

                    dbc.Col(dbc.Card(
                        [
                            html.P("No. of Retweets"),
                            html.H6(
                                id="number_of_retweets",
                                 className="card-text",
                               
                            )
                        ]),  md = 2),

                    dbc.Col(dbc.Card(
                        [
                            html.P("No. of Replies"),
                            html.H6(
                                id="number_of_replies",
                                 className="card-text",
                               
                            )
                        ]), md = 2)
                  
                 
                ], className="text-center pad-row",
                 align="center",
                 justify ="center"), 

            ],
            id="infoContainer",
            style={"padding": "1em"},
            className = "container-fluid ",
            
        ),

       
        # html.Div(
        #     children="This is project towards a BSc Computer Science degree aiming to do a research on the public's opinion.",
        #    className="text-center"
        # ),
        
       
        dbc.Row([
           
            
            
             dbc.Col(dcc.Graph(id="count"), md=8),
             dbc.Col(dcc.Graph(id="pie-chart"),  md=4),
            ]),
            
        dbc.Row([
            dbc.Col(dcc.Graph(id="sentiment_plot", ), md=8),
            
            dbc.Col(html.Iframe(id="tweet-iframe", src="https://twitframe.com/show?url=https://twitter.com/twitter/status/1509817484681134097", style={"width": "450px", "height":"450px", "margin": "10px"}), md = 4)# style=height:200px;width:300px;")),
], style={"border-style" : "solid", "margin": "10px"}),
             dbc.Row([
            
             dbc.Col([ html.H6("Topics and Domains", style={"margin-left":"10px"}),html.P("Click to expand"), dcc.Graph(id="sunburst_chart")], md=6),
             dbc.Col([html.H6("Location of Users",  style={"margin-left":"10px"}), dcc.Graph(id="pie-sunburst-locations")], md=6 ),
            ], ),
            dbc.Row([
            dbc.Col(dcc.Graph(id="common_words_bar_chart")),
            dbc.Col(dcc.Graph(id="hashtags_bar_chart"))
              ], ),
            
        #    dcc.Graph(id="sentiment")
        # dcc.Graph(id="count"),
        
        # dcc.Graph(id="sunburst_chart"),
    #   ##  dcc.Graph(id="pie-chart-locations"),
    #     dcc.Graph(id="pie-sunburst-locations")
        #dcc.Graph(id="common_words_bar_chart")
    ]

)



# dash_app
#.css.dash_app
#end_css({
#     "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
# })



@dash_app.callback(
    Output('output-div','children' ), 
    Output('memory-output','data'), 
    [Input('submit-button', 'n_clicks')],
    [State('search_keyword', 'value')], 
    
    )
def update_output(clicks, input_value):
        if clicks > 0:
            
            url = twitter.tweets_full_info_url(input_value,100)
            tweets = twitter.twitter_auth_and_connect(bearer_token, url)
            data = tweets
            data = str(data)
            data = eval(data)
            
            # print(data)
            # __local_storage = pd.json_normalize(tweets['data'])
            # print(__local_storage)
            # print(__local_storage["id"])
            # print("---------------------")
            # print(__local_storage["public_metrics.like_count"])
            
            # store_tweets(tweets, input_value)
            # store_users(tweets,input_value)
            return input_value, data

@ dash_app.callback(
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
    fig = px.line(final, x="start", y="tweet_count", labels={"start": "Day", "tweet_count": "No. of tweets"})
    
    # fig.update_layout( plot_bgcolor='rgb(10,10,10)')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        
        
    )
    return fig, __twitter_count



# @ dash_app.callback(
    
#     Output(component_id="sentiment", component_property="figure"),
#     Input(component_id="output-div", component_property="children"),
    


# )
# def generate_sentiment_graph(keyword):
#  if len(keyword) > 1 :
#     # tweets = twitter.search_hashtag_url(keyword, 10)
#     # store(tweets)
#     #
#     data = get_tweets(100, keyword)
    
   
#     sentiment_score = analyse(data)
    
#     # df = pd.DataFrame(sentiment_score)
#     df = pd.json_normalize(sentiment_score)
#     # print(df)
   
#     df["sentiment"] = df["sentiment.positive"] - df["sentiment.negative"]
#     # final = df[['text', 'sentiment']]
#     # print(df)
#     fig = px.bar(df, x=df.index, y='sentiment', hover_data=[
#         'text'], labels={'index': '#'}, color="sentiment", color_continuous_scale=px.colors.sequential.RdBu)
#    # fig = px.scatter(df, x="sentiment.positive",
#     # y="sentiment.negative")

#     # fig.update_layout(

#     #     plot_bgcolor=colors["background"],
#     #     paper_bgcolor=colors["background"],
#     #     font_color=colors["text"],
#     # )
#     return fig


@ dash_app.callback(
    
    Output(component_id="sentiment_plot", component_property="figure"),
    Output(component_id="number_of_likes", component_property="children"),
    Output(component_id="number_of_retweets", component_property="children"),
    Output(component_id="number_of_replies", component_property="children"),
    Input(component_id="memory-output", component_property="data")
    # Input(component_id="output-div", component_property="children")
   
)

def generate_sentiment_plot(data):
  if not (data == "none"):
    
    # tweets = twitter.search_hashtag_url(keyword, 10)
    # store(tweets)
    
    #data = get_tweets(100, keyword)
    
   
    # print("--------------- data -----------------")
    # print(local_storage)
    
    data = data['data']
    # print(data)
    likes = []
    retweets = []
    replies = []
    for i in data:
        likes.append(i["public_metrics"]["like_count"])
        retweets.append(i["public_metrics"]["retweet_count"])
        replies.append(i["public_metrics"]["reply_count"])
    # print(likes)
    # likes = data['public_metrics.like_count']
    # likes = data['public_metrics.like_count']
    
    # public_metrics = [d['public_metrics'] for d in data ]
    # likes = [d['like_count'] for d in public_metrics]
    
    # retweets = [d['retweet_count'] for d in public_metrics]
    # replies = [d['reply_count'] for d in public_metrics]
    # print("data\n---------------")
    # print(data)
   
    sentiment_score = analyse(data)
    tmp = []
    for i in data:
        tmp.append(i["id"])
    
    # print("tmp\n--------------------")
    # print(tmp)
    # for i in sentiment_score:
    #     sentiment_score.append(data["id"])
    
    # df = pd.DataFrame(sentiment_score)
    # print(sentiment_score)
    df = pd.json_normalize(sentiment_score)
    # print("df\n--------------------")
    df["id"] = tmp
    # print(df)
    
   
    
    #df["sentiment"] = df["sentiment.positive"] - df["sentiment.negative"]
    # final = df[['text', 'sentiment']]
    
    fig = px.scatter(df, x=df["sentiment.positive"], y=df["sentiment.negative"], hover_data=[
         'id'],  labels={'sentiment.positive': 'positive weight', 'sentiment.negative': 'negative weight', "sentiment.compound": "compound"}, color=df["sentiment.compound"], color_continuous_scale=px.colors.sequential.Blues, title="Sentiment of tweets")
    fig.update_layout(clickmode='event+select')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
        
    )

    fig.update_traces(marker_size=10)
   
   # fig = px.scatter(df, x="sentiment.positive",
    # y="sentiment.negative")

    # fig.update_layout(

    #     plot_bgcolor=colors["background"],
    #     paper_bgcolor=colors["background"],
    #     font_color=colors["text"],

    # )
    
    
    return fig, sum(likes), sum(retweets), sum(replies)


@dash_app.callback(
    Output("tweet-iframe", "src"),
    [Input("sentiment_plot", "clickData")],
)
def click(clickData):
    # print(clickData)
    points = clickData['points']
    # print(points)
    tmp = points[0]
    data = tmp['customdata']
    tweet_id = data[0]
    # print(tweet_id)
    
   
    url = "https://twitframe.com/show?url=https://twitter.com/twitter/status/{}".format(tweet_id)
    
    
   
    print(url)
    if not clickData:
        raise dash.exceptions.PreventUpdate
    
    return url


@ dash_app.callback(
    Output(component_id="pie-chart", component_property="figure"),
    Input(component_id="memory-output", component_property="data")
    # Input(component_id="output-div", component_property="children"),
   

)
def generate_pie(data):
 if not (data == "none"):
    # data = get_tweets(100, keyword)
    data = data['data']
    # print("--------------- json_sentiment -----------------")
    json_sentiment = get_sentiment_percentage(data)
    df = pd.json_normalize(json_sentiment)

    # print(df)

    #print(df.values)
    names = ['negative', 'neutral', "positive"]
    fig = px.pie(df, values=df.values[0], names=df.columns,
                 title='Percentage of Sentiment', color_discrete_sequence=px.colors.sequential.Blues)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
        
    )

    return fig


@ dash_app.callback(
    Output(component_id="sunburst_chart", component_property="figure"),
    Input(component_id="memory-output", component_property="data"),

)
def generate_sunburst(data):
  if not (data == "none"):
    data = data['data']
    context = {}
    context["domain"] = []
    context["entity"] = []
    df = pd.json_normalize(data)
    # print("--------------- normalize data for context -----------------")
    # print(df)
    for i in df['context_annotations']:
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
    #     data["domain_name"].dash_app
    #end(i)
    # for i in data.entity:
    #     data["entity_name"].dash_app
    #end(i)
    # print(data)
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
        data, path=['domain', 'entity'], values=[1]*len(data), labels={"value": "number"}, color_discrete_sequence=px.colors.sequential.Blues, title='Topics and Domains')
    fig.update_traces(insidetextorientation='radial')
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
        
    )
    #fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    #   plot_bgcolor=colors["background"],
    #   paper_bgcolor=colors["background"],
    #   font_color=colors["text"])

    return fig
# @ dash_app.callback(
#     Output(component_id="pie-chart-locations", component_property="figure"),
#     Output(component_id="number_of_users", component_property="children"),
#     Input(component_id="memory-output", component_property="data"),

# )
# def generate_pie(data):
#  if len(data) > 1 :
#     data = data['includes']
#     df = pd.json_normalize(data)
#     # print(df)
    
    
#     j = 0 
#     for i in df['location']:
        
#         if isinstance(i,str) == False:
           
#             df.at[j, "location"] = "Unknown"
#         j = j+1
#     # locations = df['location']
#     # df["location"].fillna(0)
    
#     fig = px.pie(df, values=[1]*len( df["location"]), names= df["location"],
#                  title='Location of Users', color_discrete_sequence=px.colors.sequential.Blues)

#     return fig, len(df["user"])
@ dash_app.callback(
    Output(component_id="pie-sunburst-locations", component_property="figure"),
    Output(component_id="number_of_users", component_property="children"),
    Input(component_id="memory-output", component_property="data"),

)
def generate_sunburst_locations(data):
  if not (data == "none"):
    data = data['includes']
    data = data['users']
    df = pd.json_normalize(data)
    
    j = 0 
    for i in df['location']:
        
        if isinstance(i,str) == False:
           
             df.at[j, "location"] = "Unknown"
        j = j+1
    # locations = df['location']
    # df["location"].fillna(0)
    
    
    # print(df)
    
    fig = px.sunburst(df, path=['location'], values=[1]*len(df["location"]),names=df["location"],labels={"null": "Unknown", "value": "# of users"},
                 title='Location of Users', color_discrete_sequence=px.colors.sequential.Blues)
    fig.update_traces(insidetextorientation='radial')
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
        
    )
    return fig, len(df) 

@ dash_app.callback(
    Output(component_id="common_words_bar_chart", component_property="figure"),
    Input(component_id="memory-output", component_property="data"),

)
def common_words_bar_chart(data):
 if not (data == "none"):
    # data = get_tweets(100, keyword)
    # print(data)
    data = data['data']
    tuples = common_words(data, 10)
    df = pd.DataFrame(tuples)
    df.rename(columns = {0 : 'Words', 1 : 'Occurances'}, inplace = True)
    # print(df)
  
    
    fig = px.bar(df, x=df["Occurances"], y=df['Words'], title='Common Words')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
        
    )

    return fig

@ dash_app.callback(
    Output(component_id="hashtags_bar_chart", component_property="figure"),
    Input(component_id="memory-output", component_property="data"),

)
def hashtags_bar_chart(data):
 if not (data == "none"):
    # data = get_tweets(100, keyword)
    # print(data)
    data = data['data']
    print("--------------  data ______________________-")
    print(data)
    data = [w["entities"] for w in data]
    print("-------------- entity data ______________________-")
    print(data)
    data = [w["hashtags"] for w in data]
    print("-------------- hashtag data ______________________-")
    tags = []
    for i in data:
        print(i)
        for j in i:
            print(j)
            tags.append(j['tag'])
    print(tags)
    fd = nltk.FreqDist(tags)
    print(fd)
    occurances = fd.most_common(10)
    print(occurances)
    df = pd.DataFrame(occurances)
    df.rename(columns = {0 : 'Hashtags', 1 : 'Occurances'}, inplace = True)
    
    
  
    
    fig = px.bar(df, x=df["Occurances"], y=df['Hashtags'], title='Common Hashtags')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
        
    )

    return fig


if __name__ == "__main__":
    dash_app.run_server(debug=True)
    # generate_pie("python")
