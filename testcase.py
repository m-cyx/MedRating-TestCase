from datetime import datetime
from genericpath import exists, getmtime
import os
import time
import requests


def read_from_api(path):
    try:
        response_json = requests.get(path).json()
        return response_json
    except:
        print(f'Connection-Error failed to get data from: {path}')


def cut_title(title):
    if len(title) > 48:
        return title[:48] + '...\n'
    return title + '\n'


def get_user_tasks(user_id, todos):
    user_tasks = {'total_tasks': 0, 'completed_tasks': 0, 'uncompleted_tasks': 0,
                  'completed_tasks_titles': '', 'uncompleted_tasks_titles': ''}

    for task in todos:
        if task.get("userId") == user_id:
            user_tasks['total_tasks'] += 1

            if task.get("completed"):
                user_tasks['completed_tasks'] += 1
                user_tasks['completed_tasks_titles'] += \
                    cut_title(task.get("title"))
            else:
                user_tasks['uncompleted_tasks'] += 1
                user_tasks['uncompleted_tasks_titles'] += \
                    cut_title(task.get("title"))
    return user_tasks


def create_report(user, todos):
    creation_date = datetime.now().strftime('%d.%m.%Y %H:%M')
    user_tasks = get_user_tasks(user.get("id"), todos)
    report = (f"Отчёт для {user.get('company').get('name')}.\n"
              f"{user.get('name')} <{user.get('email')}> {creation_date}\n"
              f"Всего задач: {user_tasks.get('total_tasks')}\n\n"
              f"Завершённые задачи ({user_tasks.get('completed_tasks')}):\n"
              f"{user_tasks['completed_tasks_titles']} "
              f"\nОставшиеся задачи ({user_tasks.get('uncompleted_tasks')}):\n"
              f"{user_tasks.get('uncompleted_tasks_titles')} ")
    return report


def get_user_file_name(user):
    file_name = f"{user.get('username')}"

    if exists(f"tasks/{file_name}.txt"):
        crt_date = getmtime(f"tasks/{file_name}.txt")
        crt_date = datetime.strptime(time.ctime(
            crt_date), "%a %b %d %H:%M:%S %Y").strftime('%Y-%m-%dT%H-%M')
        os.renames(f"tasks/{file_name}.txt",
                   f"tasks/old_{file_name}_{crt_date}.txt")
    return file_name


def write_files(users, todos):
    if not exists("tasks"):
        os.mkdir("tasks")

    for user in users:
        user_file = open(
            f"tasks/{get_user_file_name(user)}.txt", "w", encoding='utf-8')
        record = create_report(user, todos)
        user_file.write(record)


def main():
    todos = read_from_api("https://json.medrating.org/todos")
    users = read_from_api("https://json.medrating.org/users")

    try:
        write_files(users, todos)
    except:
        print('Unexpected error')


if __name__ == '__main__':
    main()
