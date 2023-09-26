import os
import pymongo


class AramData:
    data = []
    champions_list = []

    def fetch_mongo_data(self):
        db = pymongo.MongoClient(os.getenv("MONGO_URL"))
        collection = db.aramid.champions_data
        results = collection.find(
            {},
            {
                "_id": 0,
                "rank": 1,
                "name": 1,
                "tier": 1,
                "winrate": 1,
                "pickrate": 1,
                "matches": 1,
            },
        ).sort("rank", 1)
        for result in results:
            self.data.append(result)
            self.champions_list.append(result["name"].lower())
        db.close()

    def get_top_champions(self, amount: int):
        top_champions = []
        for champion in self.data[:amount]:
            tmp_champion = {}
            tmp_champion["name"] = champion.get("name")
            tmp_champion["winrate"] = champion.get("winrate")
            tmp_champion["matches"] = champion.get("matches")
            top_champions.append(tmp_champion)
        return top_champions
