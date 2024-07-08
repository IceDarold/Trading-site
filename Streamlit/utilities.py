import os

def get_tickers() -> list[str]:
    # Список для хранения имен файлов
    filenames = []
    
    # Проход по всем файлам в указанной директории
    for filename in os.listdir("Data"):
        # Проверка, что файл имеет расширение .csv
        if filename.endswith('.csv'):
            # Добавление имени файла без расширения в список
            filenames.append(os.path.splitext(filename)[0])
    
    return filenames

print(get_tickers())