import pymongo

client = pymongo.MongoClient("Put your own construction string")
db = client['database']

profile_collection = db.profile
recruiter_post_collection = db.recruiter_post
signup_collection = db.signup
community_collection = db.community
cybersecurity_collection = db.cybersecurity
machine_learning_collection = db.machine_learning
python_collection = db.python
webdev_collection = db.webdev
java_collection = db.java
qna_collection = db.qna
