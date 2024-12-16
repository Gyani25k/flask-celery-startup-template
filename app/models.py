from app import db

class TaskResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_data = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
