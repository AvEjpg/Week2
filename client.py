# client.py
import requests
import json

BASE_URL = 'http://127.0.0.1:5000/api/items'

def print_response(response):
    """Утилита для красивого вывода ответа сервера."""
    print(f'Status: {response.status_code}')
    try:
        print('Response:', json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print('Response text:', response.text)
    print('---')

if __name__ == '__main__':
    # 1. GET всех элементов (ожидаем пустой список)
    print('1. GET all items (should be empty)')
    resp = requests.get(BASE_URL)
    print_response(resp)

    # 2. POST – создание элемента
    print('2. POST – create item 1')
    resp = requests.post(BASE_URL, json={'name': 'Task 1', 'description': 'First task'})
    print_response(resp)

    # 3. POST – создание ещё одного (без description)
    print('3. POST – create item 2')
    resp = requests.post(BASE_URL, json={'name': 'Task 2'})
    print_response(resp)

    # 4. GET всех элементов (теперь два)
    print('4. GET all items')
    resp = requests.get(BASE_URL)
    print_response(resp)

    # 5. GET по существующему ID
    print('5. GET item with id=1')
    resp = requests.get(f'{BASE_URL}/1')
    print_response(resp)

    # 6. GET по несуществующему ID (ошибка 404)
    print('6. GET item with id=999 (should be 404)')
    resp = requests.get(f'{BASE_URL}/999')
    print_response(resp)

    # 7. PUT – обновление существующего элемента
    print('7. PUT update item id=1')
    resp = requests.put(f'{BASE_URL}/1', json={'description': 'Updated description'})
    print_response(resp)

    # 8. Проверка обновления
    print('8. GET item id=1 after update')
    resp = requests.get(f'{BASE_URL}/1')
    print_response(resp)

    # 9. PUT несуществующего элемента (404)
    print('9. PUT non-existent id')
    resp = requests.put(f'{BASE_URL}/999', json={'name': 'New'})
    print_response(resp)

    # 10. DELETE существующего элемента
    print('10. DELETE item id=1')
    resp = requests.delete(f'{BASE_URL}/1')
    print_response(resp)

    # 11. GET всех после удаления (должен остаться только item 2)
    print('11. GET all after delete')
    resp = requests.get(BASE_URL)
    print_response(resp)

    # 12. DELETE несуществующего (404)
    print('12. DELETE non-existent')
    resp = requests.delete(f'{BASE_URL}/1')
    print_response(resp)

    # 13. POST с недостающими полями (нет name – 400)
    print('13. POST missing required field')
    resp = requests.post(BASE_URL, json={'description': 'No name'})
    print_response(resp)

    # 14. POST с не-JSON данными (простой текст – 400)
    print('14. POST with plain text')
    resp = requests.post(BASE_URL, data='plain text', headers={'Content-Type': 'text/plain'})
    print_response(resp)