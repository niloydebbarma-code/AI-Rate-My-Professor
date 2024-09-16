from flask import Flask, request, jsonify, render_template
import pinecone
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

# Initialize Flask app
app = Flask(__name__)

# Initialize Pinecone
pinecone.init(api_key='your_pinecone_api_key')
index = pinecone.Index('professor-index')

# Home route to serve HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Route for querying professor data
@app.route('/query', methods=['GET'])
def query_professor():
    query = request.args.get('query')
    results = index.query(query)
    return jsonify(results)

# Route for submitting professor page links and scraping data
@app.route('/submit', methods=['POST'])
def submit_link():
    url = request.form['url']
    data = scrape_professor_data(url)
    index.upsert(data)
    return jsonify({'status': 'success'})

# Route for advanced search
@app.route('/search', methods=['GET'])
def search_professors():
    criteria = request.args.to_dict()
    results = index.query(criteria)
    return jsonify(results)

# Route for sentiment analysis
@app.route('/sentiment', methods=['POST'])
def analyze_review():
    review = request.form['review']
    sentiment = analyze_sentiment(review)
    return jsonify({'sentiment': sentiment})

# Function to scrape professor data
def scrape_professor_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Example: Extract professor name and ratings (customize based on actual structure)
    professor_data = {
        'name': soup.find('h1').text,
        'rating': soup.find('div', class_='rating').text
    }
    return professor_data

# Function for sentiment analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

if __name__ == '__main__':
    app.run(debug=True)
