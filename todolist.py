from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# create database file
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
# model class that describes the table in the database.
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        """returns a string representation of the class object"""
        return self.task


def add_task():
    new_task = input("Enter task\n")
    task_date = input("Enter deadline\n")
    new_row = Table(task=new_task, deadline=datetime.strptime(task_date, '%Y-%m-%d'))
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def show_today_tasks():
    today = datetime.today()
    print("Today " + str(today.day) + " " + today.strftime('%b') + ":")
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for i, row in enumerate(rows):
            print(str(i+1) + ". " + row.task)


def show_week_tasks():
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = datetime.today()
    for i in range(7):
        next_day = today + timedelta(days=i)
        print(days_of_week[next_day.weekday()], next_day.day, next_day.strftime('%b') + ":")
        rows = session.query(Table).filter(Table.deadline == next_day.date()).all()
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for i, row in enumerate(rows):
                print(str(i + 1) + ". " + row.task)
        print()


def show_all_tasks():
    rows = session.query(Table).order_by(Table.deadline).all()
    print("All tasks:")
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for i, row in enumerate(rows):
            print(str(i + 1) + ". " + row.task + ". " + str(row.deadline.day) + " " + row.deadline.strftime('%b'))


def show_missed_tasks():
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    print("Missed tasks:")
    if len(rows) == 0:
        print("Nothing is missed!")
    else:
        for i, row in enumerate(rows):
            print(str(i + 1) + ". " + row.task + ". " + str(row.deadline.day) + " " + row.deadline.strftime('%b'))
    print()


def delete_task():
    print("Choose the number of the task you want to delete:")
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows) == 0:
        print("Nothing to delete")
    else:
        for i, row in enumerate(rows):
            print(str(i + 1) + ". " + row.task + ". " + str(row.deadline.day) + " " + row.deadline.strftime('%b'))

        row_to_delete = int(input())
        specific_row = rows[row_to_delete - 1]
        session.delete(specific_row)
        session.commit()
        print("The task has been deleted!")


if __name__ == '__main__':
    # create database
    Base.metadata.create_all(engine)
    # create a session, to access database
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("1) Today's tasks\n"
              "2) Week's tasks\n"
              "3) All tasks\n"
              "4) Missed tasks\n"
              "5) Add task\n"
              "6) Delete task\n"
              "0) Exit")
        menu_option = input()
        if menu_option == "1":
            show_today_tasks()

        elif menu_option == "2":
            show_week_tasks()

        elif menu_option == "3":
            show_all_tasks()

        elif menu_option == "4":
            show_missed_tasks()

        elif menu_option == "5":
            add_task()

        elif menu_option == "6":
            delete_task()

        elif menu_option == "0":
            print("Bye!")
            exit()
