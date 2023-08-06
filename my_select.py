from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Student, Group, Teacher, Subject, Grade, Base

DATABASE_URL = 'postgresql://postgres:2299@localhost:5432/postgres'
engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()

# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.


def select_1():
    result = session.query(Student.fullname, func.round(func.avg(Grade.value), 2).label('avg_grade')) \
        .join(Grade).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return [(name, round(avg_grade, 2)) for name, avg_grade in result]

# 2. Знайти студента із найвищим середнім балом з певного предмета.


def select_2(subject_name):
    result = session.query(Student.fullname, func.round(func.avg(Grade.value), 2).label('avg_grade')) \
        .select_from(Student).join(Grade).join(Subject).filter(Subject.name == subject_name).group_by(Student.id) \
        .order_by(desc('avg_grade')).limit(1).first()
    if result:
        return result[0], round(result[1], 2)
    return None

# 3. Знайти середній бал у групах з певного предмета.


def select_3(subject_name):
    result = session.query(Student.group, func.round(func.avg(Grade.value), 2).label('avg_grade')) \
        .select_from(Student).join(Grade).join(Subject).filter(Subject.name == subject_name) \
        .group_by(Student.group).all()
    return [(group, round(avg_grade, 2)) for group, avg_grade in result]

# 4. Знайти середній бал на потоці (по всій таблиці оцінок).


def select_4():
    result = session.query(func.round(
        func.avg(Grade.value), 2).label('avg_grade')).scalar()
    return round(result, 2) if result else None

# 5. Знайти, які курси читає певний викладач.


def select_5(teacher_name):
    result = session.query(Subject.name).join(
        Teacher).filter(Teacher.name == teacher_name).all()
    return [name for name, in result]

# 6. Знайти список студентів у певній групі.


def select_6(group_name):
    result = session.query(Student.fullname).join(
        Group).filter(Group.name == group_name).all()
    return [name for name, in result]

# 7. Знайти оцінки студентів в окремій групі з певного предмета.


def select_7(group_name, subject_name):
    result = session.query(Student.fullname, Grade.value) \
        .join(Group).join(Grade).join(Subject) \
        .filter(Group.name == group_name, Subject.name == subject_name).all()
    return [(name, value) for name, value in result]

# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.


def select_8(teacher_name):
    result = session.query(func.round(func.avg(Grade.value), 2).label('avg_grade')) \
        .select_from(Grade).join(Subject).join(Teacher).filter(Teacher.name == teacher_name).scalar()
    return round(result, 2) if result else None

# 9. Знайти список курсів, які відвідує певний студент.


def select_9(student_name):
    result = session.query(Subject.name).join(Grade).join(
        Student).filter(Student.fullname == student_name).all()
    return [name for name, in result]

# 10. Список курсів, які певному студенту читає певний викладач.


def select_10(student_name, teacher_name):
    result = session.query(Subject.name) \
        .select_from(Subject).join(Grade).join(Student).join(Teacher) \
        .filter(Student.fullname == student_name, Teacher.name == teacher_name).all()
    return [name for name, in result]

# 11. Середній бал, який певний викладач ставить певному студентові.


def select_11(student_name, teacher_name):
    result = session.query(func.round(func.avg(Grade.value), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).join(Teacher) \
        .filter(Student.fullname == student_name, Teacher.name == teacher_name).scalar()
    return round(result, 2) if result else None

# 12. Оцінки студентів у певній групі з певного предмета на останньому занятті.


def select_12(group_name, subject_name):
    max_session_number = session.query(func.max(Grade.session_number)).scalar()
    result = session.query(Student.fullname, Grade.value) \
        .join(Group).join(Grade).join(Subject) \
        .filter(Group.name == group_name, Subject.name == subject_name, Grade.session_number == max_session_number).all()
    return [(name, value) for name, value in result]


if __name__ == "__main__":
    result_1 = select_1()
    print("Result 1:", result_1)

    result_2 = select_2('Math')
    print("Result 2:", result_2)

    result_3 = select_3('Math')
    print("Result 3:", result_3)

    result_4 = select_4()
    print("Result 4:", result_4)

    result_5 = select_5('John Doe')
    print("Result 5:", result_5)

    result_6 = select_6('Group A')
    print("Result 6:", result_6)

    result_7 = select_7('Group A', 'Math')
    print("Result 7:", result_7)

    result_8 = select_8('John Doe')
    print("Result 8:", result_8)

    result_9 = select_9('John Doe')
    print("Result 9:", result_9)

    result_10 = select_10('John Doe', 'Teacher A')
    print("Result 10:", result_10)

    result_11 = select_11('John Doe', 'Teacher A')
    print("Result 11:", result_11)

    result_12 = select_12('Group A', 'Math')
    print("Result 12:", result_12)
