import os
import json
import csv


class PriceMachine:

    def __init__(self):
        self.data = []
        self.result = ''
        # self.name_length = 0

    # load_prices - сканирует папку и загружает данные
    def load_prices(self, file_path='.'):

        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''

        header_product = ['товар', 'название', 'наименование', 'продукт']
        header_price = ['розница', 'цена']
        header_weight = ['вес', 'масса', 'фасовка']

        # Количество и название файлов заранее неизвестно,
        # однако точно известно, что в названии файлов прайс-листов есть слово "price".
        for file_name in os.listdir(file_path):
            path = os.path.join(file_path, file_name)

            # Файлы, не содержащие слово "price" следует игнорировать.
            if 'price' in file_name and os.path.isfile(path):
                file_path = os.path.join(file_path, file_name)

                # Открываем файл по проверенному пути
                with open(file_path, newline='', encoding='utf-8') as file:
                    # Читаем строки CSV-файла и преобразуем их в словари
                    read = csv.DictReader(file)
                    # Возвращает список заголовков
                    headers = read.fieldnames
                    # Получаем индексы столбцов для названия товара, цены и веса
                    product_index = self._search_product_price_weight(headers, header_product)
                    price_index = self._search_product_price_weight(headers, header_price)
                    weight_index = self._search_product_price_weight(headers, header_weight)

                    # Проверяем, что все индексы найдены
                    if product_index is not None and price_index is not None and weight_index is not None:
                        # Перебираем строки в CSV-файле
                        for row in read:
                            product_name = row[headers[product_index]]
                            price = row[headers[price_index]]
                            weight = row[headers[weight_index]]

                            # Преобразуем цену и вес в числа с плавающей точкой
                            price = float(price)
                            weight = float(weight)

                            # Вычисляем цену за килограмм
                            price_per_kg = price / weight

                            # Добавляем данные в список
                            self.data.append({
                                'product_name': product_name,
                                'price': price,
                                'weight': weight,
                                'file_name': file_name,
                                'price_per_kg': price_per_kg
                            })

    def _search_product_price_weight(self, headers, name_header):

        '''
            Возвращает номера столбцов
        '''

        # Перебираем заголовки с индексами
        for index, header in enumerate(headers):
            if header in name_header:
                return index

        return None

    # export_to_html - выгружает все данные в html файл
    def export_to_html(self, fname='output.html'):
        # Инициализируем начальную часть HTML-документа
        self.result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''

        # Перебираем все элементы в списке self.data
        for row_index, product_info in enumerate(self.data):
            # Добавляем строку данных в таблицу
            self.result += f'''
                        <tr>
                            <td>{row_index + 1}</td>
                            <td>{product_info['product_name']}</td>
                            <td>{product_info['price']}</td>
                            <td>{product_info['weight']}</td>
                            <td>{product_info['file_name']}</td>
                            <td>{product_info['price_per_kg']}</td>
                        </tr>
                    '''

        self.result += '''
            </table>
        </body>
        </html>
        '''

        with open(fname, 'w', encoding='utf-8') as f:
            f.write(self.result)

        print(f"Данные успешно экспортированы в {fname}")

    # получает текст и возвращает список позиций, содержащий этот текст в названии продукта.
    def find_text(self, text):
        results = []

        # Перебираем все элементы в списке self.data
        for product_name in self.data:
            if text.lower() in product_name['product_name'].lower():
                results.append(product_name)

        # Сортируем результаты по цене за килограмм
        results.sort(key=lambda x: x['price_per_kg'])

        return results


pm = PriceMachine()
print(pm.load_prices())

'''
    Логика работы программы
'''

while True:
    user_input = input("Введите текст для поиска или 'exit' для выхода: ")

    if user_input.lower() == 'exit':
        print("Работа закончена")
        break

    else:
        results = pm.find_text(user_input)

        if results:
            print(f"Найденные позиции для '{user_input}':")

            for row_index, product_info in enumerate(results):
                print(f"{row_index + 1} "
                      f"{product_info['product_name']} "
                      f"{product_info['price']} "
                      f"{product_info['weight']} "
                      f"{product_info['file_name']} "
                      f"{product_info['price_per_kg']}")
        else:
            print(f"Ничего не найдено для '{user_input}'")

print('the end')
print(pm.export_to_html())
