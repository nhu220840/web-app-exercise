from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define Student model
class Student(db.Model):
    # Student table model with id, name, class, and mark fields
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    mark = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Student {self.name}>'

# Home route with navigation links
@app.route('/')
def home():
    # Home page with links to all database operations
    return '''
    <h1>Exercise 8: Database Operations</h1>
    <h2>Database Setup:</h2>
    <ul>
        <li><a href="/create_table">1. Create Students Table</a></li>
        <li><a href="/insert_data">2. Insert Sample Data</a></li>
        <li><a href="/update_class">3. Update Class for Low Marks</a></li>
    </ul>
    <h2>View Students:</h2>
    <ul>
        <li><a href="/all_students">All Students</a></li>
        <li><a href="/excellent_students">Excellent Students (Mark > 75)</a></li>
        <li><a href="/good_students">Good Students (60-75)</a></li>
        <li><a href="/average_students">Average Students (< 60)</a></li>
    </ul>
    '''

# Route 1: Create the table
@app.route('/create_table')
def create_table():
    """
    Create the students table in the database
    db.create_all() creates all tables defined by models that don't exist yet
    """
    try:
        db.create_all()
        return "Students table created successfully! <a href='/'>Back to Home</a>"
    except Exception as e:
        return f"Error creating table: {str(e)} <a href='/'>Back to Home</a>"

# Route 2: Insert sample data
@app.route('/insert_data')
def insert_data():
    """
    Insert sample student data into the database
    This shows:
    - creating model instances
    - adding them to the session
    - committing the transaction
    """
    try:
        # Check if data already exists
        if Student.query.count() > 0:
            return "Data already exists in database. <a href='/all_students'>View Students</a> | <a href='/'>Home</a>"
        
        # Sample student data
        students_data = [
            {'name': 'John', 'class_name': 'One', 'mark': 80},
            {'name': 'Alice', 'class_name': 'One', 'mark': 45},
            {'name': 'Bob', 'class_name': 'One', 'mark': 90},
            {'name': 'Charlie', 'class_name': 'One', 'mark': 55},
            {'name': 'Diana', 'class_name': 'One', 'mark': 78},
            {'name': 'Eve', 'class_name': 'One', 'mark': 30},
        ]
        
        # Create new Student instance
        for data in students_data:
            student = Student(
                name=data['name'],
                class_name=data['class_name'],
                mark=data['mark']
            )
            # Add to database session (prepares for insertion)
            db.session.add(student)
        
        # Commit all changes to database (executes INSERT statements)
        # Just like github commands (add first, commit later, no push though) ✌️ 
        db.session.commit()
        return "Sample data inserted successfully! <a href='/all_students'>View Students</a> | <a href='/'>Home</a>"
        
    except Exception as e:
        # If error occurs, rollback the transaction
        db.session.rollback()
        return f"Error inserting data: {str(e)} <a href='/'>Back to Home</a>"

# Route 3: Update class for students with marks < 60
@app.route('/update_class')
def update_class():
    """
    Update the class to "Two" for students with marks less than 60
    
    This shows:
    - filtering records using SQLAlchemy queries
    - updating multiple records
    - database transactions
    """
    try:
        # Query students with marks < 60
        # Just like "SELECT * FROM students WHERE mark < 60"
        low_mark_students = Student.query.filter(Student.mark < 60).all()
        
        # Update their class to "Two"
        for student in low_mark_students:
            student.class_name = "Two"
        
        # Commit the changes
        # In SQL it would be: UPDATE students SET class_name = 'Two' WHERE mark < 60
        db.session.commit()
        return f"Updated {len(low_mark_students)} students to class 'Two'. <a href='/all_students'>View Students</a> | <a href='/'>Home</a>"
        
    except Exception as e:
        db.session.rollback()
        return f"Error updating data: {str(e)} <a href='/'>Back to Home</a>"

# Route 4: Display all students
@app.route('/all_students')
def all_students():
    """
    Display all students in the database
    """
    # Query all students
    # SQL: SELECT * FROM students
    students = Student.query.all()
    return render_template('students_table.html', students=students, title="All Students")

# Route 5: Display excellent students (mark > 75)
@app.route('/excellent_students')
def excellent_students():
    """
    Display students with marks greater than 75
    
    SQLAlchemy Query Methods:
    - Student.query: Creates a query object
    - .filter(): Adds WHERE conditions
    - .all(): Returns all matching records as a list
    """
    # Query excellent students
    # SQL: SELECT * FROM students WHERE mark > 75
    students = Student.query.filter(Student.mark > 75).all()
    return render_template('students_table.html', students=students, title="Excellent Students (Mark > 75)")

# Route 6: Display good students (60 <= mark <= 75)
@app.route('/good_students')
def good_students():
    """
    Display students with marks between 60 and 75 (inclusive)
    Multiple filter conditions using AND logic
    """
    # Query good students with compound condition
    # SQL: SELECT * FROM students WHERE mark >= 60 AND mark <= 75
    students = Student.query.filter(Student.mark >= 60, Student.mark <= 75).all()
    return render_template('students_table.html', students=students, title="Good Students (60-75)")

# Route 7: Display average students (mark < 60)
@app.route('/average_students')
def average_students():
    """
    Display students with marks less than 60
    """
    # Query average students
    # SQL: SELECT * FROM students WHERE mark < 60
    students = Student.query.filter(Student.mark < 60).all()
    return render_template('students_table.html', students=students, title="Average Students (< 60)")

# Run the application
if __name__ == '__main__':
    # Create database tables when app starts
    with app.app_context():
        db.create_all()
    
    # Run in debug mode
    app.run(debug=True)