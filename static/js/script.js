// API Base URL
const API_BASE = '/api';

// DOM Elements
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const searchResults = document.getElementById('searchResults');
const genreButtons = document.querySelectorAll('.genre-btn');
const genreRecommendations = document.getElementById('genreRecommendations');
const personalizedRecommendations = document.getElementById('personalizedRecommendations');
const allMovies = document.getElementById('allMovies');
const movieModal = document.getElementById('movieModal');
const modalClose = document.querySelector('.modal-close');
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-link');

// Favorites/Watchlist (stored in localStorage)
let favorites = JSON.parse(localStorage.getItem('movieFavorites')) || [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadPersonalizedRecommendations();
    loadAllMovies();
    setupEventListeners();
});

// Setup Event Listeners
function setupEventListeners() {
    // Search
    searchBtn.addEventListener('click', handleSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSearch();
    });

    // Genre Buttons
    genreButtons.forEach(btn => {
        btn.addEventListener('click', () => handleGenreClick(btn));
    });

    // Modal
    modalClose.addEventListener('click', closeModal);
    movieModal.addEventListener('click', (e) => {
        if (e.target === movieModal) closeModal();
    });

    // Navigation
    navToggle.addEventListener('click', toggleNav);
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.getAttribute('href');
            document.querySelector(target).scrollIntoView({ behavior: 'smooth' });
            
            // Update active state
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // Close mobile menu
            navMenu.classList.remove('active');
        });
    });

    // Scroll effect for navbar
    window.addEventListener('scroll', handleScroll);
}

// Handle Search
async function handleSearch() {
    const query = searchInput.value.trim();
    if (!query) return;

    showLoading(searchResults);
    
    try {
        const response = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}`);
        const movies = await response.json();
        
        if (movies.length > 0) {
            searchResults.innerHTML = '';
            searchResults.classList.remove('hidden');
            
            const grid = document.createElement('div');
            grid.className = 'movie-grid';
            
            movies.forEach(movie => {
                grid.appendChild(createMovieCard(movie));
            });
            
            searchResults.appendChild(grid);
        } else {
            searchResults.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No movies found. Try a different search term.</p>';
            searchResults.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Search error:', error);
        searchResults.innerHTML = '<p style="text-align: center; color: #ff6b6b;">Error searching movies. Please try again.</p>';
        searchResults.classList.remove('hidden');
    }
}

// Handle Genre Click
async function handleGenreClick(btn) {
    const genre = btn.dataset.genre;
    
    // Update active state
    genreButtons.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    // Show loading
    genreRecommendations.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
    genreRecommendations.classList.remove('hidden');
    
    try {
        const response = await fetch(`${API_BASE}/genre/${genre}`);
        const movies = await response.json();
        
        genreRecommendations.innerHTML = '';
        
        const grid = document.createElement('div');
        grid.className = 'movie-grid';
        
        movies.forEach(movie => {
            grid.appendChild(createMovieCard(movie));
        });
        
        genreRecommendations.appendChild(grid);
        
        // Scroll to recommendations
        genreRecommendations.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (error) {
        console.error('Genre error:', error);
        genreRecommendations.innerHTML = '<p style="text-align: center; color: #ff6b6b;">Error loading recommendations. Please try again.</p>';
    }
}

// Load Personalized Recommendations
async function loadPersonalizedRecommendations() {
    showLoading(personalizedRecommendations);
    
    try {
        const response = await fetch(`${API_BASE}/personalized`);
        const movies = await response.json();
        
        personalizedRecommendations.innerHTML = '';
        
        const grid = document.createElement('div');
        grid.className = 'movie-grid';
        
        movies.forEach(movie => {
            grid.appendChild(createMovieCard(movie));
        });
        
        personalizedRecommendations.appendChild(grid);
    } catch (error) {
        console.error('Personalized recommendations error:', error);
        personalizedRecommendations.innerHTML = '<p style="text-align: center; color: #ff6b6b;">Error loading recommendations. Please try again.</p>';
    }
}

// Load All Movies
async function loadAllMovies() {
    showLoading(allMovies);
    
    try {
        const response = await fetch(`${API_BASE}/movies`);
        const movies = await response.json();
        
        allMovies.innerHTML = '';
        
        const grid = document.createElement('div');
        grid.className = 'movie-grid';
        
        movies.forEach(movie => {
            grid.appendChild(createMovieCard(movie));
        });
        
        allMovies.appendChild(grid);
    } catch (error) {
        console.error('All movies error:', error);
        allMovies.innerHTML = '<p style="text-align: center; color: #ff6b6b;">Error loading movies. Please try again.</p>';
    }
}

// Create Movie Card
function createMovieCard(movie) {
    const card = document.createElement('div');
    card.className = 'movie-card';
    card.dataset.movieId = movie.id;
    
    const isFavorite = favorites.includes(movie.id);
    
    card.innerHTML = `
        <button class="favorite-btn ${isFavorite ? 'active' : ''}" data-movie-id="${movie.id}">
            ${isFavorite ? '❤️' : '🤍'}
        </button>
        <img src="${movie.poster}" alt="${movie.title}" class="movie-poster" onerror="this.src='https://via.placeholder.com/500x750?text=No+Poster'">
        <div class="movie-info">
            <h3 class="movie-title">${movie.title}</h3>
            <div class="movie-meta">
                <span class="movie-genre">${movie.genre}</span>
                <span class="movie-rating">
                    <span>⭐</span>
                    <span>${movie.rating}</span>
                </span>
            </div>
            <p class="movie-description">${movie.description}</p>
        </div>
    `;
    
    // Card click event
    card.addEventListener('click', (e) => {
        if (!e.target.classList.contains('favorite-btn')) {
            openModal(movie);
        }
    });
    
    // Favorite button event
    const favoriteBtn = card.querySelector('.favorite-btn');
    favoriteBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleFavorite(movie.id, favoriteBtn);
    });
    
    return card;
}

// Toggle Favorite
function toggleFavorite(movieId, btn) {
    const index = favorites.indexOf(movieId);
    
    if (index > -1) {
        favorites.splice(index, 1);
        btn.classList.remove('active');
        btn.textContent = '🤍';
    } else {
        favorites.push(movieId);
        btn.classList.add('active');
        btn.textContent = '❤️';
    }
    
    localStorage.setItem('movieFavorites', JSON.stringify(favorites));
}

// Open Modal
function openModal(movie) {
    document.getElementById('modalPoster').src = movie.poster;
    document.getElementById('modalPoster').onerror = function() {
        this.src = 'https://via.placeholder.com/500x750?text=No+Poster';
    };
    document.getElementById('modalTitle').textContent = movie.title;
    document.getElementById('modalGenre').textContent = movie.genre;
    document.getElementById('modalYear').textContent = movie.year;
    document.getElementById('modalRating').innerHTML = `⭐ ${movie.rating}`;
    document.getElementById('modalDescription').textContent = movie.description;
    document.getElementById('modalDirector').textContent = movie.director;
    document.getElementById('modalCast').textContent = movie.cast.join(', ');
    document.getElementById('modalWhy').textContent = movie.why_recommended || 'This movie matches your preferences based on genre, style, and similar themes.';
    
    // Setup "Get Similar Movies" button
    const recommendBtn = document.getElementById('getRecommendationsBtn');
    recommendBtn.onclick = async () => {
        await loadSimilarMovies(movie.title);
    };
    
    movieModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

// Close Modal
function closeModal() {
    movieModal.classList.add('hidden');
    document.body.style.overflow = '';
}

// Load Similar Movies
async function loadSimilarMovies(movieTitle) {
    closeModal();
    
    // Scroll to genre section and show loading
    genreRecommendations.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
    genreRecommendations.classList.remove('hidden');
    genreRecommendations.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    // Remove active state from genre buttons
    genreButtons.forEach(b => b.classList.remove('active'));
    
    try {
        const response = await fetch(`${API_BASE}/recommendations/${encodeURIComponent(movieTitle)}`);
        const movies = await response.json();
        
        genreRecommendations.innerHTML = '';
        
        if (movies.length > 0) {
            const grid = document.createElement('div');
            grid.className = 'movie-grid';
            
            movies.forEach(movie => {
                grid.appendChild(createMovieCard(movie));
            });
            
            genreRecommendations.appendChild(grid);
        } else {
            genreRecommendations.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No similar movies found.</p>';
        }
    } catch (error) {
        console.error('Similar movies error:', error);
        genreRecommendations.innerHTML = '<p style="text-align: center; color: #ff6b6b;">Error loading similar movies. Please try again.</p>';
    }
}

// Show Loading
function showLoading(container) {
    container.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
}

// Toggle Navigation
function toggleNav() {
    navMenu.classList.toggle('active');
}

// Handle Scroll
function handleScroll() {
    const navbar = document.querySelector('.navbar');
    
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(10, 10, 15, 0.95)';
        navbar.style.padding = '1rem 0';
    } else {
        navbar.style.background = 'rgba(10, 10, 15, 0.8)';
        navbar.style.padding = '1.5rem 0';
    }
    
    // Update active nav link based on scroll position
    const sections = document.querySelectorAll('section');
    const scrollPos = window.scrollY + 100;
    
    sections.forEach(section => {
        const top = section.offsetTop;
        const height = section.offsetHeight;
        const id = section.getAttribute('id');
        
        if (scrollPos >= top && scrollPos < top + height) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${id}`) {
                    link.classList.add('active');
                }
            });
        }
    });
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});
