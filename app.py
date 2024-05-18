from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


# Creats table recipes if not exist in db
# Has fields id, title, category, servings, ingredients, directions
def create_table(connection):
    cursor = connection.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS recipes 
        (
            id INTEGER PRIMARY KEY, 
            title varchar(255) NOT NULL, 
            category varchar(255) CHECK (category IN ('lunch','snack','dessert','dinner','breakfast')), 
            servings INTEGER NOT NULL, 
            ingredients varchar(255) NOT NULL, 
            directions varchar(255) NOT NULL
        );
    """
    cursor.execute(query)
    connection.commit()
    cursor.close()


# Shows main page -> index
# Uses http method GET
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# Adds new recipe to table recipes
# Uses http method POST
@app.route("/add", methods=["POST"])
def add():
    pass


# Gets all recipes from table recipes
# Uses http method GET
@app.route("/get", methods=["GET"])
def get():
    with sqlite3.connect("recipe-book.db") as conn:
        create_table(conn)
        cursor = conn.cursor()
        query = "SELECT * FROM recipes;"
        cursor.execute(query)
        recipes = cursor.fetchall()
        cursor.close()
        return jsonify({"recipes": recipes})


# Gets recipe by id from table recipes
# Uses http method GET
@app.route("/get/<int:id>", methods=["GET"])
def get_recipe(id):
    pass


# Updates recipe from table recipes
# Uses http method PUT
@app.route("/update/<int:id>", methods=["PUT"])
def update(id):
    pass


# Deletes recipe by id from table recipes
# Uses http method DELETE
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
