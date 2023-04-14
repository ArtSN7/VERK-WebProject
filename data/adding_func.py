from users import User
from projects import Project
from tasks import Tasks
import db_session as session
import datetime




def add_user():
    session.global_init("db/blogs.db")
    db_session = session.create_session()
    
    number = int(input('Введите кол-во желаемых добавлений юзеров: '))
    
    for i in range(number):
        print('')
        print(f'Делаем User {i}:')
        print('')
        
        user = User()
        user.login = input('Login: ')
        user.set_password(input('Pas: '))
        user.password = user.password_hash
        user.email = input('Email: ')
        user.name = input('Name: ')
        user.projects = input('Projects (1, 4, 5): ')
        user.tasks = input('Tasks (1, 4, 5): ')
        user.picture = 1
        
        db_session.add(user)
        
    db_session.commit()
    
    
def add_project():
    session.global_init("db/blogs.db")
    db_session = session.create_session()
    
    number = int(input('Введите кол-во желаемых добавлений проектов: '))
    
    for i in range(number):
        print('')
        print(f'Делаем Project {i}:')
        print('')
        
        user = Project()
        user.img = int(input('Число от 1 до 11: '))
        user.title = input('Title: ')
        user.description = input('Description: ')
        user.users = input('Users (ID юзеров через запятую ( 1, 4, 5 и тд)): ')
        user.tasks = input('Tasks (1, 4, 5): ')
        
        db_session.add(user)
        
    db_session.commit()
    

def add_tasks():
    session.global_init("db/blogs.db")
    db_session = session.create_session()
    
    number = int(input('Введите кол-во желаемых добавлений задач: '))
    
    for i in range(number):
        print('')
        print(f'Делаем Tasks {i}:')
        print('')
        
        user = Tasks()
        user.project = int(input('ID преокта к которому привязан: '))
        user.description = input('Description: ')
        user.users = input('Users (ID юзеров через запятую ( 1, 4, 5 и тд)): ')
        user.start_date = datetime.datetime.now()
        user.end_date = datetime.datetime.now()
        
        db_session.add(user)
        
    db_session.commit()
    
    
    
add_user()
add_project()
add_tasks()