from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        """returns a string representation of the class object"""
        return self.task


class ToDoList():
    def __init__(self):
        # create database file
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        # create database
        Base.metadata.create_all(self.engine)
        # create a session, to access database
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.today = datetime.today()

    def show_menu(self):
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
                self.show_today_tasks()

            elif menu_option == "2":
                self.show_week_tasks()

            elif menu_option == "3":
                self.show_all_tasks()

            elif menu_option == "4":
                self.show_missed_tasks()

            elif menu_option == "5":
                self.add_task()

            elif menu_option == "6":
                self.delete_task()

            elif menu_option == "0":
                print("Bye!")
                exit()

            else:
                print("Wrong parameters!")

    def add_task(self):
        new_task = input("Enter task\n")
        task_date = input("Enter deadline\n")
        try:
            new_row = Table(task=new_task, deadline=datetime.strptime(task_date, '%Y-%m-%d'))
        except ValueError:
            print("Wrong input")
        else:
            self.session.add(new_row)
            self.session.commit()
            print("The task has been added!\n")

    def print_tasks(self, rows):
        for i, row in enumerate(rows):
            print(str(i + 1) + ". " + row.task)

    def print_tasks_with_deadlines(self, rows):
        for i, row in enumerate(rows):
            print(str(i + 1) + ". " + row.task + ". " + str(row.deadline.day) + " " + row.deadline.strftime('%b'))

    def show_today_tasks(self):
        print("Today " + str(self.today.day) + " " + self.today.strftime('%b') + ":")
        rows = self.session.query(Table).filter(Table.deadline == self.today.date()).all()
        if rows:
            self.print_tasks(rows)
            print()
        else:
            print("Nothing to do!\n")

    def show_week_tasks(self):
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i in range(7):
            next_day = self.today + timedelta(days=i)
            print(days_of_week[next_day.weekday()], next_day.day, next_day.strftime('%b') + ":")
            rows = self.session.query(Table).filter(Table.deadline == next_day.date()).all()
            if rows:
                self.print_tasks(rows)
                print()
            else:
                print("Nothing to do!\n")

    def show_all_tasks(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print("All tasks:")
        if rows:
            self.print_tasks_with_deadlines(rows)
            print()
        else:
            print("Nothing to do!\n")

    def show_missed_tasks(self):
        rows = self.session.query(Table).filter(Table.deadline < self.today.date()).order_by(Table.deadline).all()
        print("Missed tasks:")
        if rows:
            self.print_tasks_with_deadlines(rows)
            print()
        else:
            print("Nothing to do!\n")

    def delete_task(self):
        print("Choose the number of the task you want to delete:")
        rows = self.session.query(Table).order_by(Table.deadline).all()
        if rows:
            self.print_tasks_with_deadlines(rows)
            try:
                row_to_delete = int(input())
                specific_row = rows[row_to_delete - 1]
            except (ValueError, IndexError) as e:
                print("Wrong input, enter one number from list printed above!")
            else:
                self.session.delete(specific_row)
                self.session.commit()
                print("The task has been deleted!\n")
        else:
            print("Nothing to delete\n")


if __name__ == '__main__':
    ToDoList().show_menu()
