import pandas as pd
import numpy as np
import yake
import plotly.express as px
import plotly.graph_objects as go
import re
import streamlit as st
import json
import requests
from streamlit_lottie import st_lottie

styl = f"""
<style>
    .div.css-1p1nwyz eltzin5v2{{
        margin-top: -200px;
    }}
    }}
</style>
"""
st.markdown(styl, unsafe_allow_html=True)


us = pd.read_csv("./data/cleaned/us.csv")
dc = pd.read_csv("./data/cleaned/dc.csv")
us  = us.drop(us.columns[[0,1]], axis = 1)
dc  = dc.drop(dc.columns[[0,1]], axis = 1)
full = pd.concat([dc,us], axis = 0, ignore_index= True)
full.city = [city.strip() for city in full.city]

extractor = yake.KeywordExtractor()
language = "en"
max_ngram_size = 3
deduplication_threshold = 0.9
keywords = 5
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=keywords, features=None)

def load_lottieurl(url):
    r  = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

l1 = load_lottieurl('https://assets3.lottiefiles.com/packages/lf20_1t8na1gy.json')
l2 = load_lottieurl('https://assets10.lottiefiles.com/packages/lf20_qqu8eybe.json')
l3 = load_lottieurl('https://assets1.lottiefiles.com/packages/lf20_s5dhjbui.json')
l4 = load_lottieurl('https://assets5.lottiefiles.com/packages/lf20_lzhwcgzg.json')
l5 = load_lottieurl('https://assets7.lottiefiles.com/packages/lf20_s2w5hjb5.json')
l6 = load_lottieurl('https://assets3.lottiefiles.com/packages/lf20_jPB3pa66pI.json')




# with st.sidebar:
#     st_lottie(l3, key = "1",height = 600,width = 300)



def intro():
    st.balloons()
    with st.sidebar:
        st.write("Welcome! Please use the above dropdown to navigate through the website :) ")
        st_lottie(l1, key = "two",height = 600,width = 300)

    col1, col2 = st.columns([2,1])
    col1.title("Post Graduation Data Science Job Prospect Analysis")
    with col2:
        st_lottie(l3, key = "three",height = 200,width = 300)

    st.write("In this analysis, we analyze the Data Science job postings acquired through google jobs in order to examine the different needs of a prospective Data Scientist who are trying to enter the world of Data Science.")
    st.write("In the recent years, since COVID-19, the so called 'excitement' of silicon valley technology jobs have dimished, as more people sought for security of occupation in the times of uncertainty." )
    st.write("Even myself, whose dream was the initially go work for the FAANG companies, have drastically changed my mind to staying in the consumer product goods sector of business, in order to learn and engage in a certain job security environment.")
    st.write("With the collected JSON dataset, we first extracted the important information that any job description could yield: Job Title, Company Name, City, State, Job Description, Qualificiations, Responsibilities, Benefits, Role Type, and Salary.")
    st.write("Through the dataset, we aim to answer one large question, and guide the readers to make logical decisions using data behind their job choices.")
    st.write("Main Question: Is District of Columbia Attractive for Data Scientists?")
    st.write("Then, we move on to the next phase, where we introduce a several logical interactive visualizations steps to make educated choice about the prospective job position a student may consider.")

    st.subheader("Data Table")

    st.write("Because not all observations contained complete set of features, many were deleted by need basis depending on the visualization. Because the missing value feature is not consistent throughout each observations, it was inevitable to leave the missing values as it is before diving into the visualizations. For more information on the missing values, please refer to each sections of the code to see what data manipulation process has been taken through.")
    st.write("Lastly, the below is the interactive data table that users can utilize to examine the data further. Because the analysis utilizes keyword extraction, for which a full sentence structure is critical, only minimal data cleaning proces was done for the text dataset. For the regex expressions, it was deleted in a need basis.")

    st.dataframe(full)

def DC():
    with st.sidebar:
            
            st.sidebar.header("Why District of Columbia?")
            st.sidebar.write("District of Columbia, as the Georgetown students belovedly stay, has become one of the centers of Data Science careers in the past few years. With bigger technology companies inflowing into the city and vicinity, the amount of opportunity has risen significantly than the past.")
            st.sidebar.write("With such facts in mind, the project first dives into the aspect of what would attract Georgetown and District of Columbia for future prospective students? Or even, what could DC offer for the current Data Science students to stay after their graduation?")
            st.sidebar.write("In order to answer those questions, we look at several factors below: ")
            st.sidebar.write("- Is DC Salary competitive enough to convince the current students to stay after graduation?")
            st.sidebar.write("- Which students of domain of interest should stay in District of Columbia?")
            st.sidebar.write("- Does the distribution of District of Columbia Data Science salary deviate significantly from the traditional tech hubs?")
            st.sidebar.write("- In comparison to other top Data Science friendly cities, how does DC perform in regards to job offerings?")

    col1, col2 = st.columns([3,2])
    col1.title("Is DC Attractive for Data Science?")
    with col2:
        st_lottie(l2, key = "one",height = 150,width = 200)


    st.write("Hope you enjoyed the short summary read of the sidebar over there! Let's get started with the fun stuff :) ")
    st.write("We first look at the average Minimum and Maximum Salary for different domain of focus in Data Science for District of Columbia versus Remininag United States.")
    st.write("Overall, as one can see from the two plots below, the DC minimum average salary is quite simliar to that of the remaining parts of the US, whereas for the maximum salary, the reamining parts of US seem to be a little bit higher.")
    st.write("In an attempt to further analyze why such is the cause, we next examine by each domain comparatively, to see if there are specific domains that pays better in DC.")
    
    d_p_1 = full.groupby(['location','domain'], as_index=False).mean(['min_salary','max_salary']).dropna()
    def plot1():    
        fig1 = px.scatter(d_p_1, 
            x= d_p_1.index.to_list(), 
            y = 'min_salary', 
            color  = 'location', 
            hover_data  = 'domain',
            labels = dict(x = "", min_salary = 'Minimum Salary (in Million USD)'),
            title = "Distribution of Minimum Salary Ranges Overall (DC vs. US)")

        fig1.update_traces(marker = dict(size =20,
                                        line = dict(width =2)))

        fig1.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })

        st.plotly_chart(fig1,theme="streamlit", use_container_width=False)

    def plot2():
        fig2 = px.scatter(d_p_1, 
            x= d_p_1.index.to_list(), 
            y = 'max_salary', 
            color  = 'location', 
            hover_data  = 'domain',
            labels = dict(x = "", max_salary = 'Maximum Salary (in Million USD)'),
            title = "Distribution of Maximum Salary Ranges Overall (DC vs. US)")

        fig2.update_traces(marker = dict(size =20,
                                        line = dict(width =2)))

        fig2.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })

        st.plotly_chart(fig2,theme="streamlit", use_container_width=True)    

    with st.container():
        tab1, tab2, tab3 = st.tabs(["Average Minimum Salary", "Average Maximum Salary", '(Hide Plot)'])

        with tab1:
            plot1()


        with tab2:
            plot2()

    st.write("As one can see from the plot below, the DC based companies generally do tend to pay less than that of the reamining United States.")
    st.write("However, when it comes to the payroll for the Data Scientists, it is very clear that the average minimum salary of the data scientists on average are quite higher than the average of the United States.")
    st.write("This suggests that our premise in the introduction, 'DC has increasing number of technology companies influx', may be holding up. However, since all other categories seem to not pay out as well as the reamining US, further investigation has to be done in order to solidify our assumptions.")

    def plot3():
        fig4 = px.bar(d_p_1, x = "location", 
                    y = "min_salary", 
                    color = "location", 
                    barmode = "group", 
                    facet_col="domain", 
                    facet_col_wrap=3, 
                    width = 600, height = 800,
                    labels = dict(x = "", min_salary = 'Maximum Salary (USD)'),
                    title = "Average Minimum Salary by Domain (DC vs. US)")
                    

        for axis in fig4.layout:
            if type(fig4.layout[axis]) == go.layout.XAxis:
                fig4.layout[axis].title.text = ''

        fig4['layout']['xaxis2']['title']['text']= ""    

        fig4.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

        for axis in fig4.layout:
            if type(fig4.layout[axis]) == go.layout.YAxis:
                fig4.layout[axis].title.text = ''

        fig4.add_annotation(x=-0.1,y=0.5,
                        text="Maximum Salary (USD)", textangle=-90,
                            xref="paper", yref="paper")

        fig4.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })

        st.plotly_chart(fig4,theme="streamlit", use_container_width=True)

    with st.container():

        tab1, tab2 = st.tabs(["Average Minimum Salary by Domain",'(Hide Plot)'])

        with tab1:
            plot3()

    st.write("Following the analysis above, we wanted to check whether the average minimum salary of DC was lower than that of the remaining US because of outliers or, whether it is actually normally distributed and does payout lower.")
    st.write("In doing so, we plotted a violin plot to show how the distribution of the payouts look like for DC versus United States. As one can imagine, our first sight for this graph should go to the Datat Scientist section, as it was the only category that DC had better payments than the US.")
    st.write("As one can see from the violin plot, the Data Scientists' payroll in the District of Columbia seems to be normally distributed with the wide range ranging form  41.6K to 608K per year. Althoguht the range is quite large, we can also see that most data scientists' job description expected payroll seems to be around the mean value, ensuring normal distribution.")
    st.write("Lastly, sadly, all the reamining positions seem to be confirmed that the reamining companies outside of the DC area does actually pay better when it is not a general 'Data Science' position.")

    def plot4():
        fig5 = px.violin(full, 
                        y="min_salary", 
                        x="location", 
                        color="location", 
                        box=True,
                        log_y=False, 
                        points="all",
                        facet_col='domain', 
                        facet_col_wrap = 5, 
                        width = 1000, height = 700,
                        title = "Distribution of Salary by Domain (DC vs. US)")

        fig5.update_yaxes(matches=None)

        for axis in fig5.layout:
            if type(fig5.layout[axis]) == go.layout.XAxis:
                fig5.layout[axis].title.text = ''

        fig5['layout']['xaxis2']['title']['text']= ""    

        fig5.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

        for axis in fig5.layout:
            if type(fig5.layout[axis]) == go.layout.YAxis:
                fig5.layout[axis].title.text = ''

        fig5.add_annotation(x=-0.1,y=0.5,
                        text="Minimum Salary (USD)", textangle=-90,
                            xref="paper", yref="paper")

        fig5.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })

        st.plotly_chart(fig5,theme="streamlit", use_container_width=True)

    with st.container():

        tab1, tab2 = st.tabs(["Distribution of Minimum Salary by Domain", '(Hide Plot)'])

        with tab1:
            plot4()

    st.write("Finally, we wanted to take a look at how many jobs are being offered in the Top 5 cities besides Washington, DC to show if there is a disparity of work availability in the Data Science field.")
    st.write("As one can see form the facet bar plots below, Washing ton has a high number of open positions for Data Analyst, Data Scientist prominently. However, for Blockchain, Neural Networks, and Time Series, there does not seem to be a lot of availability of work in the field.")
    st.write("From intution, we can deduct that, Washington, as the center of government of the United States, serves as a trustworthy analytical hub, but also has to be specially careful about the data leakage. Therefore, it is clear that the data that circulates DC, is more utilized to anlayze and observe, rather than building blockchians or consturcting neural networks that may violate privacy.")
    def plot5():
        d_p_2 = full.groupby(['city','domain'], as_index=False).count().dropna()

        x = []
        for i in range(d_p_2.shape[0]):
            if d_p_2.loc[i,"city"].strip() in ['New York', "Washington", "Anywhere", "San Francisco", "Annapolis Junction"]:
                x.append(True)
            else:
                x.append(False)

        d_p_2 = d_p_2[x].reset_index()

        fig6 = px.bar(d_p_2, x = "city", 
                    y = "location", 
                    color = "city", 
                    barmode = "group", 
                    facet_col="domain", 
                    facet_col_wrap=3, 
                    width = 1000, height = 1000,
                    labels = dict(x = "", min_salary = 'Maximum Salary (USD)'),
                    title = "Number of Jobs in Top 5 Job Count Cities by Domain")
                    
        fig6.update_traces(width=1)
        fig6.update_yaxes(matches=None)

        for axis in fig6.layout:
            if type(fig6.layout[axis]) == go.layout.XAxis:
                fig6.layout[axis].title.text = ''

        fig6['layout']['xaxis2']['title']['text']= ""    

        fig6.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

        for axis in fig6.layout:
            if type(fig6.layout[axis]) == go.layout.YAxis:
                fig6.layout[axis].title.text = ''

        fig6.add_annotation(x=-.01,y=0.5,
                        text="Maximum Salary (USD)", textangle=-90,
                            xref="paper", yref="paper")

        fig6.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })

        st.plotly_chart(fig6,theme="streamlit", use_container_width=True)

    with st.container():

        tab1, tab2 = st.tabs(["Job Opportunity Count by Top 5 Cities", '(Hide Plot)'])

        with tab1:
            plot5()

    st.write("In summary, we have seen that DC is a hub spot for Data Scientists and Data Analyst. And if our students in Georgetown are interested in portions of Data Science focusing on the anlaytical work, rather than the 'state of the arc' Data Science work, DC, actually may be a good place to stay after graduation. Further, with a pay that is often significanlty higher than the reamining cities as a well positioned Data Scientists, Georgetown can also attract students in advertising for our good job sercurity and high yielding payments post graduation in the local area. ")

def suggestions():
    with st.sidebar:
        st.header("Where is your Ideal Occupation?")
        st.write("In this section, rather than explaining like we have in the 'Why District of Columbia?' section, the focus is the interactivity of the visualizations, and help the users guide through their job application process, ensuring the logic behind their decision to choose certain jobs or areas.")
        st.write("At the end of each section, there is a final recommendation of job listings that I found the users to be most apt for. The keywords give the users a sense how what to prepare for the job if given an interview, or what to expect from the job as well. The bigrams to trigrams were extracted using Keyword Extraction software which I hypertuned myself. With the support from the results, I hope that this information can help current and future students in seelecting their future occupation and prepare for what is coming.")
        st.write("With that being said, we first ask the users to answer a simple question in the main page and follow along the guidelines and enjoy the flow :) ")
    
    col1, col2 = st.columns([4,2])
    col1.title("What is more important to you? Location or Domain of focus?")
    with col2:
        st_lottie(l4, key = "four",height = 250,width = 300)

    path = st.selectbox("Choose your Journey!", ["LOCATION","DOMAIN"])

    st.write("If you have chosen 'LOCATION' : ")

    st.write("The bubble plot below shows you the number of jobs available in each state by the size of the bubles, while also showing the average minimum and maximum salary of the given state for the entire dataset. The plot is designed so that the users can choose what aspect of their job search process they would appreciate. First, by looking at the magnitutde of the markers, the users can understand the breadth of opportunites in each state; which without a doubt, California has the abudnace of, followed by Maryland and Virgina. Next, one of the highest paying jobs was New York with average minimum salary of 130k and maximum of 200k per year. This will allow the users to choose a state that will be tailored for their needs.")

    st.write("If you have chosen 'DOMAIN' :")
    st.write("The bubble plot below shows you the average salary for both minimum and maximum of each domain of expertise in the field of Data Science. From this plot, users can have multiple takeaways. First, if a current or prospective student, depending on the pay range of their desired choice, he or she can decide to partake in the courses that will lead to higher payments. For isntance, with reinforcement learning jobs garnering much higher pay han the other possible domains, if a student is seeking for higher pay over a specific domain field experience, he or she may be more inclined to take a Reinforcement Learning course prior to graduation.")


    if path == "LOCATION":
        dp3 = full.groupby(['state'], as_index=False).count().dropna()
        dp4 = full.groupby(['state'], as_index=False).mean(['min_salary', 'max_salary'])
        dp5 = dp3.merge(dp4, how = 'inner', on = 'state')
        dp5 = dp5[['state','min_salary_y', 'max_salary_y', 'location']].dropna()

        def plot6():
            fig7 = px.scatter(dp5, 
                    x= 'max_salary_y', 
                    y = 'min_salary_y', 
                    color  = 'location', 
                    hover_data  = 'state',
                    labels = dict(max_salary_y = "Average Maximum Salary (USD)", min_salary_y = "Average Minimum Salary (USD)", location = "Number of Jobs"),
                    title = "Number of Jobs according to Min/Max Salary by State")

            fig7.update_traces(marker = dict(size = dp5['location'],
                                            line = dict(width =2)))

            fig7.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            })

            st.plotly_chart(fig7,theme="streamlit", use_container_width=True)
        
        with st.container():

            tab1, tab2 = st.tabs(["Opportunity Count, Average Minimum/Maximum Salary (USD)", 'salary'])

            with tab1:
                plot6()

        options = dp5.state.unique().tolist()
        states = st.selectbox("select state", options)

        cities = full[full['state'] == states].city.unique().tolist()
        x = []
        for i in range(full.shape[0]):
            if full.loc[i,"city"] in cities:
                x.append(True)
            else:
                x.append(False)

        dp6 = full[x].reset_index()

        dp7 = dp6.groupby(['city','domain'], as_index=False).mean(['min_salary','max_salary']).dropna() 

        print(dp7.head())
        with st.container():
            def plot7():
                fig8 = px.bar(dp7, x = "city", 
                            y = "min_salary", 
                            color = "city", 
                            barmode = "group", 
                            facet_col="domain", 
                            facet_col_wrap=3, 
                            width = 800, height = 800,
                            labels = dict(x = "", min_salary = 'Maximum Salary (USD)'),
                            title = f"Average Minimum Salary by Domain {states}")
                fig8.update_traces(width=1)
                fig8.update_yaxes(matches=None)             

                for axis in fig8.layout:
                    if type(fig8.layout[axis]) == go.layout.XAxis:
                        fig8.layout[axis].title.text = ''

                # fig8['layout']['xaxis2']['title']['text']= ""    

                fig8.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

                for axis in fig8.layout:
                    if type(fig8.layout[axis]) == go.layout.YAxis:
                        fig8.layout[axis].title.text = ''

                fig8.add_annotation(x=-0.1,y=0.5,
                                text="Maximum Salary (USD)", textangle=-90,
                                    xref="paper", yref="paper")

                fig8.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                })

                st.plotly_chart(fig8,theme="streamlit", use_container_width=True)



            tab1, tab2 = st.tabs(["Average Minimum Salary by Domain", '(Hide Plot)'])

            st.write("If you have chosen 'LOCATION' : ")
            st.write("Now that you have chosen your choice of state, now it's time to look into what domain is the best paying area of focus in the Data Science field in the state! For the purpose of demonstration, I recommend viewing this plot with California selected. Since may companies do not tell about their salary ranges, some states have minial amounts of data whenm it comes to salaray range when state specific. Nonetheless, as you can see from (if you chose CA), the plot below, it is evident that majority of the cities in California have positions for neural networks, and extremely paid well as well. However, the point of this plot is for the users to be able to see which cities might have the best option for their area of focus. But for the case of those who wanted to move to Clifornia, one of the prime reasons why they wanted to move to California would have been for the advanced technology, thus neural net would also fit perfectly. ")

            with tab1:
                plot7()
            
            
            available_domains = dp7.domain.unique().tolist()
            domain_select_1 = st.selectbox("select domain", available_domains)   

        dp8 = dp6[dp6['domain'] == domain_select_1]
        top_jobs_1 = dp8.sort_values(by = "min_salary")[:3].reset_index()

        st.write("The Best Job Fit for you would be in",states, "working in domain of", domain_select_1)
        st.write("Here are the Top 3 Job Recommendations for you and the requirements!")        

        def plot8():
            x1 = custom_kw_extractor.extract_keywords(top_jobs_1.responsibility[0])
            st.write("Responsibility Top5 Keywords")
            fig9 = go.Figure([go.Bar(
            x=[t[0] for t in x1],
            y=[t[1] for t in x1],
            text= [t[0] for t in x1])])
            fig9.update_xaxes(visible=False)
            st.plotly_chart(fig9,theme="streamlit", use_container_width=True)

            st.write("Qualification Top5 Keywords")
            y1 = custom_kw_extractor.extract_keywords(top_jobs_1.qualification[0])
            fig10 = go.Figure([go.Bar(
            x=[t[0] for t in y1],
            y=[t[1] for t in y1],
            text= [t[0] for t in y1])])
            fig10.update_xaxes(visible=False)
            st.plotly_chart(fig10,theme="streamlit", use_container_width=True)    

            z1 = custom_kw_extractor.extract_keywords(top_jobs_1.description[0])
            st.write("Description Top5 Keywords")
            fig11 = go.Figure([go.Bar(
            x=[t[0] for t in z1],
            y=[t[1] for t in z1],
            text= [t[0] for t in z1])])
            fig11.update_xaxes(visible=False)
            st.plotly_chart(fig11,theme="streamlit", use_container_width=True)        

        def plot9():
            x1 = custom_kw_extractor.extract_keywords(top_jobs_1.responsibility[1])
            st.write("Responsibility Top5 Keywords")
            fig9 = go.Figure([go.Bar(
            x=[t[0] for t in x1],
            y=[t[1] for t in x1],
            text= [t[0] for t in x1])])
            fig9.update_xaxes(visible=False)
            st.plotly_chart(fig9,theme="streamlit", use_container_width=True)
            st.divider()
            st.write("Qualification Top5 Keywords")
            y1 = custom_kw_extractor.extract_keywords(top_jobs_1.qualification[1])
            fig10 = go.Figure([go.Bar(
            x=[t[0] for t in y1],
            y=[t[1] for t in y1],
            text= [t[0] for t in y1])])
            fig10.update_xaxes(visible=False)
            st.plotly_chart(fig10,theme="streamlit", use_container_width=True)    
            st.divider()
            z1 = custom_kw_extractor.extract_keywords(top_jobs_1.description[1])
            st.write("Description Top5 Keywords")
            fig11 = go.Figure([go.Bar(
            x=[t[0] for t in z1],
            y=[t[1] for t in z1],
            text= [t[0] for t in z1])])
            fig11.update_xaxes(visible=False)
            st.plotly_chart(fig11,theme="streamlit", use_container_width=True)     

        def plot10():
            x1 = custom_kw_extractor.extract_keywords(top_jobs_1.responsibility[2])
            st.write("Responsibility Top5 Keywords")
            fig9 = go.Figure([go.Bar(
            x=[t[0] for t in x1],
            y=[t[1] for t in x1],
            text= [t[0] for t in x1])])
            fig9.update_xaxes(visible=False)
            st.plotly_chart(fig9,theme="streamlit", use_container_width=True)

            st.write("Qualification Top5 Keywords")
            y1 = custom_kw_extractor.extract_keywords(top_jobs_1.qualification[2])
            fig10 = go.Figure([go.Bar(
            x=[t[0] for t in y1],
            y=[t[1] for t in y1],
            text= [t[0] for t in y1])])
            fig10.update_xaxes(visible=False)
            st.plotly_chart(fig10,theme="streamlit", use_container_width=True)    

            z1 = custom_kw_extractor.extract_keywords(top_jobs_1.description[2])
            st.write("Description Top5 Keywords")
            fig11 = go.Figure([go.Bar(
            x=[t[0] for t in z1],
            y=[t[1] for t in z1],
            text= [t[0] for t in z1])])
            fig11.update_xaxes(visible=False)
            st.plotly_chart(fig11,theme="streamlit", use_container_width=True)     




        with st.container():

            tab1, tab2, tab3 = st.tabs(["Candidate Job 1", "Candidate Job 2", "Candidate Job 3"])

            with tab1:
                st.write("Postion:",top_jobs_1.position[0])
                st.write("Company:", top_jobs_1.company_name[0])
                st.write("Minimum Salary:",top_jobs_1.min_salary[0])
                st.write("Maximum Salary:", top_jobs_1.max_salary[0])
                st.divider()
                plot8()

            with tab2:
                st.write("Postion:",top_jobs_1.position[1])
                st.write("Company:", top_jobs_1.company_name[1])
                st.write("Minimum Salary:",top_jobs_1.min_salary[1])
                st.write("Maximum Salary:", top_jobs_1.max_salary[1])
                st.divider()                
                plot9()

            with tab3:
                st.write("Postion:",top_jobs_1.position[2])
                st.write("Company:", top_jobs_1.company_name[2])
                st.write("Minimum Salary:",top_jobs_1.min_salary[2])
                st.write("Maximum Salary:", top_jobs_1.max_salary[2])
                st.divider()                
                plot10()
        
    if path == "DOMAIN":
        dp9 = full.groupby(['domain'], as_index=False).mean(['min_salary','max_salary']).dropna()
        dp10 = full.groupby(['domain'], as_index=False).count()
        dp10 = dp10[['domain','location']]
        dp11 = dp9.merge(dp10, how = 'inner', on = 'domain')



        with st.container():
            def plot11():
                fig12 = px.scatter(dp11, 
                    x= 'max_salary', 
                    y = 'min_salary', 
                    color  = 'domain', 
                    hover_data  = 'domain',
                    labels = dict(max_salary = "Average Maximum Salary (USD)", min_salary = "Average Minimum Salary (USD)", location = "Number of Jobs"),
                    title = "Number of Jobs according to Min/Max Salary by Domain")

                fig12.update_traces(marker = dict(size = dp11['location'],
                                                line = dict(width =1)))

                fig12.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                })

                st.plotly_chart(fig12,theme="streamlit", use_container_width=True)
            
            tab1, tab2 = st.tabs(["Occupation Count by Minimum/Maximum Salary (Domain)", 'plot '])

            with tab1:
                plot11()

            possilbe_domains_2 = dp11.domain.unique().tolist()
            domain_2 = st.selectbox("SELECT Domain", possilbe_domains_2)

            dp12 = full[full['domain'] == domain_2].reset_index().groupby(['state'], as_index = False).mean(['min_salary','max_salary']).dropna()
            dp13 = full[full['domain'] == domain_2].reset_index().groupby(['state'], as_index = False).count()
            dp13 = dp13[['state','location']]
            dp14 = dp12.merge(dp13, how = 'inner', on = 'state')

            def plot12():
                fig13 = go.Figure([go.Bar(
                x=dp14['state'],
                y=dp14['min_salary'],
                text= dp14['state'],
                )])

                fig13.update_layout(
                    title=f"Minimum Salary Average for Top States of Domain: {domain_2}",
                    xaxis_title="State",
                    yaxis_title="Average Minimum Salary (USD)",
                )
                fig13.update_xaxes(visible=False)

                st.plotly_chart(fig13,theme="streamlit", use_container_width=True)

            
            tab1, tab2 = st.tabs(["Average Minimum Salary from Top States (Domain)", 'plot '])

            st.write("If you have chosen 'DOMAIN' :")
            st.write("For the case of Domain, the approach is the opposite from the LOCATION pathway. Instead of choosing the 'prime place of living', we are first going to focus on 'prime area of domain area of focus'. As a users chooses a domain of interest, the plot will show a simple barplot of average minimum salary of top states for the given domain. With such information, from the domain to state to city, the users can narrow down their scope of occupation location. Further, once the user chooses a city of interest, a datatable of the salary range and index number of the observation will be shown, such that users can reference the data table in the introduction if needed more information.")

            with tab1:
                plot12()

            possible_states = dp14.state.unique().tolist()

            state_2 = st.selectbox("SELECT STATE", possible_states)

            dp14 = full[full['domain'] == domain_2].reset_index()
            x = []
            for i in range(dp14.shape[0]):
                if dp14.state[i] == state_2:
                    x.append(True)
                else:
                    x.append(False)

            dp15 = dp14[x].reset_index()

            dp16 = dp15.groupby(['city'], as_index=False).mean(['min_salary']).dropna()
            st.table(dp16)
            dp17 = dp15.groupby(['city'], as_index=False).count()
            dp17 = dp17[['city','location']]
            dp18 = dp16.merge(dp17, how = 'inner', on = 'city')

            def plot13():
                fig14 = px.scatter(dp18, 
                        x= 'max_salary', 
                        y = 'min_salary', 
                        # color  = dp18['location'], 
                        hover_data  = 'city',
                        labels = dict(max_salary = "Average Maximum Salary (USD)", min_salary = "Average Minimum Salary (USD)", location = "Number of Jobs"),
                        title = f"Number of Jobs according to Min/Max Salary in {state_2} Cities")

                fig14.update_traces(marker = dict(size = dp18['location']*100,
                                                line = dict(width =1)))

                fig14.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                })
                st.plotly_chart(fig14,theme="streamlit", use_container_width=True)
            
            st.write("If you have chosen 'DOMAIN' :")
            st.write("Lastly, once the user chooses a city of choice within the state of choice, the scatterplot will be generated to show the number of jobs avaialble, versus minimum and maximum salary on average for the respective city. Through this, the users can make educated choice as to their payroll range and breadth of job opportunities that they have.")
        
            tab1, tab2 = st.tabs(["Occupation vs. Salary by State Scatterplot", 'plot '])

            if dp18.shape[0] ==0:
                st.write("No jobs found! Try other cities :) ")
            else:
                with tab1:
                    plot13()        
        
                possible_cities_3 = dp18.city.unique().tolist()
                cities_3 = st.selectbox("SELECT", possible_cities_3)

                dp19 = full[full['domain'] == domain_2].reset_index()
                dp20 = dp19[dp19['city'] == cities_3]
                top_jobs_3 = dp20.sort_values(by = "min_salary")[:3].reset_index()

        st.write("The Best Job Fit for you would be in the domain of",domain_2, "located in",cities_3, ",", state_2)
        st.write("Here are the Top 3 Job Recommendations for you and the requirements!")        

        def plot14():
            x1 = custom_kw_extractor.extract_keywords(top_jobs_3.responsibility[0])
            st.write("Responsibility Top5 Keywords")
            fig9 = go.Figure([go.Bar(
            x=[t[0] for t in x1],
            y=[t[1] for t in x1],
            text= [t[0] for t in x1])])
            fig9.update_xaxes(visible=False)
            st.plotly_chart(fig9,theme="streamlit", use_container_width=True)

            st.write("Qualification Top5 Keywords")
            y1 = custom_kw_extractor.extract_keywords(top_jobs_3.qualification[0])
            fig10 = go.Figure([go.Bar(
            x=[t[0] for t in y1],
            y=[t[1] for t in y1],
            text= [t[0] for t in y1])])
            fig10.update_xaxes(visible=False)
            st.plotly_chart(fig10,theme="streamlit", use_container_width=True)    

            z1 = custom_kw_extractor.extract_keywords(top_jobs_3.description[0])
            st.write("Description Top5 Keywords")
            fig11 = go.Figure([go.Bar(
            x=[t[0] for t in z1],
            y=[t[1] for t in z1],
            text= [t[0] for t in z1])])
            fig11.update_xaxes(visible=False)
            st.plotly_chart(fig11,theme="streamlit", use_container_width=True)        

        def plot15():
            x1 = custom_kw_extractor.extract_keywords(top_jobs_3.responsibility[1])
            st.write("Responsibility Top5 Keywords")
            fig9 = go.Figure([go.Bar(
            x=[t[0] for t in x1],
            y=[t[1] for t in x1],
            text= [t[0] for t in x1])])
            fig9.update_xaxes(visible=False)
            st.plotly_chart(fig9,theme="streamlit", use_container_width=True)
            st.divider()
            st.write("Qualification Top5 Keywords")
            y1 = custom_kw_extractor.extract_keywords(top_jobs_3.qualification[1])
            fig10 = go.Figure([go.Bar(
            x=[t[0] for t in y1],
            y=[t[1] for t in y1],
            text= [t[0] for t in y1])])
            fig10.update_xaxes(visible=False)
            st.plotly_chart(fig10,theme="streamlit", use_container_width=True)    
            st.divider()
            z1 = custom_kw_extractor.extract_keywords(top_jobs_3.description[1])
            st.write("Description Top5 Keywords")
            fig11 = go.Figure([go.Bar(
            x=[t[0] for t in z1],
            y=[t[1] for t in z1],
            text= [t[0] for t in z1])])
            fig11.update_xaxes(visible=False)
            st.plotly_chart(fig11,theme="streamlit", use_container_width=True)     

        def plot16():
            x1 = custom_kw_extractor.extract_keywords(top_jobs_3.responsibility[2])
            st.write("Responsibility Top5 Keywords")
            fig9 = go.Figure([go.Bar(
            x=[t[0] for t in x1],
            y=[t[1] for t in x1],
            text= [t[0] for t in x1])])
            fig9.update_xaxes(visible=False)
            st.plotly_chart(fig9,theme="streamlit", use_container_width=True)

            st.write("Qualification Top5 Keywords")
            y1 = custom_kw_extractor.extract_keywords(top_jobs_3.qualification[2])
            fig10 = go.Figure([go.Bar(
            x=[t[0] for t in y1],
            y=[t[1] for t in y1],
            text= [t[0] for t in y1])])
            fig10.update_xaxes(visible=False)
            st.plotly_chart(fig10,theme="streamlit", use_container_width=True)    

            z1 = custom_kw_extractor.extract_keywords(top_jobs_3.description[2])
            st.write("Description Top5 Keywords")
            fig11 = go.Figure([go.Bar(
            x=[t[0] for t in z1],
            y=[t[1] for t in z1],
            text= [t[0] for t in z1])])
            fig11.update_xaxes(visible=False)
            st.plotly_chart(fig11,theme="streamlit", use_container_width=True)     




        with st.container():

            tab1, tab2, tab3 = st.tabs(["Candidate Job 1", "Candidate Job 2", "Candidate Job 3"])

            with tab1:
                st.write("Postion:",top_jobs_3.position[0])
                st.write("Company:", top_jobs_3.company_name[0])
                st.write("Minimum Salary:",top_jobs_3.min_salary[0])
                st.write("Maximum Salary:", top_jobs_3.max_salary[0])
                st.divider()

                try:
                    plot14()
                except:
                    pass

            if top_jobs_3.shape[0] < 2:
                pass
            else:
                with tab2:
                    st.write("Postion:",top_jobs_3.position[1])
                    st.write("Company:", top_jobs_3.company_name[1])
                    st.write("Minimum Salary:",top_jobs_3.min_salary[1])
                    st.write("Maximum Salary:", top_jobs_3.max_salary[1])
                    st.divider()                
                    plot15()

                if top_jobs_3.shape[0] < 3:
                    pass
                else:
                    with tab3:
                        st.write("Postion:",top_jobs_3.position[2])
                        st.write("Company:", top_jobs_3.company_name[2])
                        st.write("Minimum Salary:",top_jobs_3.min_salary[2])
                        st.write("Maximum Salary:", top_jobs_3.max_salary[2])
                        st.divider()                
                        plot16()


def Conclusion():
    col1, col2 = st.columns([5,1])
    col1.title("Conclusion: What we learned")
    with col2:
        st_lottie(l5, key = "five",height = 60,width = 100)

    st.write("From the analysis in the previous pages, we have learned that data is 'what you make out of it' and there is no aboslute path. From the inital analysis of comparing DC against the remaining cities of the United States, we found that DC may be a good place for Georgeotwn DSAN graduates to stay after graduation for its high salary in domains of general Data Science or Data Analytics. From this, we have conlcuded our initial assumption that DC, is in fact a Data Science welcoming environment with abundant opportunities. However, as mentioned before, the store that data tells us is what we make of it. From the experience, we do know that DC is generally a hub for government realted occupations. With that being said, the roles that are often available in DC are government related, hindering international students to participate in the progress of applying. Thus, we can conclude that depending on who the user of this platform is, it is very important to understand this context before anything else.")
    st.write("Next, as we looked at two different scenarios of choosing the location of DSAN students' post graduation job locations, we saw that 'perception' changes everything. Staerting from the importance of location, we found California to be one of the price locations as the state has abundance of opportunities for advanced Data Science materials. However, when lookikng at the data from the persepctive of focus in domain knowledge, it was evident that NY or even VA were among the top choices where Data Scientists would be copmensated fairly. In that sense, we can gather from the understandings that it is what the user focuses on, no ground truth in data as well.")
    st.write("And as a final closing remark, I wanted to say thank you, as this mini-project actually has been a lot of fun. Having to use Streamlit for the first time in a long time to this extent, brought reminded me of how, when showing work, it is not just the content that matters, but also the presentations. Hope whoever views this enjoys the content, and finds it useful. Hopefully in the future, with more data, we will be able to dive deeper into the realms of each cities, and garner more data analysis out of it.")
    st.write("Thank you for a wonderful semester")
    st.write("Sincerely,")
    st.write("Anonymous (wink wink)")

    with st.sidebar:
        st_lottie(l6, key = "six",height = 600,width = 300)

def Resources():
    st.write('https://www.youtube.com/watch?v=gr_KyGfO_eU')
    st.write('https://docs.streamlit.io/library/get-started/multipage-apps/create-a-multipage-app')
    st.write('https://python-charts.com/correlation/bubble-chart-plotly/')
    st.write('https://www.youtube.com/watch?v=TXSOitGoINE')
    st.write('https://lottiefiles.com/143550-checklist')
    st.write('https://www.youtube.com/watch?v=3f-j-PZ5N8A')

page_names_to_funcs = {
    "Hey! How are You?": intro,
    "District of Columbia Analysis": DC,
    "What kind of a Person Are You?": suggestions,
    "Saying Goodbyes": Conclusion,
    "How did I learn to do all this?": Resources
}

demo_name = st.sidebar.selectbox("Please Select a Page", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
        
        