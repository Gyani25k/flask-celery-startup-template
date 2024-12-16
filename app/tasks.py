from app import create_app, make_celery, db
from app.models import TaskResult

app = create_app()
celery = make_celery(app)

@celery.task(bind=True)
def background_task(self, user_input):
    try:
        # Simulate long computation
        result = f"Processed input: {user_input}"

        # Save result to SQLite
        with app.app_context():
            task = TaskResult(
                input_data=user_input,
                result=result,
                status='SUCCESS'
            )
            db.session.add(task)
            db.session.commit()

        return result

    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        with app.app_context():
            task = TaskResult(
                input_data=user_input,
                result=str(e),
                status='FAILURE'
            )
            db.session.add(task)
            db.session.commit()
        raise
