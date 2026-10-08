from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from movies_data import movies_data
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

app = Flask(__name__)
CORS(app)

# Convert movies data to DataFrame
df = pd.DataFrame(movies_data)

# Create TF-IDF vectorizer for content-based filtering
def create_tfidf_matrix():
    # Combine description, keywords, genre, and director for better recommendations
    df['combined_features'] = df['description'] + ' ' + \
                              df['genre'] + ' ' + \
                              df['director'] + ' ' + \
                              ' '.join(df['keywords'].apply(lambda x: ' '.join(x)))
    
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])
    return tfidf_matrix

tfidf_matrix = create_tfidf_matrix()
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Create indices mapping
indices = pd.Series(df.index, index=df['title']).drop_duplicates()

def get_recommendations(movie_title, num_recommendations=5):
    """Get content-based recommendations for a movie"""
    try:
        idx = indices[movie_title]
        source_movie = df.iloc[idx].to_dict()
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:num_recommendations+1]  # Skip the movie itself
        movie_indices = [i[0] for i in sim_scores]
        
        recommendations = df.iloc[movie_indices].to_dict('records')
        
        # Add similarity scores and reasoning
        for i, rec in enumerate(recommendations):
            rec['similarity_score'] = round(sim_scores[i][1] * 100, 1)
            rec['why_recommended'] = generate_recommendation_reason(source_movie, rec, rec['similarity_score'])
        
        return recommendations
    except KeyError:
        return []

def generate_recommendation_reason(source_movie, recommended_movie, similarity_score=None):
    """Generate a detailed reason why a movie was recommended"""
    reasons = []
    
    # Check for same genre
    if source_movie['genre'] == recommended_movie['genre']:
        reasons.append(f"Same {source_movie['genre']} genre")
    
    # Check for same director
    if source_movie['director'] == recommended_movie['director']:
        reasons.append(f"Directed by {recommended_movie['director']}")
    
    # Check for shared keywords
    shared_keywords = set(source_movie['keywords']) & set(recommended_movie['keywords'])
    if shared_keywords:
        reasons.append(f"Similar themes: {', '.join(list(shared_keywords)[:2])}")
    
    # Check for shared cast
    shared_cast = set(source_movie['cast']) & set(recommended_movie['cast'])
    if shared_cast:
        reasons.append(f"Features {list(shared_cast)[0]}")
    
    # Check rating similarity
    rating_diff = abs(source_movie['rating'] - recommended_movie['rating'])
    if rating_diff < 0.5:
        reasons.append("Similar quality rating")
    
    # Add similarity score if provided
    if similarity_score and similarity_score > 80:
        reasons.append(f"High similarity match ({similarity_score}%)")
    
    # Check year proximity
    year_diff = abs(source_movie['year'] - recommended_movie['year'])
    if year_diff <= 5:
        reasons.append(f"Released in similar era ({recommended_movie['year']})")
    
    # Default reason if no specific matches
    if not reasons:
        reasons.append("Similar narrative style and tone")
    
    return ". ".join(reasons[:2]) + "."

def get_genre_recommendations(genre, num_recommendations=6):
    """Get recommendations filtered by genre with enhanced reasoning"""
    genre_movies = df[df['genre'] == genre].to_dict('records')
    
    # Sort by rating and return top recommendations
    genre_movies.sort(key=lambda x: x['rating'], reverse=True)
    
    for movie in genre_movies[:num_recommendations]:
        reasons = []
        reasons.append(f"Top-rated {genre} movie with a {movie['rating']}/10 rating")
        reasons.append(f"Directed by {movie['director']}")
        reasons.append(f"Features {movie['cast'][0]}")
        movie['why_recommended'] = ". ".join(reasons[:2]) + "."
    
    return genre_movies[:num_recommendations]

def get_personalized_recommendations(num_recommendations=6):
    """Get personalized recommendations based on multiple factors"""
    # Get top-rated movies across all genres
    top_movies = df.sort_values('rating', ascending=False).to_dict('records')
    
    # Add personalized reasons with more detail
    for movie in top_movies[:num_recommendations]:
        reasons = []
        reasons.append(f"Highly rated ({movie['rating']}/10) {movie['genre']} film")
        reasons.append(f"Masterpiece by {movie['director']}")
        reasons.append(f"Features acclaimed cast including {movie['cast'][0]}")
        if movie['rating'] >= 8.5:
            reasons.append("Critically acclaimed with universal praise")
        movie['why_recommended'] = ". ".join(reasons[:2]) + "."
    
    return top_movies[:num_recommendations]

def search_movies(query):
    """Search movies by title, genre, keywords, director, or cast"""
    query = query.lower()
    results = []
    
    for movie in movies_data:
        # Search in title
        if query in movie['title'].lower():
            results.append(movie)
            continue
        
        # Search in genre
        if query in movie['genre'].lower():
            results.append(movie)
            continue
        
        # Search in keywords
        if any(query in keyword.lower() for keyword in movie['keywords']):
            results.append(movie)
            continue
        
        # Search in director
        if query in movie['director'].lower():
            results.append(movie)
            continue
        
        # Search in cast
        if any(query in cast_member.lower() for cast_member in movie['cast']):
            results.append(movie)
            continue
    
    return results

def get_trending_movies(num_recommendations=6):
    """Get trending movies based on rating and recency"""
    # Sort by rating and year (more recent with high rating)
    trending = df.sort_values(['rating', 'year'], ascending=[False, False]).to_dict('records')
    
    for movie in trending[:num_recommendations]:
        movie['why_recommended'] = f"Trending {movie['genre']} hit with {movie['rating']}/10 rating from {movie['year']}"
    
    return trending[:num_recommendations]

def get_director_recommendations(director, num_recommendations=6):
    """Get recommendations by director"""
    director_movies = df[df['director'] == director].to_dict('records')
    
    for movie in director_movies[:num_recommendations]:
        movie['why_recommended'] = f"Another masterpiece by {director}"
    
    return director_movies[:num_recommendations]

def get_cast_recommendations(actor, num_recommendations=6):
    """Get recommendations featuring a specific actor"""
    cast_movies = [movie for movie in movies_data if actor.lower() in [c.lower() for c in movie['cast']]]
    
    for movie in cast_movies[:num_recommendations]:
        movie['why_recommended'] = f"Features {actor} in a compelling role"
    
    return cast_movies[:num_recommendations]

def get_random_discovery(num_recommendations=6):
    """Get random movie recommendations for discovery"""
    random_movies = random.sample(movies_data, min(num_recommendations, len(movies_data)))
    
    for movie in random_movies:
        movie['why_recommended'] = f"Discover this {movie['genre']} gem: {movie['title']}"
    
    return random_movies

def get_decade_recommendations(decade, num_recommendations=6):
    """Get recommendations from a specific decade"""
    decade_start = (decade // 10) * 10
    decade_end = decade_start + 9
    decade_movies = df[(df['year'] >= decade_start) & (df['year'] <= decade_end)].to_dict('records')
    
    decade_movies.sort(key=lambda x: x['rating'], reverse=True)
    
    for movie in decade_movies[:num_recommendations]:
        movie['why_recommended'] = f"Best of the {decade_start}s: {movie['rating']}/10 rated {movie['genre']}"
    
    return decade_movies[:num_recommendations]

def get_hybrid_recommendations(genre=None, min_rating=7.0, num_recommendations=6):
    """Get hybrid recommendations combining genre and rating filters"""
    filtered_movies = df.copy()
    
    if genre:
        filtered_movies = filtered_movies[filtered_movies['genre'] == genre]
    
    filtered_movies = filtered_movies[filtered_movies['rating'] >= min_rating]
    hybrid_movies = filtered_movies.sort_values('rating', ascending=False).to_dict('records')
    
    for movie in hybrid_movies[:num_recommendations]:
        reasons = []
        if genre:
            reasons.append(f"Top {genre} choice")
        reasons.append(f"Highly rated ({movie['rating']}/10)")
        movie['why_recommended'] = ". ".join(reasons)
    
    return hybrid_movies[:num_recommendations]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/movies')
def get_all_movies():
    return jsonify(movies_data)

@app.route('/api/recommendations/<movie_title>')
def recommendations(movie_title):
    num = request.args.get('num', 5, type=int)
    recommendations = get_recommendations(movie_title, num)
    return jsonify(recommendations)

@app.route('/api/genre/<genre>')
def genre_recommendations(genre):
    num = request.args.get('num', 6, type=int)
    recommendations = get_genre_recommendations(genre, num)
    return jsonify(recommendations)

@app.route('/api/personalized')
def personalized_recommendations():
    num = request.args.get('num', 6, type=int)
    recommendations = get_personalized_recommendations(num)
    return jsonify(recommendations)

@app.route('/api/search')
def search():
    query = request.args.get('q', '')
    results = search_movies(query)
    return jsonify(results)

@app.route('/api/genres')
def get_genres():
    genres = sorted(list(set(movie['genre'] for movie in movies_data)))
    return jsonify(genres)

@app.route('/api/trending')
def trending_recommendations():
    num = request.args.get('num', 6, type=int)
    recommendations = get_trending_movies(num)
    return jsonify(recommendations)

@app.route('/api/director/<director>')
def director_recommendations(director):
    num = request.args.get('num', 6, type=int)
    recommendations = get_director_recommendations(director, num)
    return jsonify(recommendations)

@app.route('/api/cast/<actor>')
def cast_recommendations(actor):
    num = request.args.get('num', 6, type=int)
    recommendations = get_cast_recommendations(actor, num)
    return jsonify(recommendations)

@app.route('/api/discover')
def random_discovery():
    num = request.args.get('num', 6, type=int)
    recommendations = get_random_discovery(num)
    return jsonify(recommendations)

@app.route('/api/decade/<int:decade>')
def decade_recommendations(decade):
    num = request.args.get('num', 6, type=int)
    recommendations = get_decade_recommendations(decade, num)
    return jsonify(recommendations)

@app.route('/api/hybrid')
def hybrid_recommendations():
    genre = request.args.get('genre')
    min_rating = request.args.get('min_rating', 7.0, type=float)
    num = request.args.get('num', 6, type=int)
    recommendations = get_hybrid_recommendations(genre, min_rating, num)
    return jsonify(recommendations)

@app.route('/api/movie/<int:movie_id>')
def get_movie_by_id(movie_id):
    movie = next((m for m in movies_data if m['id'] == movie_id), None)
    if movie:
        return jsonify(movie)
    return jsonify({"error": "Movie not found"}), 404

@app.route('/api/rating')
def rating_range_recommendations():
    min_rating = request.args.get('min', 0.0, type=float)
    max_rating = request.args.get('max', 10.0, type=float)
    num = request.args.get('num', 6, type=int)
    
    rating_movies = df[(df['rating'] >= min_rating) & (df['rating'] <= max_rating)]
    rating_movies = rating_movies.sort_values('rating', ascending=False).to_dict('records')
    
    for movie in rating_movies[:num]:
        movie['why_recommended'] = f"Rated {movie['rating']}/10 - fits your preference range"
    
    return jsonify(rating_movies[:num])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
