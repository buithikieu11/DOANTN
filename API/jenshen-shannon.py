from scipy.spatial.distance import jensenshannon
from numpy import asarray
import pymongo
import settings
client = pymongo.MongoClient(settings.MONGODB_SETTINGS["host"])
db = client[settings.MONGODB_SETTINGS["db"]]
mongo_col = db[settings.MONGODB_SETTINGS["collection"]]
# define distributions
# p = asarray([0.10, 0.40, 0.50])
# q = asarray([0.80, 0.15, 0.05])
p = asarray([0.8, 0.1, 0.1])
q = asarray([0.9, 0.05, 0.05])
# calculate JS(P || Q)
js_pq = jensenshannon(p, q, base=2)
print('JS(P || Q) Distance: %.3f' % js_pq)
# calculate JS(Q || P)
js_qp = jensenshannon(q, p, base=2)
print('JS(Q || P) Distance: %.3f' % js_qp)
most_sim_ids = [1,2,3,4,5]
posts = list(mongo_col.find({"idrs": {"$in": most_sim_ids}}))
print(posts)