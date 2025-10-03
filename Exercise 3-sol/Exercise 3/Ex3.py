from flask import Flask, render_template

app = Flask(__name__)

@app.route('/table')

def display_table():
    """
        Function to display student data into HTML table using Jinja2
    """

    # Create list and dictionaries containing student data
    data = [
        {'name': 'Alice', 'age': 22},
        {'name': 'Bob', 'age': 19},
        {'name': 'Charlie', 'age': 25},
        {'name': 'David', 'age': 24},
        {'name': 'Eve', 'age': 21}
    ]

    """
    render_template() function:
        - Looks for "table.html" 
        - Pass the data to the "templates" folder as students variable
        = Return the rendered HTML to the browser
    """
    return render_template('table.html', students=data)

if __name__ == '__main__':
    app.run(debug=True)