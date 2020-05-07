import pandas as pd
from services import firestore_services

fs = firestore_services.FireStoreServices("newspector-backend-firebase-adminsdk-ws3xc-bd1c31a298.json")
data = pd.read_csv("data_to_use.csv")
# new_data = data[:1800].reset_index(drop=True)
# old_data = data[1800:].reset_index(drop=True)

for i, tweet in data.iterrows():
    print("Adding", str(i+1))
    fs.add_tweet(tweet.to_dict())

# old_data.to_csv("data_to_use.csv")
# new_data.to_csv("new_data.csv")