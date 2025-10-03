from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

# Model
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    math = db.Column(db.Float, nullable=False)
    physics = db.Column(db.Float, nullable=False)
    informatics = db.Column(db.Float, nullable=False)

# Hàm tính xếp loại
def qualify(avg):
    if avg >= 18: return "Excellent"
    if avg >= 16: return "Very Good"
    if avg >= 14: return "Good"
    if avg >= 10: return "Average Good"
    return "Fail"

# API POST nhận student_id và trả về kết quả
@app.route('/api/student', methods=['POST'])
def get_student():
    sid = request.json['student_id']
    s = Student.query.filter_by(student_id=sid).first()   # giả định luôn tồn tại
    avg = (s.math + s.physics + s.informatics) / 3
    return jsonify({
        "student_id": s.student_id,
        "math": s.math,
        "physics": s.physics,
        "informatics": s.informatics,
        "average": round(avg, 2),
        "qualification": qualify(avg)
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
