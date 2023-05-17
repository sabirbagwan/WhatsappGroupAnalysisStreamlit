import streamlit as st
import preprocess, helper
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette("pastel")
sns.set_style("darkgrid")
import re

# import unicodedata
plt.rcParams['font.family'] = 'DejaVu Sans'
# plt.rcParams['font.family'] = 'Segoe UI Emoji'
# plt.rcParams['font.family'] = 'Twemoji'
from wordcloud import WordCloud



st.sidebar.title('Whatsapp text analysis!!')
# st.sidebar.write('Created by Sabir Bagwan')
st.sidebar.write('Created by <strong><em>SABIR BAGWAN</em></strong>', unsafe_allow_html=True)


# Display social media links in sidebar
st.sidebar.markdown("[Twitter](https://twitter.com/sabirbagwan_), \
                    [LinkedIn](https://www.linkedin.com/in/sabirbagwan/), \
                    [GitHub](https://github.com/sabirbagwan), \
                    [Kaggle](https://kaggle.com/sabirbagwan)")

st.sidebar.header("Disclaimer:")
st.sidebar.write("This Streamlit application for WhatsApp chat analysis has been created solely for academic and learning purposes. \
    The results and insights provided by the application should not be taken as accurate or definitive. \
        The creator of this application is not responsible for any actions taken based on the information provided by the application.")

# st.header('Want to do a short analysis of your Whatsapp group?')
st.markdown('<h2 style="text-align: center;">Want to do a short analysis of your Whatsapp group?</h2>', unsafe_allow_html=True)
# st.header('Follow along!')
st.markdown('<h3 style="text-align: center;">Follow along</h3>', unsafe_allow_html=True)

# st.header('Instructions to use')
# st.write("For seeing the analysis of your whataspp group chat, follow the instructions below:")

####################
st.markdown("1. Go to the mobile whatsapp")
st.markdown("2. Go to the group you want the anlysis for")
st.markdown("3. Go to the info page of the group")
st.markdown("4. Scroll down till you see 'Export Chat' and click over it")
st.markdown("5. Now choose 'Without Media'")
st.markdown("6. Save the .txt file")
st.markdown("7. And finally, Choose that file below. Done!")
st.markdown("8. If your file gets uploaded without any error, the chat will be displayed in a table format and now you \
            can choose an indivisual or the overall group analysis. And Click 'Go'")
st.markdown("Note: This app only works for the groups and not on indivisual chats")

#################
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocess.preprocess(data)
    st.dataframe(df)
    # df['extracted_value'] = df['sender'].apply(lambda x: re.findall(r'^(.*):.*added you', x)[0] if re.findall(r'added you', x) else '')

    # Remove rows with empty 'extracted_value'
    # df = df[df['extracted_value'] != '']
    # print(df['extracted_value'])
    # df.drop(df[df['extracted_value'] == ''].index, inplace=True)

# Reset the index if needed
    # df.reset_index(drop=True, inplace=True)


# Reset the index if needed
    # df.reset_index(drop=True, inplace=True)

    user_list = df['sender'].unique().tolist()
    # user_list.remove('Haldi Mehendi -Dance prep')

    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.selectbox("List of Users", user_list)

    if st.button("Go"):
        st.markdown('\n')
        st.markdown('<h2 style="text-align: center;">Analysis</h2>', unsafe_allow_html=True)
        st.markdown('\n')
        
        num_messages, words, num_images, num_videos, num_links = helper.fetch_stats(selected_user, df)



        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            # st.header('Total Mgs')
            st.markdown('<h5 style="text-align: center;">Total Mgs</h5>', unsafe_allow_html=True)
            st.markdown(f'<h5 style="text-align: center;">{num_messages}</h5>', unsafe_allow_html=True)
            # st.title(num_messages)

        with col2:
            # st.header('Total Words')
            # st.title(words)
            st.markdown('<h5 style="text-align: center;">Total Words</h5>', unsafe_allow_html=True)
            st.markdown(f'<h5 style="text-align: center;">{words}</h5>', unsafe_allow_html=True)

        with col3:
            # st.header('Images Shared')
            # st.title(num_images)
            st.markdown('<h5 style="text-align: center;">Total Images</h5>', unsafe_allow_html=True)
            st.markdown(f'<h5 style="text-align: center;">{num_images}</h5>', unsafe_allow_html=True)

        with col4:
            # st.header('Videos Shared')
            # st.title(num_videos)
            st.markdown('<h5 style="text-align: center;">Total Videos</h5>', unsafe_allow_html=True)
            st.markdown(f'<h5 style="text-align: center;">{num_videos}</h5>', unsafe_allow_html=True)

        with col5:
            # st.header('Total Links')
            # st.title(num_links)
            st.markdown('<h5 style="text-align: center;">Total Links</h5>', unsafe_allow_html=True)
            st.markdown(f'<h5 style="text-align: center;">{num_links}</h5>', unsafe_allow_html=True)

        
        if selected_user == 'Overall':

            st.markdown('\n')
            st.markdown('<h3 style="text-align: center;">Most Active User</h3>', unsafe_allow_html=True)

            x, y = helper.most_busy_users(df)
            x_sorted = x.sort_values(ascending=False)  # Sort values in descending order
            x_top10 = x_sorted.head(10)  # Select top 10 values
            fig, ax = plt.subplots()
            col1 = st.columns(1)[0]  # Use only one column instead of two

            with col1:
                ax = sns.barplot(x=x_top10.values, y=x_top10.index)
                st.pyplot(fig)

#################################### Most Used Words ############################################

        st.markdown('\n')
        st.markdown('<h3 style="text-align: center;">Most Used Words</h3>', unsafe_allow_html=True)
        x= helper.most_common_words(selected_user, df)
        x = x[:10]
        # print(x)
        x = x[1:]
        # print(x)['First'][0]
        # print('This')

        # first_row_element = x.iloc[0, 0]

# Check if the element is an empty string or "nothing"
        # if not first_row_element:
            # print("The element is empty or represents 'nothing'")
        # else:
    # Get the Unicode code point value
            # code_point = ord(first_row_element)
    # Get the character name using Unicode code point
            # char_name = unicodedata.name(first_row_element)

            # print(f"The element represents the character '{first_row_element}'")
            # print(f"Unicode code point: {code_point}")
            # print(f"Character name: {char_name}")


        # print(x.iloc[0, 0])
        # x = x.iloc[4:, :]
        fig, ax = plt.subplots()

        col1 = st.columns(1)[0] 

        with col1:
            sns.set_palette("pastel")
            sns.set_style("darkgrid")
            ax = sns.barplot(data=x, y='first', x='second')
            ax.set_xlabel('')
            ax.set_ylabel('')
            st.pyplot(fig)


#################################### Most Busy days ############################################


        st.markdown('\n')
        st.markdown('<h3 style="text-align: center;">Most Busy days</h3>', unsafe_allow_html=True)


        x= helper.day_stats(selected_user, df)

        fig, ax = plt.subplots()

        col1 = st.columns(1)[0] 

        with col1:
            sns.set_palette("pastel")
            sns.set_style("darkgrid")
            ax = sns.barplot(x=x['day_name'].value_counts().sort_values(ascending=False), \
                             y=x['day_name'].value_counts().sort_values(ascending=False).index)
            ax.set_xlabel('')
            ax.set_ylabel('')
            st.pyplot(fig)


#################################### Messages ############################################

        # st.markdown('\n')
        # st.markdown('<h3 style="text-align: center;">All Messages</h3>', unsafe_allow_html=True)

        # x = helper.messages_df(selected_user, df)

        # st.dataframe(x)

        # st.dataframe(x)
        # st.markdown(x, unsafe_allow_html=True)






#################################### links list ############################################

        st.markdown('\n')
        st.markdown('<h3 style="text-align: center;">Links Shared</h3>', unsafe_allow_html=True)

        x = helper.linkslist(selected_user, df)

        # st.dataframe(x)

        st.dataframe(x)
        # st.markdown(x, unsafe_allow_html=True)





#################################### Word Cloud ############################################

        st.markdown('\n')
        st.markdown('<h3 style="text-align: center;">Word Cloud</h3>', unsafe_allow_html=True)

        x= helper.most_common_words(selected_user, df)
        # st.dataframe(x)
        text = ' '.join(caption for caption in x['first'])

        wordcloud = WordCloud(width=500, height=350, background_color='black').generate(text)

        st.image(wordcloud.to_image(), use_column_width=True)
