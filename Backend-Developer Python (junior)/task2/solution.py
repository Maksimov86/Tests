import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_animal_counts():
    url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    base_url = "https://ru.wikipedia.org"
    
    # Инициализация словаря для подсчёта животных
    animal_counts = {chr(i): 0 for i in range(ord('А'), ord('Я') + 1)}
    
    while url:
        # Загружаем страницу
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем все записи на текущей странице
        for link in soup.select('.mw-category-group ul li a'):
            name = link.text.strip()
            if name:  # Проверяем, что строка не пустая
                first_letter = name[0].upper()
                if first_letter in animal_counts:
                    animal_counts[first_letter] += 1
        
        # Проверяем ссылку на следующую страницу
        next_page = soup.find('a', text="Следующая страница")
        url = base_url + next_page['href'] if next_page else None
    
    return animal_counts


def save_to_csv(data, filename="beasts.csv"):
    # Преобразуем данные в DataFrame
    df = pd.DataFrame(data.items(), columns=["Letter", "Count"])
    df.to_csv(filename, index=False, header=False, encoding="utf-8")

def main():
    print("Fetching animal counts from Wikipedia...")
    animal_counts = fetch_animal_counts()
    print("Saving results to beasts.csv...")
    save_to_csv(animal_counts)
    print("Done!")

if __name__ == "__main__":
    main()
