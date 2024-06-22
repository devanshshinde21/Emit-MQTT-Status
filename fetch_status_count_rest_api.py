from emit_status_mqtt import mongodb_name, collection_name
import pandas as pd
from fastapi import FastAPI
import uvicorn

app = FastAPI()

collection_data = mongodb_name[collection_name].find()


@app.get("/endpoint/{start_time}/{end_time}")
async def read_item(start_time: str, end_time: str):
    try:
        if start_time and end_time:
            df = pd.DataFrame([i for i in collection_data])
            filter_df = df[(df.start_time >= start_time) & (df.end_time <= end_time)]
            fetched_data = filter_df['status'].value_counts().to_dict()
            response = {"Fetched Mongo Data": [{"Status": key, "Count": val} for key, val in fetched_data.items()]}
            return response
    except Exception as e:
        print(e)
        return {"Error": "Something went wrong while fetching data!."}
