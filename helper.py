import pandas as pd
from urlextract import URLExtract
extract = URLExtract()
import emojis
from preprocess import preprocess

# plt.rcParams['font.family'] = 'DejaVu Sans'



def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['sender'] == selected_user]

        # sum_videos = len(df.loc[df['message'].str.contains('video omitted')])
        # sum_images = len(df.loc[df['message'].str.contains('image omitted')])
        # sum_messages = df.shape[0]
        # sum_links = len(df.loc[df['message'].str.contains('video omitted')])

    # df['message'] = df['message'].str.strip()
    # num_videos = len(df.loc[df['message'] == 'video omitted'])
    num_videos = len(df.loc[df['message'].str.contains('video omitted')])
    print(num_videos)
    print((df.loc[df['message'] == 'video omitted']))

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    # num_videos = df[df['message'] == r" \u200evideo omitted\n"].shape[0]
    # df['message'] = df['message'].str.strip()
    # num_videos = len(df[df['message'] == "video omitted"])
    num_images = len(df.loc[df['message'].str.contains('image omitted')])



    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_videos, num_images, len(links)
# , sum_videos, sum_images, sum_messages

def most_busy_users(df):
    # df = df['sender'].value_counts().sort_values(ascending=True)
    x = df['sender'].value_counts().sort_values()
    df = round((df['sender'].value_counts()/df['sender'].shape[0]) * 100, 2).reset_index().rename(columns = {'index':'name', 'sender': 'percent'})

    return x, df 


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['sender'] == selected_user]

    df_omm = df.copy()
    df_omm = df_omm.loc[df_omm['message'] != ' image omitted']
    df_omm = df_omm.loc[df_omm['message'] != 'U+021B1']
    df_omm = df_omm.loc[df_omm['message'] != '\u021B1']
    df_omm = df_omm.loc[df_omm['message'] != r' \u200e omitted\n']
    df_omm = df_omm.loc[df_omm['message'] != ' video omitted']
    df_omm = df_omm.loc[df_omm['message'] != ' GIF omitted']
    df_omm = df_omm.loc[df_omm['message'] != ' sticker omitted']
    df_omm = df_omm.loc[df_omm['message'] != ' Contact card omitted']
    df_omm = df_omm.loc[df_omm['message'] != ' audio omitted']
    df_omm = df_omm.loc[df_omm['message'] != ' Drinks S&H.pdf • 1 page document omitted']
    df_omm = df_omm.loc[df_omm['message'] != ' https']



    from collections import Counter
    f = open('stop_hinglish.txt', 'r')
    stopwords = f.read()

    words = []
    for m in df_omm['message']:
        for w in m.lower().split():
            if w not in stopwords:
                words.append(w)
                
    count = Counter(words)
    x = count.most_common(100)
    x = pd.DataFrame(x)
    x = x.reset_index(drop=True)
    x = x.rename(columns={"1":'frequency'})
    x = x.rename(columns={0: 'first', 1: 'second'}) 
    x = x.loc[x['first'] != 'omitted']
    x = x.loc[x['first'] != 'video']
    x = x.loc[x['first'] != 'image']
    x = x.loc[~x['first'].str.contains('image')]
    x = x.loc[~x['first'].str.contains('video')]
    x = x.dropna()
    # x['first'] = x['first'].str.replace('\u200E', '')
    x['first'] = x['first'].str.replace('@918170821166', '@kunal')
    x['first'] = x['first'].apply(lambda x: emojis.encode(x) if x else x)

    # import emoji

    # # Assuming df is your DataFrame with an 'emojis' column containing emojis

    # # Define a function to convert emojis
    # def convert_emoji(text):
    #     return emoji.emojize(text, use_aliases=True) if text else text

    # # Apply the convert_emoji function to the 'emojis' column
    # x['first'] = x['first'].apply(convert_emoji)


    # first_row_element = x.iloc[0, 0]
    return x


def day_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['sender'] == selected_user]

    df['day_name'] = df['date'].dt.day_name()
    return df


def linkslist(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['sender'] == selected_user]

    # extractor = URLExtract()
    # links = []
    # for message in df['message'].dropna():
    #     links.extend(extractor.find_urls(message))
    # links_df = pd.DataFrame({'links': links})



    extractor = URLExtract()
    links = []
    dates = []
    senders = []

    for index, row in df.iterrows():
        message = row['message']
        link = extractor.find_urls(message)
        if link:
            links.append(link[0])
            dates.append(row['date'])
            senders.append(row['sender'])

    links_df = pd.DataFrame({'date': dates, 'sender': senders, 'links': links})
    formatted_df = links_df.copy()

    # formatted_df['links'] = formatted_df['links'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

    # formatted_df = formatted_df.to_html(escape=False, index=False)

    return formatted_df



# def messages_df(selected_user, df):
#     if selected_user != 'Overall':
#         df = df[df['sender'] == selected_user]

#     df = preprocess(df)
#     print('down')
#     print(df)

#     return df
