import re
import pandas as pd

def preprocess(data):
    patt = r'\[\d{2}\/\d{2}\/\d{2},\s\d{2}:\d{2}:\d{2}]\s'

    messages = re.split(patt, data)[1:]

    dates = re.findall(patt, data)

    df = pd.DataFrame({'date': dates, 'message': messages})
    
    df['date'] = df['date'].str.replace('[', '')
    df['date'] = df['date'].str.replace(']', '')


#     group_name = df.loc[df['message'].str.contains('added you')]['message'].str.split(':').str[0]
    group_name = df.loc[df['message'].str.contains('added you') | df['message'].str.contains('Messages and calls are end-to-end encrypted')]['message'].str.split(':').str[0]

    group_name = group_name.values[0]
    group_name

    df['date'] = pd.to_datetime(df['date'], format = '%d/%m/%y, %H:%M:%S ')
    # df['date'][0]
    df = df[1:]

    # df['sender'] = df.message.str.split(':').str[0]
    # df['message'] = df.message.str.split(':').str[1]

    df[['sender', 'message']] = df['message'].str.split(':', n=1, expand=True)

    # df['message'] = df['message'].str.encode('utf-8')
    df = df[['date', 'sender', 'message']]

    df['year'] = df['date'].dt.year
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['second'] = df['date'].dt.second
    df['month'] = df['date'].dt.month_name()
    df = df.loc[df['sender'] != group_name]
    
    df = df[['date', 'sender', 'message']]

    # df = df.loc[df['sender'] != '\u202a+91\xa095456\xa017572\u202c']
    # df = df.loc[df['sender'] != 'Haldi Mehendi -Dance prep']
    
    return df
