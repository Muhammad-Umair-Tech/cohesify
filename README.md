# Cohesify

Cohesify is a social media web application that lets users share posts, connect with friends, and interact through likes and comments. It supports sorting, filtering, and searching across posts and people through a consistent, easy-to-use interface.

## Features

- **User Accounts** — Sign up and log in with a username and password.
- **Posts** — Upload images and videos with captions.
- **Likes & Comments** — Like/unlike posts and leave comments.
- **Undo/Redo** — Undo and redo like/unlike actions, and undo accidental post deletions (restores the post along with its likes and comments).
- **Friends** — Add or remove friends and view your friends list.
- **Search** — Search for people and posts.
- **Sorting & Filtering** — Sort posts by trend or recency, sort people alphabetically, and filter posts by media type (images/videos).
- **Profile Management** — Update your profile picture and manage your own posts.

## Tech Stack

| Layer      | Technology                     |
|------------|---------------------------------|
| Backend    | Python, Django                  |
| Frontend   | HTML, CSS, JavaScript           |
| Database   | SQLite (via Django ORM)         |

## Screens

- **Home** — View, sort, filter, like, and comment on posts from friends and other users.
- **Friends** — View your current friends and discover new people to add.
- **Profile** — Manage your profile picture, create new posts, and manage/delete your existing posts.
- **Search** — Search for people and posts by keyword.
- **Comments** — View and add comments on a specific post.

## Getting Started

### Prerequisites

- Python 3.x
- pip
- Django

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd cohesify
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

## Usage

1. Create an account or log in with existing credentials.
2. Go to your **Profile** to create a post by adding a caption and choosing a picture.
3. Browse the **Home** feed to like, comment on, sort, and filter posts.
4. Visit **Friends** to add or remove connections.
5. Use the **Search** bar to find specific people or posts.
6. If you accidentally delete a post or unlike something, use the **Undo** options to restore it.

## Author

**Muhammad Umair**
Department of Computer Science, University of Engineering and Technology, Lahore

## Supervisor

Ma'am Rabeeya Saleem — CSC200 Data Structures and Algorithms

## License

This project was developed for academic purposes as part of the CSC200 Data Structures and Algorithms course.
