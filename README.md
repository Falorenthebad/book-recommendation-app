# Book Recommendation App

A Django-based web application that allows users to search for books, select their favorite titles, and receive personalized book recommendations based on shared genres and ratings. Additionally, users can get a random high-rated book suggestion or view detailed information about any book in the database.

---

## Features

* **Home Page**: Welcome screen with navigation to all features.
* **Book Search**: Filter and sort books by title, author, rating, publication year, number of pages, and genres.
* **Favorite-based Recommendations**: Select three favorite books and receive the top 15 recommended titles based on genre similarity and rating.
* **Random Recommendation**: Get a random book suggestion with an average rating above 3.7.
* **Book Details**: View detailed information for any book, including title, authors, rating, ratings count, publication year, page count, and genres.

---

## Prerequisites

* Python 3.7 or higher
* pip (Python package installer)
* Django 4.x

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Falorenthebad/book-recommendation-app.git
   cd book-recommendation-app
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv env
   env\Scripts\activate    # for MacOs: source env/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create migrations**:

   ```bash
   python manage.py makemigrations
   ```

5. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

7. **Access the app**: Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## Configuration

* **Database**: By default uses `db.sqlite3`. To switch to another database, update `DATABASES` in `settings.py`.
* **Static Files**: Collected by Django’s `collectstatic`. Ensure `STATIC_ROOT` is set in production.
* **Settings**: Adjust `DEBUG`, `ALLOWED_HOSTS`, and other settings in `book_recommendation_website/settings.py`.

---

## Usage

* **Search**: Navigate to the "Book Search" page and use the filters to find books.
* **Recommendations**: Go to "Book Recommendations", type in three favorite books (autocomplete will help), and view recommendations.
* **Random Book**: Click "Surprise Me" on the home page for a random high-rated book.
* **Book Details**: Click any book title or image to view its detailed information.

---