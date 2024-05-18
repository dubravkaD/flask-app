from flask import Flask, render_template, request, jsonify

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


@app.rout("/add", methods=["POST"])
def add():
    pass

@app.rout("/get", methods=["GET"])
def get():
    pass

@app.rout("/get/<int:id>", methods=["GET"])
def get_recipe(id):
    pass


@app.rout("/update/<int:id>", methods=["PUT"])
def update(id):
    pass


@app.rout("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
