import os
import pymongo


class AramData:
    data = []

    def fetch_mongo_data(self):
        db = pymongo.MongoClient(os.getenv("MONGO_URL"))
        collection = db.aramid.champions_data
        results = collection.find(
            {}, {"_id": 0, "name": 1, "winrate": 1, "matches": 1}
        ).sort("rank", 1)
        for result in results:
            self.data.append(result)
        db.close()

    def get_top_champions(self, amount: int):
        champions = self.data[:amount]
        return champions
