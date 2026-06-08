from models import User, Task

class TaskServices:
    def __init__(self, session):
        self.session = session

    def create_user(self, username, role="employee"):
        user = User(username=username, role=role)
        self.session.add(user)
        self.session.commit()
        return user

    def get_user(self, username):
        return self.session.query(User).filter_by(username=username).first()
    
    def get_all_users(self):
        return self.session.query(User).all()
    
    def is_admin(self, user):
        return user.role == "admin"

    def create_task(self, title, user_id):
        task = Task(title=title, user_id=user_id)
        self.session.add(task)
        self.session.commit()

    def get_tasks(self, user_id):
        return self.session.query(Task).filter_by(user_id=user_id).all()

    def delete_task(self, task_id):
        task = self.session.get(Task, task_id)
        if task:
            self.session.delete(task)
            self.session.commit()
            
            

