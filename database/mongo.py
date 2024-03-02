from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

# MONGO_HOST = 'localhost'  # for Local MongoDB connection

MONGO_HOST = 'mongodb-svc'
MONGO_PORT = 27017
MONGO_DB = 'quiz_database'


client = MongoClient(f'mongodb://{MONGO_HOST}:{MONGO_PORT}/')

db = client[MONGO_DB]

questions_collection = db['questions']

# Clear existing data
questions_collection.delete_many({})

# Provided quiz data
question_data = [
  {
    "question": "The Apostle Paul's first letter in the New Testament is to the Galatians.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  },
  {
    "question": "King Ahab's wife was Jezebel.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "In the Bible, the 'Book of Wisdom' is found in both Catholic and Protestant Bibles.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  },
  {
    "question": "The first person to be resurrected by Jesus was Lazarus.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  },
  {
    "question": "Solomon wrote all the Proverbs in the Book of Proverbs.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  },
  {
    "question": "Moses and Elijah appeared during the Transfiguration of Jesus.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The phrase 'God helps those who help themselves' is found in the Bible.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  },
  {
    "question": "The book of Esther in the Bible does not mention God.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The longest verse in the Bible is in the book of Esther.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  },
  {
    "question": "The Apostle John saw a vision of the New Jerusalem coming down out of heaven in Revelation.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "There were 13 tribes of Israel.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The last words of Jesus on the cross were 'It is finished'.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The prophet Jeremiah was thrown into a lion's den.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  },
  {
    "question": "Rahab, mentioned in the Book of Joshua, was a carpenter.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  },
  {
    "question": "The only book in the Bible that doesn't mention the word 'God' is the Song of Solomon.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  },
  {
    "question": "Paul's first missionary journey was to Cyprus.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "Joseph was the youngest son of Jacob.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  },
  {
    "question": "There are four Gospels in the New Testament.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The last judge of Israel was Samuel.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "Jesus was baptized in the River Jordan by John.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "Melchizedek was a king and priest during the time of Abraham.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The book of Hezekiah is in the Old Testament.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  },
  {
    "question": "Paul's second missionary journey started in Antioch.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The Bible mentions the names of the two thieves crucified with Jesus.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  },
  {
    "question": "Naomi is Ruth's daughter-in-law.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The book of Lamentations was written by Jeremiah.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "Methuselah is the oldest person recorded in the Bible.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "Ehud was a left-handed judge.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The book of Acts has 28 chapters.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "Jephthah made a vow that led to the sacrifice of his daughter.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "Peter's original name was Simon.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "Rebekah was Isaac's cousin.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The first plague in Egypt was turning water into blood.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The Apostle Thomas is also known as 'Doubting Thomas'.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "Elisha succeeded Elijah as prophet.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The 'Hall of Faith' is found in the book of Hebrews.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The Apostle Paul was born in Tarsus.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The first Christian martyr was Stephen.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "Jesus' Sermon on the Mount is found in the Gospel of Mark.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  },
  {
    "question": "The oldest man in the Bible is Enoch.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  },
  {
    "question": "Jesus taught the Lord's Prayer during the Sermon on the Mount.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "Paul and Barnabas had a disagreement over John Mark.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The name 'Immanuel' means 'God with us'.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The Holy Spirit descended on Jesus like a dove.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The book of Isaiah contains 66 chapters.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The 'fruit of the Spirit' is listed in the book of Galatians.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The Ark of the Covenant is housed in the First Temple in Jerusalem.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  },
  {
    "question": "Timothy was a companion of the Apostle Paul.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "Jesus' transfiguration was witnessed by Peter, James, and John.",
    "correct_answer": "True",
    "incorrect_answers": ["False"]
  },
  {
    "question": "The Apostle Paul was shipwrecked three times during his missionary journeys.",
    "correct_answer": "False",
    "incorrect_answers": ["True"]
  }
]

# Transform data to the appropriate structure for MongoDB
formatted_questions = []
for question in question_data:
    formatted_question = {
        "question": question["question"],
        "correct_answer": question["correct_answer"],
        "incorrect_answers": question["incorrect_answers"]
    }
    formatted_questions.append(formatted_question)

# Insert the questions
questions_collection.insert_many(formatted_questions)
print("Questions inserted successfully.")

# Collection for users
users_collection = db['users']

# Example user data (you might want to remove this in production)
example_user = {
    "email": "test@example.com",
    "password": generate_password_hash("test1234")  # Hash the password
}

# Insert the example user
users_collection.insert_one(example_user)
print("Example user inserted successfully.")

admin_user = {
    "email": "ogochukwu.ozotta@gmail.com",
    "password": generate_password_hash("Admin123"),
    "is_admin": True
}

users_collection.insert_one(admin_user)
print("Example admin inserted successfully.")


# Collection for scores
scores_collection = db['scores']

# Example score data (linked to the user by email)
example_score = {
    "email": "test@example.com",
    "score": 100
}

# Insert the example score
scores_collection.insert_one(example_score)
print("Example score inserted successfully.")