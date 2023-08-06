from faker import Faker
import random
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Student, Group, Teacher, Subject, Grade, Base

faker = Faker()
DATABASE_URL = 'postgresql://postgres:2299@localhost:5432/postgres'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def generate_grades():
    return [random.randint(60, 100) for _ in range(10)]


# Створюємо групи
groups = [Group(name=f'Group {i}') for i in range(1, 4)]
session.add_all(groups)
session.commit()

# Створюємо викладачів
teachers = [Teacher(name=faker.name()) for _ in range(3)]
session.add_all(teachers)
session.commit()

# Створюємо предмети
subjects = [Subject(name=f'Subject {i}', teacher=random.choice(
    teachers)) for i in range(1, 6)]
session.add_all(subjects)
session.commit()

# Створюємо студентів та додаємо їх у групи та предмети
for group in groups:
    for _ in range(10):
        student = Student(fullname=faker.name(), group=group)
        student.teacher = random.choice(teachers)
        session.add(student)

        # Add this block to add grades for each student
        for subject in subjects:
            grades = generate_grades()
            for i, grade_value in enumerate(grades):
                grade = Grade(value=grade_value,
                              student=student, subject=subject)
                session.add(grade)

session.commit()
