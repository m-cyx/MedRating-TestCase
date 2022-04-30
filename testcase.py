from datetime import datetime
import os
import time
import requests
# задокументирвоать функции
# обратить внимание на двоеточие в названии. на линуксе должно быть ок


def read_from_api(path):
    response_json = requests.get(path).json()
    # сюда добавить проверку, что всё окей, выкинуть исключение если не ок
    return response_json


def cut_str(str):
    # проверяет и режет строки
    if len(str) > 48:
        return str[:48] + '...\n'
    return str + '\n'


def get_todos_by_user_id(user_id, todos):
    # будет возвращать словарь в котором два ключа completed и not_completed значения - айдишники задач (или сами задачи??)
    # переделать, чтобы возвращала тудушки
    # создать отдельно функцию, которая сортирует и пакует в словарь при этом обрезая строки
    user_todos_dict = {}
    completed = []
    not_completed = []
    for todo in todos:
        if todo.get("userId") == user_id:
            if todo.get("completed"):
                # хранить тут туду айди, чтобы по нему потом брать тудушку
                completed.append(cut_str(todo.get("title")))
            else:
                not_completed.append(cut_str(todo.get("title")))

    user_todos_dict['completed_todos'] = completed
    user_todos_dict['not_completed_todos'] = not_completed

    return user_todos_dict


def create_report(user, todos):
    # мб написать гет юзер дата бай юзер айди, а основной аргумент будет юзер айди
    # user_id = user.get("id")
    creation_date = datetime.now().strftime('%d.%m.%Y %H:%M')

    user_todos_dict = get_todos_by_user_id(user.get("id"), todos)
    completed_todos = user_todos_dict.get("completed_todos")
    not_completed_todos = user_todos_dict.get("not_completed_todos")

    report = (f"Отчёт для {user.get('company').get('name')}.\n"
              f"{user.get('name')} <{user.get('email')}> {creation_date}\n"
              f"Всего задач: {len(completed_todos) + len(not_completed_todos)}\n\n"
              f"Завершённые задачи ({len(completed_todos)}):\n")
    #   f"{user_todos_dict['completed_todos']} ")
    # вынести в отдельный метод
    for todo in completed_todos:
        report += todo

    report += f"\nОставшиеся задачи: ({len(not_completed_todos)})\n"

    for todo in not_completed_todos:
        report += todo

    return report


def get_user_filename(user):
    filename = f"{user.get('username')}"
    if os.path.exists(f"tasks/{filename}.txt"):
        created_at = os.path.getmtime(f"tasks/{filename}.txt")
        created_at = datetime.strptime(
            time.ctime(created_at), "%a %b %d %H:%M:%S %Y")
        os.renames(f"tasks/{filename}.txt",
                   f"tasks/old_{filename}_{created_at.strftime('%Y-%m-%dT%H-%M')}.txt")
    return filename


def mkdir(directory_name):
    try:
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
        return True
    except OSError:
        print("эрор!")
        return False


def write(users, todos):
    if mkdir("tasks"):
        for user in users:
            user_file = open(
                f"tasks/{get_user_filename(user)}.txt", "w", encoding='utf-8')
            record = create_report(user, todos)
            user_file.write(record)


def main():
    todos = read_from_api("https://json.medrating.org/todos")
    users = read_from_api("https://json.medrating.org/users")

    write(users, todos)


if __name__ == '__main__':
    main()
