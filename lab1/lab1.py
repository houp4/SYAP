import pandas as pd
import numpy as np
import random
import os
from concurrent.futures import ProcessPoolExecutor as Pool

def create_csv_file(i):
    filename = f'file_{i}.csv'
    data = []
    for _ in range(50): 
        category = random.choice(['A', 'B', 'C', 'D'])
        value = round(random.uniform(1.0, 100.0), 2)
        data.append([category, value])
    df = pd.DataFrame(data, columns=['Category', 'Value'])
    df.to_csv(filename, index=False)
    return filename

def process_file(filename):
    df = pd.read_csv(filename)
    result = []
    for letter in ['A', 'B', 'C', 'D']:
        values = df[df['Category'] == letter]['Value']
        if len(values) > 0:
            median = np.median(values)
            std = np.std(values)
            result.append([letter, round(median, 2), round(std, 2)])
    return result

def main():
    filenames = []
    for i in range(5):
        filename = create_csv_file(i)
        filenames.append(filename)


    all_results = list(Pool.map(process_file, filenames))
    
    print("Результаты по файлам:")
    for i, result in enumerate(all_results):
        print(f"Файл {i}:")
        for row in result:
            print(f"{row[0]}: медиана={row[1]}, отклонение={row[2]}")
    
    print("\nОбщиий результат:")
    letter_medians = {'A': [], 'B': [], 'C': [], 'D': []}
    
    for file_result in all_results:
        for letter, median, std in file_result:
            letter_medians[letter].append(median)
    
    final_result = []
    for letter in ['A', 'B', 'C', 'D']:
        medians = letter_medians[letter]
        if medians:
            median_of_medians = np.median(medians)
            std_of_medians = np.std(medians)
            final_result.append([letter, round(median_of_medians, 2), round(std_of_medians, 2)])

    for row in final_result:
        print(f"{row[0]}: медиана={row[1]}, отклонение={row[2]}")
    
    # for filename in filenames:
    #     os.remove(filename)

if __name__ == "__main__":
    main()