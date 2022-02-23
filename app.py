from flask import Flask, jsonify, request
import pandas as pd
from datetime import datetime
from flasgger import Swagger
from flasgger import swag_from

app=Flask(__name__)
swagger = Swagger(app)
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "Flasgger",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ]}
#Merger fucntion for static SKU file and dynamic input
def read_and_filter():
    df=pd.DataFrame(pd.read_csv("Transaction Record.csv", dtype=str)) #read the Transaction record file
    df_sku=pd.DataFrame(pd.read_csv("SKU Record.csv",dtype=str)) #read the static SKU details file
    df_all=pd.merge(df,df_sku,how="left",left_on="sku_id",right_on="sku_id") #Merging SKU static and Transaction input

    return df_all

##Two different functions below if we need to see the totals (SKU,price, etc), irrespective of 'last n days' 

#Adds a new column for time delta(for today and transaction date) also filter's based on last n days
def delta_column_add(df_all,last_n_days):
    today=datetime.today()
    delta_list=[]
    for x in df_all["transaction_datetime"]:
        datetime_object = datetime.strptime(x, '%d/%m/%Y') #converting to datetime
        delta_days=str(today.date()-datetime_object.date()) #calculating the delta
        delta_days=delta_days.split(",")[0]#reforming to take delta number
        delta_days=delta_days.replace(" days","")
        delta_list.append(int(delta_days))#appending to list to add to dataframe
    delta_list=pd.Series(delta_list)
    df_all["delta_days"]=delta_list

    df_all=df_all[df_all["delta_days"]<=int(last_n_days)]
    
    return df_all

#Aggregates the total price for SKU Name/Category
def aggregation(df_all,sku_x): 
    print(df_all)
    #making unique list of all SKU Names/Category
    all_unique_sku=[]
    for x in df_all[sku_x]:
        if x not in all_unique_sku:
            all_unique_sku.append(x)
    
    #Iterating on unique SKU Name/Category to return
    sku_summary_list=[]
    for uq_sku in all_unique_sku:
        summary={}
        df_sum_temp=df_all[df_all[sku_x]==uq_sku]
        total_price_this_sku=0
        for x in df_sum_temp["sku_price"]:
            total_price_this_sku+=float(x)
        
        #Appending things
        summary[sku_x]=uq_sku
        summary["total_amount"]=total_price_this_sku
        sku_summary_list.append(summary)
    outer_summary={"summary":sku_summary_list}

    return(outer_summary)
     
#[End Point: 1]
@app.route("/transaction/<transaction_id>",methods=["GET"])
@swag_from('yml/transaction.yml')
def transactions(transaction_id):

    df_all=read_and_filter()
    
    df_all=df_all[df_all["transaction_id"]==transaction_id] #Filtering the requested trasaction id in dataframe
    df_all.reset_index(drop=True, inplace=True)
    return jsonify({
        "transaction_id":transaction_id,
        "sku_name":df_all["sku_name"][0],
        "sku_price":df_all["sku_price"][0],
        "transaction_datetime":df_all["transaction_datetime"][0]
         })

#[End Point: 2]
@app.route("/transaction-summary-bySKU/<last_n_days>", methods=["GET"])
@swag_from("yml/summary.yml")
def transaction_summary_name(last_n_days):

    df_all=read_and_filter()

    df_all=delta_column_add(df_all,last_n_days)

    return jsonify(aggregation(df_all,"sku_name"))


#[End Point: 3]
@app.route("/transaction-summary-bycategory/<last_n_days>", methods=["GET"])
@swag_from("yml/summary.yml")
def transaction_summary_category(last_n_days):

    df_all=read_and_filter()

    df_all=delta_column_add(df_all,last_n_days)

    return jsonify(aggregation(df_all,"sku_category"))



if __name__=="__main__":
    app.run(host="0.0.0.0")  