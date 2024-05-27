# Recipe Book

Recipe Book is an application built with Python Flask, SQLite, jQuery, and Ajax.

## About the Project

Recipe Book is an app designed to help users manage their collection of recipes, providing a convenient way to store, organize, and access your recipes.

## Features

**Recipe Management**: Add, edit, and delete recipes. Each recipe includes details such as ingredients, directions, serving size, and meal category.

### Endpoints:

- **Home**: Main page where all recipes and form for adding recipes are displayed (`http://localhost:5000`)
- **Add**: Route that is using the POST method and form to add recipe to the database (`http://localhost:5000/add`)
- **Delete**: Used by button in table with recipes on the home page, deletes recipe from the database with the DELETE method (example for recipe with id 1: `http://localhost:5000/delete/1`)
- **Edit**: Second page with fields for data to update accessed through button table from the home page, all fields need to be filled (`http://localhost:5000/edit`)
- **Update**: Route used by the edit page to update the database using the PUT method (example for recipe with id 1: `http://localhost:5000/update/1`)
- **Get**: Route to get all recipes or singular recipe by id, used by home page to fill table (to get all: `http://localhost:5000/get` and example for recipe with id 1 `http://localhost:5000/get/1`)

## Prerequisites

- Python 3.10.5 or above
- Git 2.38.0 or above

## Installation

For Windows:

1. Clone the repository:

   ```bash
   git clone https://github.com/dubravkaD/flask-app.git
   ```

2. Navigate to the project directory:

   ```bash
   cd flask-app
   ```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   ```bash
   .\venv\Scripts\activate
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Start the Flask server:

   ```bash
   python app.py
   ```

## Usage

1. Start the Flask server:

   ```bash
   python app.py
   ```

2. Open a web browser and go to `http://localhost:5000` to access the Recipe Book.
