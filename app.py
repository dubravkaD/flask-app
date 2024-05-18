from flask import Flask, render_template

app = Flask(__name__)


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


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
