![Python](https://img.shields.io/badge/Python-80%25-brightgreen.svg) ![Django](https://img.shields.io/badge/Django-3.x-brightgreen.svg) ![HTML](https://img.shields.io/badge/HTML-10%25-yellow.svg) ![CSS](https://img.shields.io/badge/CSS-5%25-blue.svg) ![JavaScript](https://img.shields.io/badge/JavaScript-5%25-lightgrey.svg) ![SQLite](https://img.shields.io/badge/SQLite-Default-lightgrey.svg) ![Linux](https://img.shields.io/badge/Linux-Host-lightgrey.svg) ![Contributors](https://img.shields.io/badge/contributors-1-orange.svg)

# Django Blog Management System

## Overview
This Django-based blog management app was built to solidify the concepts I learned from Dr. Charles Severance, affectionately known as "Dr. Chuck," whose teachings on Python and web development inspired me to dive deeper into backend frameworks. It allows users to create, read, update, and delete blog posts with secure user authentication, making it a practical tool for managing personal content.

## Features
- **User Authentication**: Sign up and log in to securely manage your blog posts.
- **CRUD Operations**: Effortlessly create, read, update, and delete posts.
- **Personalized Homepage**: After logging in, users land on a tailored homepage to manage their content, and also view the content of every user on the general homepage.
- **Responsive Design**: Enjoy a seamless experience across desktops, tablets, and phones.

## What I Learned
Thanks to Dr. Chuck’s guidance, I gained hands-on experience with:
- Building web applications using Django and Python.
- Implementing user authentication and database management.
- Structuring a project with models, views, and templates.
- Writing cleaner, more maintainable code through practice and iteration.

## Code Structure
- **Views**: Logic for handling HTTP requests and rendering pages.
- **Templates**: HTML files for the user interface.
- **URLs**: Routing configurations to connect URLs to views.
- **Models**: Database schemas for posts and users.
- **Forms**: Tools for validating and processing user input.

## Getting Started
1. Clone the repository:
```bash
git clone https://github.com/olugbeminiyi2000/Django-Blog-Management-System-DBMS-/
```
2. Install dependencies:
```bash
pip install -r requirements42.txt
pip install -r requirements4.txt
```
3. Run migrations:
```bash
python manange.py makemigrations
python manage.py migrate
```
4. Start the server:
```
python manage.py runserver
```
5. Visit `http://localhost:8000` in your browser.

## Future Improvements
- Adopt Django’s generic class-based views (e.g., `CreateView`, `ListView`) for cleaner code.
- Enhance security with features like password hashing (already included via Django) and CSRF protection.
- Modularize the codebase and add detailed documentation for scalability.
- Integrate a richer frontend with more JavaScript or a framework like React.

## Conclusion
This project is a testament to the foundational knowledge I gained from Dr. Chuck. While it meets its core goals, there’s room to grow—streamlining with class-based views and refining code organization are next steps to make it even more robust and maintainable.

6. 
7. Run migrations:
