from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# recipes = []


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
    recipes = get()
    # get type of recipes
    # print(type(recipes))
    # if recipes is tuples -> recipes[0].json is list and each element in list is dict
    recipes_res = recipes[0]
    recipes_list = recipes_res.json
    #
    # print()
    # [print(row) for row in recipes_list]
    # print()
    #
    # if recipes is type flask.wrappers.Response
    #
    # recipes_json = recipes.json
    # print(type(recipes_json))
    # [print(row) for row in recipes_json]
    return render_template("index.html", recipes=recipes_list)


# Adds new recipe to table recipes
# Uses http method POST
@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    category = request.form["category"]
    servings = request.form["servings"]
    ingredients = request.form["ingredients"]
    directions = request.form["directions"]
    recipe = (title, category, int(servings), ingredients, directions)
    with sqlite3.connect("recipe-book.db") as connection:
        create_table(connection)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO recipes (title,category,servings,ingredients,directions) VALUES(?,?,?,?,?)",
            recipe,
        )
        connection.commit()
        cursor.close()
        return jsonify({"message": "Successfully added recipe!"}), 201


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
        return (
            jsonify(
                [
                    dict(
                        zip(
                            [
                                "id",
                                "title",
                                "category",
                                "servings",
                                "ingredients",
                                "directions",
                            ],
                            row,
                        )
                    )
                    for row in recipes
                ]
            ),
            200,
        )
        # return recipes


# Gets recipe by id from table recipes
# Uses http method GET
@app.route("/get/<int:id>", methods=["GET"])
def get_recipe(id):
    with sqlite3.connect("recipe-book.db") as conn:
        create_table(conn)
        cursor = conn.cursor()
        query = f"SELECT * FROM recipes WHERE id={int(id)};"
        cursor.execute(query)
        recipes = cursor.fetchall()
        cursor.close()
        return jsonify({"recipes": recipes})

@app.route('/edit',methods=['GET'])
def edit_recipe():
    return render_template('edit_recipe.html')

# Updates recipe from table recipes
# Uses http method PUT
@app.route("/update/<int:id>", methods=["PUT"])
def update(id):
    pass


# Deletes recipe by id from table recipes
# Uses http method DELETE
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    with sqlite3.connect("recipe-book.db") as connection:
        create_table(connection)
        cursor = connection.cursor()
        cursor.execute("DELETE from recipes WHERE id=?", (id,))
        connection.commit()
        cursor.close()
        if cursor.rowcount == 0:
            return jsonify({"message": "Recipe not found"}), 404
        return jsonify({"message": "Recipe deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
