# # ------------------------------
# # Original Imports + Neo4j Setup
# # ------------------------------
# import aiml
# import os
# from glob import glob
# from flask import Flask, render_template, request
#
# import nltk
# from nltk.corpus import wordnet as wn
# from textblob import TextBlob
# import spacy
#
# # ADD: Neo4j imports
# from neo4j import GraphDatabase
#
# # ADD: Prolog imports
# from pyswip import Prolog
#
# # ------------------------------
# # Neo4j Connection
# # ------------------------------
# neo4j_uri = "bolt://localhost:7687"
# neo4j_user = "neo4j"
# neo4j_password = "12345678"
#
# driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
#
# # ------------------------------
# # Prolog Setup
# # ------------------------------
# prolog = Prolog()
# prolog.consult("ml_knowledge_base.pl")  # Load your Prolog knowledge base
#
# # ------------------------------
# # Helper Functions for Neo4j Queries
# # ------------------------------
# def get_ml_info(name: str) -> str:
#     query = """
#     MATCH (n {name: $name})
#     RETURN n
#     """
#     with driver.session() as session:
#         result = session.run(query, name=name)
#         record = result.single()
#         if record and record["n"]:
#             node = record["n"]
#             description = node.get("description", "")
#             return f"Info about {name}: {description}" if description else f"Found node {name}, but no description."
#         else:
#             return f"Sorry, I couldn't find info about '{name}' in Neo4j."
#
# # ------------------------------
# # Helper Functions for Prolog Queries
# # ------------------------------
# def query_prolog_for_category(algorithm: str) -> str:
#     query = f'find_category("{algorithm}", CategoryName)'
#     results = list(prolog.query(query))
#     if results:
#         return f"Category of {algorithm}: {results[0]['CategoryName']}"
#     return f"No category found for {algorithm}."
#
# def query_prolog_for_description(algorithm: str) -> str:
#     query = f'find_description("{algorithm}", Description)'
#     results = list(prolog.query(query))
#     if results:
#         return f"Description of {algorithm}: {results[0]['Description']}"
#     return f"No description found for {algorithm}."
#
# def query_prolog_for_related(algorithm: str) -> str:
#     query = f'find_related("{algorithm}", Related)'
#     results = list(prolog.query(query))
#     if results:
#         related = [result['Related'] for result in results]
#         return f"Algorithms related to {algorithm}: {', '.join(related)}"
#     return f"No related algorithms found for {algorithm}."
#
# # ------------------------------
# # NLTK WordNet Definition
# # ------------------------------
# def getdefinition(word):
#     s = wn.synset(word+'.n.01')
#     return s.definition()
#
# # ------------------------------
# # Sentiment, Analysis, Etc.
# # ------------------------------
# def detect_sentiment(sentence):
#     blob = TextBlob(sentence)
#     polarity = blob.sentiment.polarity
#     if polarity > 0:
#         return 'Positive'
#     elif polarity < 0:
#         return 'Negative'
#     else:
#         return 'Neutral'
#
# nlp = spacy.load("en_core_web_sm")
#
# def analyze_sentence_type(sentence):
#     doc = nlp(sentence)
#     if sentence.endswith('?'):
#         return 'Interrogative'
#     elif sentence.endswith('!'):
#         return 'Exclamatory'
#     elif doc[0].tag_ == 'VB' or doc[0].dep_ == 'ROOT':
#         return 'Imperative'
#     else:
#         return 'Declarative'
#
# # ------------------------------
# # AIML Kernel + Flask Setup
# # ------------------------------
# bot = aiml.Kernel()
# app = Flask(__name__)
#
# aiml_folder = r'C:\Users\farha\Desktop\aiml project\New folder\aiml project\aiml project\aiml'
# sentence_history = {}
#
# def load_aiml_files(folder_path):
#     try:
#         aiml_files = glob(os.path.join(folder_path, '*.aiml'))
#         if not aiml_files:
#             raise FileNotFoundError(f"No AIML files found in folder: {folder_path}")
#         for file in aiml_files:
#             bot.learn(file)
#         print(f"Loaded {len(aiml_files)} AIML files from {folder_path}")
#     except Exception as e:
#         print(f"Error loading AIML files: {e}")
#
# # ------------------------------
# # Main Chatbot Logic
# # ------------------------------
# def get_response(user_input):
#     """
#     Generate a response from the bot based on user input.
#     """
#     try:
#         # Analyze sentence structure and sentiment
#         sentence_type = analyze_sentence_type(user_input)
#         sentiment = detect_sentiment(user_input)
#         print(f"Sentence Type: {sentence_type}")
#         print(f"Sentiment: {sentiment}")
#
#         # Store the analysis in sentence history
#         sentence_history['last_sentence_type'] = sentence_type
#         sentence_history['last_sentence_sentiment'] = sentiment
#
#         # --------------------------------------
#         # 1. Handle Prolog Queries (Highest Priority)
#         # --------------------------------------
#         if user_input.lower().startswith("category of"):
#             algorithm = user_input.split("category of", 1)[1].strip()
#             return query_prolog_for_category(algorithm)
#
#         if user_input.lower().startswith("description of"):
#             algorithm = user_input.split("description of", 1)[1].strip()
#             return query_prolog_for_description(algorithm)
#
#         if user_input.lower().startswith("related to"):
#             algorithm = user_input.split("related to", 1)[1].strip()
#             return query_prolog_for_related(algorithm)
#
#         # --------------------------------------
#         # 2. Handle Neo4j Queries
#         # --------------------------------------
#         if user_input.lower().startswith("info about"):
#             name = user_input.split("info about", 1)[1].strip()
#             return get_ml_info(name)
#
#         # --------------------------------------
#         # 3. Handle NLTK WordNet Queries
#         # --------------------------------------
#         if user_input.lower().startswith("define"):
#             word = user_input.split("define", 1)[1].strip()
#             try:
#                 definition = getdefinition(word)
#                 return f"Definition of {word}: {definition}"
#             except Exception:
#                 return f"Sorry, I couldn't find a definition for '{word}'."
#
#         # --------------------------------------
#         # 4. AIML Response (Fallback)
#         # --------------------------------------
#         bot_response = bot.respond(user_input)
#         if bot_response and bot_response != "Sorry, I didn't understand that.":
#             word = bot.getPredicate("word")
#             if word:
#                 definition = getdefinition(word)
#                 print("Definition: ", definition)
#                 bot.setPredicate("definition", definition)
#                 bot_response = bot.respond(user_input)
#             return bot_response
#
#         # --------------------------------------
#         # 5. Sentiment Fallback (If No Match in Prolog, Neo4j, or AIML)
#         # --------------------------------------
#         if sentiment == 'Positive':
#             return "That's great! I'm happy to hear that!"
#         elif sentiment == 'Negative':
#             return "I'm sorry to hear that. How can I help?"
#         else:
#             return "Can you please elaborate? I want to help!"
#
#     except Exception as e:
#         print(f"Error generating response: {e}")
#         return "Something went wrong while processing your request."
#
# # ------------------------------
# # Flask Routes
# # ------------------------------
# @app.route("/")
# def home():
#     return render_template("home.html")
#
# @app.route("/get")
# def get_bot_response():
#     query = request.args.get('msg', '').strip()
#     if not query:
#         return "Please provide a message."
#
#     if query.lower() == "what was my previous sentence type?":
#         sentence_type = sentence_history.get('last_sentence_type', "No previous sentence type found.")
#         sentiment = sentence_history.get('last_sentence_sentiment', "No previous sentence sentiment found.")
#         return f"Your previous sentence was {sentence_type} with {sentiment} sentiment."
#
#     response = get_response(query)
#     return str(response)
#
# # ------------------------------
# # Run Flask
# # ------------------------------
# if __name__ == "__main__":
#     try:
#         load_aiml_files(aiml_folder)
#         print("AIML files loaded successfully.")
#         app.run(debug=True, host='0.0.0.0', port=5000)
#     except Exception as e:
#         print(f"Error: {e}")


# ------------------------------
# Original Imports + Neo4j Setup
# ------------------------------
import aiml
import os
from glob import glob
from flask import Flask, render_template, request

import nltk
from nltk.corpus import wordnet as wn
from textblob import TextBlob
import spacy

# ADD: Neo4j imports
from neo4j import GraphDatabase

# ADD: Prolog imports
from pyswip import Prolog

# ------------------------------
# Neo4j Connection
# ------------------------------
neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "12345678"

driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

# ------------------------------
# Prolog Setup
# ------------------------------
prolog = Prolog()
# prolog.consult(r"ml_knowledge_base.pl")
# prolog_file_path = r"C:\Users\farha\Desktop\aiml project\New folder\aiml project\aiml project\ml_knowledge_base.pl"Update with correct path
prolog_file_path = "ml_knowledge_base.pl"

if not os.path.exists(prolog_file_path):
    raise FileNotFoundError(f"Prolog file not found at {prolog_file_path}")

# Load the Prolog knowledge base
try:
    prolog.consult(prolog_file_path)
    print(f"Successfully loaded Prolog file: {prolog_file_path}")
except Exception as e:
    print(f"Failed to load Prolog file: {e}")
    raise
# ------------------------------
# Helper Functions for Neo4j Queries
# ------------------------------
def get_ml_info(name: str) -> str:
    query = """
    MATCH (n {name: $name})
    RETURN n
    """
    with driver.session() as session:
        result = session.run(query, name=name)
        record = result.single()
        if record and record["n"]:
            node = record["n"]
            description = node.get("description", "")
            return f"Info about {name}: {description}" if description else f"Found node {name}, but no description."
        else:
            return f"Sorry, I couldn't find info about '{name}' in Neo4j."

# ------------------------------
# Helper Functions for Prolog Queries
# ------------------------------
def query_prolog_for_category(algorithm: str) -> str:
    query = f'find_category("{algorithm}", CategoryName)'
    print(f"Executing Prolog Query: {query}")  # Debug print
    results = list(prolog.query(query))
    if results:
        return f"Category of {algorithm}: {results[0]['CategoryName']}"
    return f"No category found for {algorithm}."

def query_prolog_for_description(algorithm: str) -> str:
    query = f'find_description("{algorithm}", Description)'
    print(f"Executing Prolog Query: {query}")  # Debug print
    results = list(prolog.query(query))
    if results:
        return f"Description of {algorithm}: {results[0]['Description']}"
    return f"No description found for {algorithm}."

def query_prolog_for_related(algorithm: str) -> str:
    query = f'find_related("{algorithm}", Related)'
    print(f"Executing Prolog Query: {query}")  # Debug print
    results = list(prolog.query(query))
    if results:
        related = [result['Related'] for result in results]
        return f"Algorithms related to {algorithm}: {', '.join(related)}"
    return f"No related algorithms found for {algorithm}."

# Query Prolog for advantages of an algorithm
def query_prolog_for_advantage(algorithm: str) -> str:
    query = f'find_advantage("{algorithm}", Advantage)'
    print(f"Executing Prolog Query: {query}")  # Debug print
    results = list(prolog.query(query))
    if results:
        return f"Advantage of {algorithm}: {results[0]['Advantage']}"
    return f"No advantages found for {algorithm}."

# Query Prolog for disadvantages of an algorithm
def query_prolog_for_disadvantage(algorithm: str) -> str:
    query = f'find_disadvantage("{algorithm}", Disadvantage)'
    print(f"Executing Prolog Query: {query}")  # Debug print
    results = list(prolog.query(query))
    if results:
        return f"Disadvantage of {algorithm}: {results[0]['Disadvantage']}"
    return f"No disadvantages found for {algorithm}."

# Query Prolog for application areas of an algorithm
def query_prolog_for_application(algorithm: str) -> str:
    query = f'find_application("{algorithm}", Application)'
    print(f"Executing Prolog Query: {query}")  # Debug print
    results = list(prolog.query(query))
    if results:
        return f"Application of {algorithm}: {results[0]['Application']}"
    return f"No application areas found for {algorithm}."


# ------------------------------
# NLTK WordNet Definition
# ------------------------------
def getdefinition(word):
    s = wn.synset(word+'.n.01')
    return s.definition()

# ------------------------------
# Sentiment, Analysis, Etc.
# ------------------------------
def detect_sentiment(sentence):
    blob = TextBlob(sentence)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

nlp = spacy.load("en_core_web_sm")

def analyze_sentence_type(sentence):
    doc = nlp(sentence)
    if sentence.endswith('?'):
        return 'Interrogative'
    elif sentence.endswith('!'):
        return 'Exclamatory'
    elif doc[0].tag_ == 'VB' or doc[0].dep_ == 'ROOT':
        return 'Imperative'
    else:
        return 'Declarative'

# ------------------------------
# AIML Kernel + Flask Setup
# ------------------------------
bot = aiml.Kernel()
app = Flask(__name__)

aiml_folder = r'aiml'
sentence_history = {}

def load_aiml_files(folder_path):
    try:
        aiml_files = glob(os.path.join(folder_path, '*.aiml'))
        if not aiml_files:
            raise FileNotFoundError(f"No AIML files found in folder: {folder_path}")
        for file in aiml_files:
            bot.learn(file)
        print(f"Loaded {len(aiml_files)} AIML files from {folder_path}")
    except Exception as e:
        print(f"Error loading AIML files: {e}")

# ------------------------------
# Main Chatbot Logic
# ------------------------------
def get_response(user_input):
    try:
        # Analyze sentence structure and sentiment
        sentence_type = analyze_sentence_type(user_input)
        sentiment = detect_sentiment(user_input)
        print(f"Sentence Type: {sentence_type}")
        print(f"Sentiment: {sentiment}")

        # Store the analysis in sentence history
        sentence_history['last_sentence_type'] = sentence_type
        sentence_history['last_sentence_sentiment'] = sentiment

        # --------------------------------------
        # 1. Handle Prolog Queries (Highest Priority)
        # --------------------------------------
        if user_input.lower().startswith("category of"):
            algorithm = user_input.split("category of", 1)[1].strip()
            return query_prolog_for_category(algorithm)

        if user_input.lower().startswith("description of"):
            algorithm = user_input.split("description of", 1)[1].strip()
            return query_prolog_for_description(algorithm)



        if user_input.lower().startswith("advantage of"):
            algorithm = user_input.split("advantage of", 1)[1].strip()
            return query_prolog_for_advantage(algorithm)

        if user_input.lower().startswith("disadvantage of"):
            algorithm = user_input.split("disadvantage of", 1)[1].strip()
            return query_prolog_for_disadvantage(algorithm)

        if user_input.lower().startswith("application of"):
            algorithm = user_input.split("application of", 1)[1].strip()
            return query_prolog_for_application(algorithm)

        # --------------------------------------
        # 2. Handle Neo4j Queries
        # --------------------------------------
        if user_input.lower().startswith("info about"):
            name = user_input.split("info about", 1)[1].strip()
            return get_ml_info(name)

        # --------------------------------------
        # 3. Handle NLTK WordNet Queries
        # --------------------------------------
        if user_input.lower().startswith("define"):
            word = user_input.split("define", 1)[1].strip()
            try:
                definition = getdefinition(word)
                return f"Definition of {word}: {definition}"
            except Exception:
                return f"Sorry, I couldn't find a definition for '{word}'."

        # --------------------------------------
        # 4. AIML Response (Fallback)
        # --------------------------------------
        bot_response = bot.respond(user_input)
        if bot_response and bot_response != "Sorry, I didn't understand that.":
            word = bot.getPredicate("word")
            if word:
                definition = getdefinition(word)
                print("Definition: ", definition)
                bot.setPredicate("definition", definition)
                bot_response = bot.respond(user_input)
            return bot_response

        # --------------------------------------
        # 5. Sentiment Fallback (If No Match in Prolog, Neo4j, or AIML)
        # --------------------------------------
        if sentiment == 'Positive':
            return "That's great! I'm happy to hear that!"
        elif sentiment == 'Negative':
            return "I'm sorry to hear that. How can I help?"
        else:
            return "Can you please elaborate? I want to help!"

    except Exception as e:
        print(f"Error generating response: {e}")
        return "Something went wrong while processing your request."

# ------------------------------
# Flask Routes
# ------------------------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    query = request.args.get('msg', '').strip()
    if not query:
        return "Please provide a message."

    if query.lower() == "what was my previous sentence type?":
        sentence_type = sentence_history.get('last_sentence_type', "No previous sentence type found.")
        sentiment = sentence_history.get('last_sentence_sentiment', "No previous sentence sentiment found.")
        return f"Your previous sentence was {sentence_type} with {sentiment} sentiment."

    response = get_response(query)
    return str(response)

# ------------------------------
# Run Flask
# ------------------------------
if __name__ == "__main__":
    try:
        load_aiml_files(aiml_folder)
        print("AIML files loaded successfully.")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error: {e}")
