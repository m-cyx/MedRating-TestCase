from datetime import datetime
import os
import time

user = {
    "id": 1,
    "name": "Leanne Graham",
    "username": "test",
    "email": "Sincere@april.biz",
    "address": {
        "street": "Kulas Light",
        "suite": "Apt. 556",
        "city": "Gwenborough",
        "zipcode": "92998-3874",
        "geo": {
            "lat": "-37.3159",
            "lng": "81.1496"
        }
    },
    "phone": "1-770-736-8031 x56442",
    "website": "hildegard.org",
    "company": {
        "name": "Romaguera-Crona",
        "catchPhrase": "Multi-layered client-server neural-net",
        "bs": "harness real-time e-markets"
    }
}


def get_user_file_name(user):
    file_name = f"{user.get('username')}"
    
    if os.path.exists(f"tasks/{file_name}.txt"):
        crt_date = os.path.getctime(f"tasks/{file_name}.txt")
        crt_date = datetime.strptime(time.ctime(
            crt_date), "%a %b %d %H:%M:%S %Y").strftime('%Y-%m-%dT%H-%M')
        os.renames(f"tasks/{file_name}.txt",
                   f"tasks/old_{file_name}_{crt_date}.txt")
    return file_name


print(get_user_file_name(user))
