from csv import reader
from reciepts.models import Ingridients

# импорт csv без строки заголовков

with open('ingredients.csv', 'r', encoding='utf-8-sig') as f:
    csv_reader = reader(f)
    for row in csv_reader:
        Ingridients.objects.get_or_create(
            ingridient=row[0], 
            measure=row[1]
        )