import os

def get_tickers() -> list[str]:
    # Список для хранения имен файлов
    filenames = []
    
    # Проход по всем файлам в указанной директории
    for filename in os.listdir("Data"):
        # Проверка, что файл имеет расширение .csv
        if filename.endswith('.csv'):
            with open("Data/" + filename, "r") as f:
                columns = f.readline()[:-1].split(",")
                if "Date" in columns and "Close" in columns:
                    # Добавление имени файла без расширения в список
                    filenames.append(os.path.splitext(filename)[0])
                else:
                    print("Отсутствует колонка Date или Close")
    
    return filenames
