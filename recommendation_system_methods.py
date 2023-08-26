

import pandas as pd
from scipy.spatial.distance import cosine
def getRecoItemBased(data):
    data = data[['user_id', 'cms_course_id']]
    data["Quantity"] = 1
    dataWide = data.pivot_table(index="user_id", columns="cms_course_id", values="Quantity")
    dataWide.fillna(0, inplace=True)
    
    data_ib = dataWide.copy()
    data_ib = data_ib.reset_index()
    data_ib = data_ib.drop(columns=["user_id"])
    data_ibs = pd.DataFrame(columns=data_ib.columns, index=data_ib.columns)
    for i in range(0,len(data_ibs.columns)) :
        # Loop through the columns for each column
        for j in range(0,len(data_ibs.columns)) :
            # Fill in placeholder with cosine similarities
            data_ibs.iloc[i,j] = 1-cosine(data_ib.iloc[:,i],data_ib.iloc[:,j])
    data_neighbours = pd.DataFrame(index=data_ibs.columns,columns=range(1,4))
 
    # Loop through our similarity dataframe and fill in neighbouring item names
    for i in range(0,len(data_ibs.columns)):
        data_neighbours.iloc[i,:3] = data_ibs.iloc[0:,i].sort_values(ascending=False)[:3].index
    data_neighbours = pd.DataFrame(index=data_ibs.columns,columns=range(1,11))
 
    # Loop through our similarity dataframe and fill in neighbouring item names
    for i in range(0,len(data_ibs.columns)):
        data_neighbours.iloc[i,:10] = data_ibs.iloc[0:,i].sort_values(ascending=False)[:10].index

    return data_neighbours


import mysql.connector
import pandas as pd


def getScore(history, similarities):
    return sum(history*similarities)/sum(similarities)

def getRecoUserBased(user, pwd, host, dbName):

    config = {
        'user': user,
        'password': pwd,
        'host': host,
        'database': dbName,
    }

    cnx = mysql.connector.connect(**config)
    query = "SELECT * FROM reco_course_users"
    cursor = cnx.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    data = pd.DataFrame(results, columns=cursor.column_names)

    data = data[['user_id', 'cms_course_id']]
    data["Quantity"] = 1
    dataWide = data.pivot_table(index="user_id", columns="cms_course_id", values="Quantity")
    dataWide.fillna(0, inplace=True)
    
    data_ib = dataWide.copy()
    data_ib = data_ib.reset_index()
    data_ib = data_ib.drop(columns=["user_id"])
    data_ibs = pd.DataFrame(index=data_ib.columns,
                        columns=data_ib.columns)

    data_sims1 = dataWide.reset_index()
    data_sims = pd.DataFrame(index=data_sims1.index,columns=data_sims1.columns)
    data_sims.iloc[:,:1] = data_sims1.iloc[:,:1]
    
    data_neighbours = getRecoItemBased(data)
    
    #Need to run this for only 500 users. Might be slow beyond that. 
    #Subset it to 500 users before running this
    for i in range(0,len(data_sims.index)):
        for j in range(1,len(data_sims.columns)):
            user = data_sims.index[i]
            product = data_sims.columns[j]

            if data_sims1.iloc[i].iloc[j] == 1:
                data_sims.iloc[i].iloc[j] = 0
            else:
                product_top_names = data_neighbours.loc[product][1:10]
                product_top_sims = data_ibs.loc[product].sort_values(ascending=False)[1:10]
                user_purchases = data_ib.loc[user,product_top_names]

                #print (i)
                #print (j)

                data_sims.iloc[i].iloc[j] = getScore(user_purchases,product_top_sims)                
    data_recommend = pd.DataFrame(index=data_sims.index, columns=['Person','1','2','3','4','5','6'])
    data_recommend.iloc[0:,0] = data_sims.iloc[:,0]
    
    for i in range(0,len(data_sims.index)):
        data_recommend.iloc[i,1:] = data_sims.iloc[i,:].sort_values(ascending=False).iloc[1:7,].index.transpose()
    return data_recommend






