from flask import Flask
import math

app = Flask(__name__)

"""
Define route for the URL parameter: <int:number>
    - Accept a parameter as the name number
    - Convert the parameter into integer automatically
    - Pass the parameter to the function later as an argument
"""
@app.route('/factorial/<int:number>')

def caluculate_factorial(number):

    try: 
        if number < 0:
            return f"Error: Factorial number cannot be negative!"

        result = math.factorial(number)
        return f"<h1>The factorial of {number} is {result}/<h1>"
        
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)