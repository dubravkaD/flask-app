from flask import Flask, render_template, request, jsonify, url_for
import sqlite3
import json

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
        recipe = cursor.fetchone()
        cursor.close()
        if recipe is None:
            return jsonify({"message": "Recipe not found"}), 404
        return jsonify(dict(zip(["id","title","category","servings","ingredients","directions",],recipe,))),200


# Returns edit_recipe page
# Uses http method GET
@app.route("/edit", methods=["GET"])
def edit_recipe():
    ids = get_ids()
    # print(min(ids),max(ids))
    # return url_for('edit_recipe')
    return render_template("edit_recipe.html", min=min(ids), max=max(ids))


# Updates recipe from table recipes
# Uses http method PUT
@app.route("/update/<int:id>", methods=["PUT"])
def update(id):
    data = request.get_json(force=True) # class dict -> json
    json_data=jsonify(data).json
    # print(type(data))
    # print(data)
    # print(data['title'])
    # print(type(json_data))
    # print(json_data)
    # print(json_data['id'])

    recipe=json_data

    # data_str=str(data,'utf-8')
    # recipe_json=json.loads(data_str)
    # json_data = json.dumps(data)
    # print(data_str)
    # print(type(recipe_json),recipe_json)
    # print(type(json_data))
    # print(json_data)

    # recipe = json.loads(data)
    # print(recipe)

    # print(data.to_dict(flat=False))
    # list = data.to_dict(flat=False)
    # print(list)

    # data = request.form
    # print(type(data.getlist('title'))) # class list
    # print(data.to_dict(flat=False))
    # list = data.to_dict(flat=False)
    # print(list)

    # recipe = json.loads(data)
    # print(recipe)

    # data = request.get_data()  # class bytes
    # print(type(data))
    # recipe = str(data)
    # recipe = recipe.replace("b", "")
    # recipe = recipe.replace("'", "")
    # print(recipe,type(recipe))
    # recipe = json.loads(recipe)
    # print(type(data), type(recipe))
    # print(recipe)

    # return jsonify({"message": "hi"}), 200

    with sqlite3.connect("recipe-book.db") as conn:
        create_table(conn)
        cursor = conn.cursor()
        # cursor.execute(
        #         "UPDATE recipes SET title=?, category=?, servings=?, ingredients=?, directions=? WHERE id=?",
        #         (
        #             title,
        #             category,
        #             servings,
        #             ingredients,
        #             directions,
        #             id,
        #         ),
        #     )
        query = f"UPDATE recipes SET title='{recipe['title']}', category='{recipe['category']}', servings='{int(recipe['servings'])}', ingredients='{recipe['ingredients']}', directions='{recipe['directions']}' WHERE id={int(id)};"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        return jsonify({"message": "Recipe updated"}), 200


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


# Gets all values for field id in db
def get_ids():
    with sqlite3.connect("recipe-book.db") as conn:
        create_table(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM recipes")
        rows = cursor.fetchall()
        cursor.close()
        newRows = []
        [newRows.append(int(row[0])) for row in rows]
        # print(type(newRows)) # class list
        return newRows


if __name__ == "__main__":
    app.run(debug=True)
