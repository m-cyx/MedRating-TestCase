import os
import requests
# задокументирвоать функции


def read_from_api(path):
    """Чтение из API типа 'json' и возвращение данных типа 'dict'
    :param path: путь до файла типа 'json'
    :return response_json: - json файл
    """
    response_json = requests.get(path).json()
    # сюда добавить проверку, что всё окей, выкинуть исключение если не ок
    return response_json

# проверяет и режет строки
def cut_str(str):
    if len(str) > 48:
        return str[:48] + '...\n'
    return str + '\n'
    
# будет возвращать словарь в котором два ключа completed и not_completed значения - айдишники задач (или сами задачи??)
def get_todos_by_user_id(user_id):
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



def report_maker(user):
    # мб написать гет юзер дата бай юзер айди, а основной аргумент будет юзер айди
    user_id = user.get("id")
    # вместо юзера сделать доступ по юзер айди
    company_name = user.get("company").get("name")
    name = user.get("name")
    email = user.get("email")
    creation_date = "тут дата"
    username = user.get("username")

    user_todos_dict = get_todos_by_user_id(user_id)
    completed_todos = user_todos_dict.get("completed_todos")
    not_completed_todos = user_todos_dict.get("not_completed_todos")

    report = (f"Отчёт для {company_name}.\n"
              f"{name} <{email}> {creation_date}\n"
              f"Всего задач: {len(completed_todos) + len(not_completed_todos)}\n\n"
              f"Завершённые задачи ({len(completed_todos)}):\n")

    # вынести в отдельный метод
    for todo in completed_todos:
        report = report + todo

    report = report + f"\nОставшиеся задачи: ({len(not_completed_todos)})\n"

    for todo in not_completed_todos:
        report = report + todo

    return report
    

def make_file(report, username):
    # вернуть лучше репорт, а запись вынести в отдельную функию, там и работу с файлами сделать
    file = open(f"{username}.txt", "w", encoding='utf-8')
    # добавить кодировку ютф8
    file.write(report)


# список задач из 'todos' (элементы списка типа 'dict')
todos = read_from_api("https://json.medrating.org/todos")
# список пользователей из 'users' (элементы списка типа 'dict')
users = read_from_api("https://json.medrating.org/users")


if not os.path.isdir("tasks"):
    os.mkdir("tasks")
    # переходим в каталог "tasks"
os.chdir("tasks")

for user in users:

    report = report_maker(user)
    make_file(report, user.get("username"))
