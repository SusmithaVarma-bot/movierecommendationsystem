# 🎬 CineVerse - AI Movie Recommendation System

A modern, AI-powered movie recommendation system with a stunning cinematic dark UI. Built with Flask, Python, and machine learning for intelligent content-based filtering.

![CineVerse](https://img.shields.io/badge/CineVerse-AI%20Powered-purple)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🎨 Unique Modern UI
- **Cinematic Dark Theme**: Premium dark interface with glassmorphism effects
- **Animated Background**: Subtle floating particles and gradient animations
- **Responsive Design**: Fully optimized for mobile, tablet, and desktop
- **Smooth Transitions**: Elegant hover effects and card animations
- **Modern Typography**: Clean fonts with professional hierarchy

### 🤖 AI-Powered Recommendations
- **Content-Based Filtering**: TF-IDF vectorization for intelligent matching
- **Multiple Recommendation Types**:
  - Similar movie recommendations
  - Genre-based recommendations
  - Personalized top-rated picks
  - Director-based recommendations
  - Cast-based recommendations
  - Decade-based recommendations
  - Rating range filtering
  - Random discovery for exploration
  - Hybrid recommendations (genre + rating)

### 🎯 Interactive Features
- **Smart Search**: Search by title, genre, keywords, director, or cast
- **Genre Filtering**: Quick genre buttons (Comedy, Thriller, Horror, Romance, Action, Sci-Fi)
- **Movie Cards**: Stylish cards with poster, title, genre, rating, and description
- **"Why This Movie?"**: Detailed explanations for each recommendation
- **Favorite/Watchlist**: Save movies to your personal watchlist (localStorage)
- **Modal Details**: Click any movie for detailed information
- **Get Similar Movies**: Instant recommendations from any movie modal

### 🚀 API Endpoints

#### Core Endpoints
- `GET /` - Main UI page
- `GET /api/movies` - Get all movies
- `GET /api/movie/<id>` - Get specific movie by ID
- `GET /api/genres` - Get all available genres

#### Recommendation Endpoints
- `GET /api/recommendations/<movie_title>` - Get similar movies
- `GET /api/genre/<genre>` - Get genre-based recommendations
- `GET /api/personalized` - Get personalized recommendations
- `GET /api/trending` - Get trending movies
- `GET /api/director/<director>` - Get movies by director
- `GET /api/cast/<actor>` - Get movies by actor
- `GET /api/discover` - Get random discovery picks
- `GET /api/decade/<decade>` - Get movies from a specific decade
- `GET /api/hybrid` - Get hybrid recommendations (genre + rating)
- `GET /api/rating` - Get movies by rating range

#### Search Endpoints
- `GET /api/search?q=<query>` - Search movies

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd movierecommendationsystem
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
movierecommendationsystem/
├── app.py                      # Flask backend with recommendation logic
├── movies_data.py              # Movie dataset (30 diverse movies)
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── templates/
│   └── index.html             # Main HTML frontend
└── static/
    ├── css/
    │   └── style.css          # Cinematic dark theme styles
    └── js/
        └── script.js           # Interactive JavaScript
```

## 🎯 Recommendation Algorithm

The system uses **TF-IDF (Term Frequency-Inverse Document Frequency)** vectorization combined with **cosine similarity** for content-based filtering:

1. **Feature Extraction**: Combines movie description, genre, director, and keywords
2. **Vectorization**: Converts text features into numerical vectors using TF-IDF
3. **Similarity Calculation**: Computes cosine similarity between movies
4. **Ranking**: Sorts by similarity score and returns top recommendations
5. **Reasoning**: Generates personalized explanations based on shared attributes

### Recommendation Factors
- Genre matching
- Director similarity
- Shared keywords/themes
- Cast overlap
- Rating proximity
- Release year proximity
- Overall similarity score

## 🎨 UI Features

### Navigation
- Fixed glassmorphism navbar
- Smooth scroll to sections
- Mobile-responsive hamburger menu
- Active state indicators

### Hero Section
- Large cinematic search bar
- Animated background particles
- Gradient text effects
- Instant search results

### Movie Cards
- Glassmorphism card design
- Hover lift animations
- Poster scaling effects
- Favorite/heart button
- Quick metadata display

### Modal
- Detailed movie information
- Cast and director details
- "Why recommended" explanation
- "Get Similar Movies" button
- Smooth open/close animations

### Genre Buttons
- Icon-based genre selection
- Hover gradient effects
- Active state styling
- Instant filtering

## 🔧 Configuration

### Adding More Movies
Edit `movies_data.py` and add movies in the following format:

```python
{
    "id": 31,
    "title": "Movie Title",
    "genre": "Genre",
    "rating": 8.5,
    "year": 2024,
    "description": "Movie description...",
    "poster": "Poster URL",
    "director": "Director Name",
    "cast": ["Actor 1", "Actor 2", "Actor 3"],
    "keywords": ["keyword1", "keyword2", "keyword3"]
}
```

### Customizing Colors
Edit `static/css/style.css` and modify the CSS variables:

```css
:root {
    --primary-dark: #0a0a0f;
    --accent-gold: #ffd700;
    --accent-purple: #8b5cf6;
    --accent-blue: #3b82f6;
    /* ... more variables */
}
```

## 📊 Dataset

The system includes 30 diverse movies across 6 genres:
- **Sci-Fi**: Inception, Interstellar, Arrival, Blade Runner 2049, The Matrix, Alien
- **Action**: The Dark Knight, Pulp Fiction, Mad Max: Fury Road, John Wick, Fight Club, Die Hard
- **Horror**: The Conjuring, Get Out, A Quiet Place, Hereditary, The Exorcist
- **Romance**: The Notebook, La La Land, Titanic, Pride and Prejudice, Casablanca
- **Comedy**: Superbad, The Hangover, The Grand Budapest Hotel, Step Brothers
- **Thriller**: Parasite, Knives Out, Gone Girl

## 🌐 Technologies Used

### Backend
- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning (TF-IDF, cosine similarity)

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript (ES6+)**: Interactive functionality
- **Google Fonts**: Playfair Display & Inter

## 🚀 Future Enhancements

- [ ] User authentication and profiles
- [ ] Collaborative filtering (user-based recommendations)
- [ ] Movie ratings and reviews
- [ ] Watchlist synchronization with backend
- [ ] Movie trailers integration
- [ ] External API integration (TMDB, OMDB)
- [ ] Dark/light theme toggle
- [ ] Advanced filtering options
- [ ] Recommendation history
- [ ] Social sharing features

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📧 Support

For questions or issues, please open an issue on the repository.

---

**Built with ❤️ using Python, Flask, and modern web technologies**

**CineVerse - Your AI Movie Companion** 🎬
