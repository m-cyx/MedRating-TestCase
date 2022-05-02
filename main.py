from datetime import datetime
import os
import time
import requests


def main():
    todos = get_api_data("https://json.medrating.org/todos")
    users = get_api_data("https://json.medrating.org/users")

    create_files(users, todos)


def get_api_data(path):
    try:
        api_data = requests.get(path).json()
    except Exception as ex:
        print(ex)
    return api_data


def create_files(users, todos):
    if not os.path.exists("tasks"):
        os.mkdir("tasks")

    for user in users:
        file_name = f"{user.get('username')}"

        if os.path.exists(f"tasks/{file_name}.txt"):
            rename_file(file_name)

        with open(f"tasks/{file_name}.txt", "w", encoding="utf-8") as user_file:
            report = create_report(user, todos)
            user_file.write(report)


def rename_file(file_name):
    creation_date = os.path.getmtime(f"tasks/{file_name}.txt")
    creation_date = datetime.strptime(time.ctime(
        creation_date), "%a %b %d %H:%M:%S %Y").strftime('%Y-%m-%dT%H-%M')
    os.renames(f"tasks/{file_name}.txt",
               f"tasks/old_{file_name}_{creation_date}.txt")


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


def get_user_tasks(user_id, todos):
    user_tasks = {'total_tasks': 0, 'completed_tasks': 0, 'uncompleted_tasks': 0,
                  'completed_tasks_titles': '', 'uncompleted_tasks_titles': ''}

    # В случае масштабирования возможна оптимизация: сериализовать json, чтобы уйти от O(n^2).
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


def cut_title(title):
    if len(title) > 48:
        return title[:48] + '...\n'
    return title + '\n'


if __name__ == '__main__':
    main()
