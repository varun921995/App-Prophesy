import json

from flask import Flask, render_template, Blueprint
import pandas as pd
import numpy as np

sunburst = Blueprint('sunburst',__name__)

@sunburst.route("/sunburstpage")
def index():
    print("here")
    df = pd.read_csv('dataset/processed.csv')
    df = df[['App Name','Category','Installs','Type','Content Rating','Rating']]
    df['Content Rating'] = df['Content Rating'].str.lower()
    df['Content Rating'] = df['Content Rating'].str.replace(' ','')
    df['Category'] = df['Category'].str.lower()
    df['Category'] = df['Category'].str.replace('-', '')

    list5 = df['Content Rating'].tolist()
    list9 = df['Category'].tolist()
    list6 = df['Type'].tolist()
    print(list6[2])
    
    list7 =[]
    list8 = []
    list10 = []
    list11 = []
    list12 = []
    list13 = []
    list14 = []
    list15 = []
    list16 = []
    list17 = []
    list18 = []
    list19 = []
    
    #Forming data frame of content rating 
    le = len(list5)
    
    for i in range(le):
        
        if((list5[i] == 'everyone') and (list6[i] == 'Paid')):
            
            list7.append(list5[i])
            list10.append(list9[i])

        elif((list5[i] == 'teen') and (list6[i] == 'Paid')):
            print(2)
            list7.append(list5[i])
            list11.append(list9[i])
        elif((list5[i] == 'everyone10+') and (list6[i] == 'Paid')):
            print(3)
            list7.append(list5[i])
            list12.append(list9[i])
        elif((list5[i] == 'mature17+') and (list6[i] == 'Paid')):
             print(4)
             list7.append(list5[i])
             list13.append(list9[i])
        elif((list5[i] == 'adultsonly18+') and (list6[i] == 'Paid')):
             print(5)
             list7.append(list5[i])
        elif((list5[i] == 'unrated') and (list6[i] == 'Paid')):
             print(6)
             list7.append(list5[i])
    for j in range(le):
       
        if((list5[j] == 'everyone') and (list6[j] == 'Free')):
            list8.append(list5[j])
            list14.append(list9[j])
        elif((list5[j] == 'teen') and (list6[j] == 'Free')):
            list8.append(list5[j])
            list15.append(list9[j])
        elif((list5[j] == 'everyone10+') and (list6[j] == 'Free')):
            list8.append(list5[j])
            list16.append(list9[j])
        elif((list5[j] == 'mature17+') and (list6[j] == 'Free')):
            list8.append(list5[j])
            list17.append(list9[j])
        elif((list5[j] == 'adultsonly18+') and (list6[j] == 'Free')):
            list8.append(list5[j])
            list18.append(list9[j])
        elif((list5[j] == 'unrated') and (list6[j] == 'Free')):
            list8.append(list5[j])
            list19.append(list9[j])
    
    myset = set(list7)
    newlist1 = list(myset)

    myset1 = set(list8)
    newlist2 = list(myset1)

    myset2 = set(list10)
    newlist3 = list(myset2)

    myset3 = set(list11)
    newlist4 = list(myset3)

    myset4 = set(list12)
    newlist5 = list(myset4)

    myset5 = set(list13)
    newlist6 = list(myset5)

    myset6 = set(list14)
    newlist7 = list(myset6)

    myset7 = set(list15)
    newlist8 = list(myset7)

    myset8 = set(list16)
    newlist9 = list(myset8)

    myset9 = set(list17)
    newlist10 = list(myset9)

    myset10 = set(list18)
    newlist11 = list(myset10)

    myset11 = set(list19)
    newlist12 = list(myset11)

    #Dividing free apps and paid apps in different data frame 
    df2 = df[df['Type'] == 'Free']
    df3 = df[df['Type'] == 'Paid']
    df2 = df2.sort_values(by=['Rating'], ascending=False)
    df2['Rating'] = df2['Rating'].astype(float)
    df3 = df3.sort_values(by=['Rating'], ascending=False)
    df3['Rating'] = df3['Rating'].astype(float)

#Getting apps names based on content rating and category for free apps
    topAppsDict = dict()
    for i in df2['Content Rating'].unique():
        newDf1 = df2.loc[df2['Content Rating'] == i]
        for j in newDf1['Category'].unique():
            list20 = []
            newDf2 = newDf1.loc[newDf1['Category'] == j]
            listKey = i + "_"+j 
            newDf3 = newDf2[newDf2.Rating > 4.55]       
            list20.append(newDf3['App Name'].iloc[:3].values)#.tolist())
            topAppsDict[listKey] =list20[0:3]

#Getting apps namse based on content rating and category for paid apps 
    topAppsDict1 = dict()
    for i in df3['Content Rating'].unique():
        newDf1 = df3.loc[df3['Content Rating'] == i]
        for j in newDf1['Category'].unique():
            list500 = []
            newDf2 = newDf1.loc[newDf1['Category'] == j]
            listKey = i + "_"+j 
            newDf3 = newDf2[newDf2.Rating > 4.55]         
            list500.append(newDf3['App Name'].iloc[:3].values)
            topAppsDict1[listKey] =list500[0:3]
            
    newlist = list()
    list298 = list()
    list129 = list()
    flattened_list = list()
    for i in topAppsDict.keys():
        newlist.append(i)
    for k in newlist:
        list298.append(np.array(topAppsDict[k]).tolist())
    for i in range(0,124):
        list129.append(list298[i][0])
    flattened_list = [y for x in list129 for y in x]
    df_app = pd.DataFrame(flattened_list , columns = ['Apps'])

    newlist500 = list()
    list299 = list()
    list130 = list()
    flattened_list1 = list()
    for i in topAppsDict1.keys():
        newlist500.append(i)
    for k in newlist500:
        list299.append(np.array(topAppsDict1[k]).tolist())
    for i in range(0,57):
        list130.append(list299[i][0])
    flattened_list1 = [y for x in list130 for y in x]
    df_app1 = pd.DataFrame(flattened_list1 , columns = ['Apps'])

    #paid and free content rating data frames
    df_paid = pd.DataFrame(newlist1,columns = {'content'})
    df_free1 = pd.DataFrame(newlist2,columns = {'content'})
   #paid category dataframes
    df_pc1 = pd.DataFrame(newlist3,columns = {'category'})
    df_pc2 = pd.DataFrame(newlist4,columns = {'category'})
    df_pc3 = pd.DataFrame(newlist5,columns = {'category'})
    df_pc4 = pd.DataFrame(newlist6,columns = {'category'})
    #free category dataframes
    df_fc1 = pd.DataFrame(newlist7,columns = {'category'})
    df_fc2 = pd.DataFrame(newlist8,columns = {'category'})
    df_fc3 = pd.DataFrame(newlist9,columns = {'category'})
    df_fc4 = pd.DataFrame(newlist10,columns = {'category'})
    df_fc5 = pd.DataFrame(newlist11,columns = {'category'})
    df_fc6 = pd.DataFrame(newlist12,columns = {'category'})




    #converting dataframes to json objects
    chart_data1 = df_paid.to_dict(orient='records')
    chart_data1 = json.dumps(chart_data1, indent=2)
    data1 = {'chart_data1': chart_data1}
  
    chart_data2 = df_free1.to_dict(orient='records')
    chart_data2 = json.dumps(chart_data2, indent=2)
    data2 = {'chart_data2': chart_data2}
    #converting category dataframe into json
    chart_data3 =  df_pc1.to_dict(orient='records')
    chart_data3 = json.dumps(chart_data3, indent=2)
    data3 = {'chart_data3': chart_data3}

    chart_data4 =  df_pc2.to_dict(orient='records')
    chart_data4 = json.dumps(chart_data4, indent=2)
    data4 = {'chart_data4': chart_data4}

    chart_data5 =  df_pc3.to_dict(orient='records')
    chart_data5 = json.dumps(chart_data5, indent=2)
    data5 = {'chart_data5': chart_data5}

    chart_data6 =  df_pc4.to_dict(orient='records')
    chart_data6 = json.dumps(chart_data6, indent=2)
    data6 = {'chart_data6': chart_data6}

    chart_data7 =  df_fc1.to_dict(orient='records')
    chart_data7 = json.dumps(chart_data7, indent=2)
    data7 = {'chart_data7': chart_data7}

    chart_data8 =  df_fc2.to_dict(orient='records')
    chart_data8 = json.dumps(chart_data8, indent=2)
    data8 = {'chart_data8': chart_data8}

    chart_data9 =  df_fc3.to_dict(orient='records')
    chart_data9 = json.dumps(chart_data9, indent=2)
    data9 = {'chart_data9': chart_data9}

    chart_data10 =  df_fc4.to_dict(orient='records')
    chart_data10 = json.dumps(chart_data10, indent=2)
    data10 = {'chart_data10': chart_data10}

    chart_data11 =  df_fc5.to_dict(orient='records')
    chart_data11 = json.dumps(chart_data11, indent=2)
    data11 = {'chart_data11': chart_data11}

    chart_data12 =  df_fc6.to_dict(orient='records')
    chart_data12 = json.dumps(chart_data12, indent=2)
    data12 = {'chart_data12': chart_data12}
   # chart_data13= json.dumps(topAppsDict, indent=2)
   # data13 = {'chart_data13': chart_data13}
    chart_data13 =  df_app.to_dict(orient='records')
    chart_data13 = json.dumps(chart_data13, indent=2)
    data13 = {'chart_data13': chart_data13}

    chart_data14 =  df_app1.to_dict(orient='records')
    chart_data14 = json.dumps(chart_data14, indent=2)
    data14 = {'chart_data14': chart_data14}


    #data13 = {'topAppsDict':topAppsDict}
    #Forming dataframe of price 
    new_dict = df['Type'].value_counts()
    df5 = pd.DataFrame(list(new_dict.iteritems()),
                      columns=['price','count'])
    df5['percentage'] = (df5['count']/df5['count'].sum())*100
    chart_data = df5.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data,'chart_data1':chart_data1,'chart_data2':data2,'chart_data3':data3,'chart_data4':data4,
            'chart_data5':data5,'chart_data6':data6,'chart_data7':data7,'chart_data8':data8,'chart_data9':data9,'chart_data10':data10,
            'chart_data11':data11,'chart_data12':data12,'chart_data13':data13,'chart_data14':data14}

    return render_template("sunburst.html", data=data,data2 = topAppsDict)


# if __name__ == "__main__":
#     app.run(debug=True)

