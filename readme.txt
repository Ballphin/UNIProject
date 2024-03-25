Name: Kanmin (Daniel) Sung
UID: 31322966 

How to start the program:

1. Enter the flasky directory  === Code --> (cd flasky)
2. Activate the virtual Environment === Code --> (.\flaskVM\Scripts\Activate.ps1)
3. run the Website === Code --> (flask run)

Overview
The UNI Social Network is a comprehensive web application designed to connect university students, faculty, and alumni. 
Built with Flask, this polished application facilitates user interactions through posts, comments, likes, and personal accounts. 
It serves as a platform for sharing ideas, events, and updates within the university community. This project aligns with the requirements set forth in the "Polished Flask App" 
assignment, demonstrating the application of HTML, CSS, Python-Flask, WTForms, and Flask-SQLAlchemy.

Features
User Authentication: Secure signup and login functionality, including password hashing and session management.
Post Creation and Viewing: Users can create posts and view a feed of posts made by others.
Comments and Likes: Posts can be liked and commented on, allowing for interactive discussions.

Profile Management: Users can view and update their profiles, enhancing the social aspect of the network.
Technical Requirements Fulfillment

HTML and CSS
Document Structure: The application uses HTML5 with proper document structure and semantic tags, such as <header>, <nav>, <main>, and <footer>.
CSS Validation: Stylesheets are used to enhance the UI, with attention to responsiveness and aesthetics. The CSS code validates without errors.

Python-Flask
Project Structure: The Flask app follows the recommended project structure, including separate modules for forms (forms.py), models (models.py), and routes (main.py).
Templates and Static Files: Jinja2 templates are used for rendering HTML, and static files (CSS, images) are managed according to Flask conventions.

WTForms
Form Handling: WTForms are utilized for handling user input in registration, login, post creation, and comments, with CSRF protection enabled.
Validation and Redirection: Forms include validation checks, and successful submissions redirect to prevent duplicate submissions on refresh.

Flask-SQLAlchemy
Database Structure: The app's database includes at least two tables with relationships:
User: Stores user information. Each user can author multiple posts and comments.
Post: Stores posts made by users. Each post can have multiple likes and comments, demonstrating the use of foreign keys.
Data Insertion: Users can insert data into the database through the registration form, post creation form, and comment submission.

Navigation and URLs
/: Homepage with login and signup options.
/login: Login page for existing users.
/register: Registration page for new users.
/main: Main feed displaying posts from all users.
/post/new: Page for creating a new post.
/logout: Logs out the current user.

Database Configuration
User Table: Stores username, email, and hashed password. Acts as a foreign key in the Post table.
Post Table: Stores post content, date, and author relationship. Linked to the User table via a foreign key.

Conclusion
The UNI Social Network is a fully-functional web application designed to foster community 
engagement within an academic setting. By meeting the outlined requirements, this project demonstrates 
a comprehensive understanding of web development principles using Flask and associated technologies.