# Parfum App - Fragrance Discovery Platform

A web application for fragrance enthusiasts to explore and discover perfumes, their notes, and detailed information. This platform is inspired by Fragrantica and aims to provide a comprehensive database of perfumes with their characteristics.

## Website Overview

### Home Page

- Featured perfumes carousel
- Latest releases section
- Popular perfumes grid
- Quick search functionality
- Featured brands showcase

### Browse Perfumes Page

- Complete perfume catalog
- Advanced filtering options:
  - By brand
  - By release year
  - By fragrance family
  - By notes
  - By gender
- Sorting options (popularity, release date, rating)
- Grid/List view toggle
- Pagination

### Perfume Detail Page

- Hero section with perfume image and basic info
- Perfume information:
  - Brand
  - Release year
  - Perfumer
  - Gender
  - Price range
- Scent profile visualization:
  - Top notes
  - Heart notes
  - Base notes
- Interactive note pyramid
- User ratings and reviews section
- Similar perfumes recommendations
- Where to buy section

### Brand Pages

- Brand overview and history
- Complete brand catalog
- Bestsellers section
- Latest releases
- Brand statistics

### User Features

- Personal profile
- Perfume collection management
- Wishlist
- Review and rating system
- Personal notes and comments
- Perfume comparison tool

### Search and Discovery

- Global search functionality
- Advanced search with multiple criteria
- Note-based perfume finder
- "Perfumes like this" recommendations
- Trending perfumes section

## Features (MVP)

### Frontend (Nuxt.js)

- Modern and responsive user interface
- Browse perfumes with pagination and search functionality
- Detailed perfume pages showing:
  - Basic information (name, brand, year of release)
  - Fragrance notes (top, middle, base)
  - Perfumer information
  - User ratings and reviews
  - Similar perfumes
- Search and filter functionality
- User authentication

### Backend (Python)

- RESTful API built with FastAPI
- PostgreSQL database for storing perfume and user data
- Authentication and authorization
- Data models for:
  - Perfumes
  - Fragrance notes
  - Brands
  - User reviews
  - User profiles

## Tech Stack

### Frontend

- Nuxt.js 3
- Vue.js 3
- TailwindCSS
- Pinia (State Management)

### Backend

- Python 3.9+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (Database migrations)
- JWT Authentication

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL
- Docker (optional)

### Backend Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your database credentials and other configurations
```

4. Run migrations:

```bash
alembic upgrade head
```

5. Start the backend server:

```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Set up environment variables:

```bash
cp .env.example .env
```

3. Run the development server:

```bash
npm run dev
```

## API Documentation

Once the backend server is running, you can access the API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database Schema

### Main Entities:

- Perfumes
- Brands
- Notes
- Users
- Reviews
- Ratings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
