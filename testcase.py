from datetime import datetime
import os
import time
import requests
# задокументирвоать функции на английском
# обратить внимание на двоеточие в названии старых файлов. на линуксе должно быть ок


def read_from_api(path):
    response_json = requests.get(path).json()
    # сюда добавить проверку, что всё окей, выкинуть исключение если не ок
    return response_json


def cut_title(title):
    # проверяет и режет строки
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


def get_user_filename(user):
    # укоротить
    filename = f"{user.get('username')}"
    if os.path.exists(f"tasks/{filename}.txt"):
        created_at = os.path.getmtime(f"tasks/{filename}.txt")
        created_at = datetime.strptime(
            time.ctime(created_at), "%a %b %d %H:%M:%S %Y")
        os.renames(f"tasks/{filename}.txt",
                   f"tasks/old_{filename}_{created_at.strftime('%Y-%m-%dT%H-%M')}.txt")
    return filename


def dir_exist(dir_name):
    # можно сократить
    try:
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        return True
    except OSError:
        print("эрор!")
        return False


def write_files(users, todos):
    if dir_exist("tasks"):
        for user in users:
            user_file = open(
                f"tasks/{get_user_filename(user)}.txt", "w", encoding='utf-8')
            record = create_report(user, todos)
            user_file.write(record)


def main():
    todos = read_from_api("https://json.medrating.org/todos")
    users = read_from_api("https://json.medrating.org/users")

    write_files(users, todos)


if __name__ == '__main__':
    main()
