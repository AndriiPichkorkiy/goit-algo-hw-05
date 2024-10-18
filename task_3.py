from pathlib import Path
import timeit

# Підготовка данних
articles = []
assets = Path("assets")
for child in assets.iterdir():
    articles.append(Path(child).read_text(encoding="UTF-8"))

# Алгоритм Кнута-Морріса-Пратта


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

# Алгоритм Боєра-Мура


def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1


# Алгоритм Рабіна-Карпа
def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)

    # Базове число для хешування та модуль
    base = 256
    modulus = 101

    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(
        main_string[:substring_length], base, modulus)

    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus

    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash -
                                  ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (
                current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


# Функція для виводу результатів

def print_result(list_type: str, list_times: list[tuple[str, float]]) -> None:
    def get_time(element):
        return element[1]
    list_times.sort(key=get_time, reverse=True)

    print(f"{list_type}:")
    for x in list_times:
        print(
            f"Пошук {x[0]:<20} займає: {x[1]:<25} секунд")

    dif_1 = round(list_times[0][1] / list_times[2][1] * 100, 2)
    dif_2 = round(list_times[1][1] / list_times[2][1] * 100, 2)
    print(
        f"Алгоритм {list_times[2][0]} швидший на {dif_1}% за алгоритм {list_times[0][0]} та швидший на {dif_2}% за алгоритм {list_times[1][0]}", end="\n\n")


algoritms = {
    "Кнута-Морріса-Пратта": kmp_search,
    "Боєра-Мура": boyer_moore_search,
    "Рабіна-Карпа": rabin_karp_search,
}

time_number_executions = 500

# визначення часу для короткого існуючого слова
short_pattern = "результат"
short_results_article_1 = []
short_results_article_2 = []
short_results_total = []


for alg in algoritms:
    results_article_1 = timeit.timeit(
        lambda: algoritms[alg](articles[0], short_pattern), number=time_number_executions)
    results_article_2 = timeit.timeit(
        lambda: algoritms[alg](articles[1], short_pattern), number=time_number_executions)
    results_total = results_article_1 + results_article_2

    short_results_article_1.append([alg, results_article_1])
    short_results_article_2.append([alg, results_article_2])
    short_results_total.append([alg, results_total])

print("<====> Визначення часу для короткого існуючого слова <====>")
print_result("Стаття 1",
             short_results_article_1)
print_result("Стаття 2",
             short_results_article_2)
print_result("Загалом",
             short_results_total)


# визначення часу для довгого існуючого слова
long_pattern_1 = "1. Вікіпедія GPGPU [Електронний ресурс]. Режим доступу до ресурсу: https://uk.wikipedia.org/wiki/GPGPU – Назва з екрану. Зачем программисту изучать алгоритмы. Tproger [Електронний ресурс] – Режим доступу до ресурсу: https://tproger.ru/articles/why-learn-algorithms/ "
long_pattern_2 = "8. Meleshko Ye. Computer model of virtual social network with recommendation system. Scientific journal Innovative Technologies and Scientific Solutions for Industries, Kharkiv, NURE. 2019. Issue 2(8). P. 80 "
long_results_article_1 = []
long_results_article_2 = []
long_results_total = []

for alg in algoritms:
    results_article_1 = timeit.timeit(
        lambda: algoritms[alg](articles[0], long_pattern_1), number=time_number_executions)
    results_article_2 = timeit.timeit(
        lambda: algoritms[alg](articles[1], long_pattern_2), number=time_number_executions)
    results_total = results_article_1 + results_article_2

    long_results_article_1.append([alg, results_article_1])
    long_results_article_2.append([alg, results_article_2])
    long_results_total.append([alg, results_total])

print("<====> Визначення часу для довгого існуючого слова <====>")
print_result("Стаття 1",
             long_results_article_1)
print_result("Стаття 2",
             long_results_article_2)
print_result("Загалом",
             long_results_total)

# визначення часу для не існуючого слова
non_existent_pattern = "Теоре́ма Піфаго́ра (Пітаго́ра[1]) — одна із засадничих теорем евклідової геометрії, яка встановлює співвідношення між сторонами прямокутного трикутника. Уважається, що її довів грецький математик Піфагор, на чию честь її й названо (є й інші версії, зокрема думка, що цю теорему в загальному вигляді було сформульовано математиком-піфагорійцем Гіппасом)."

non_existent_results_article_1 = []
non_existent_results_article_2 = []
non_existent_results_total = []

for alg in algoritms:
    results_article_1 = timeit.timeit(
        lambda: algoritms[alg](articles[0], non_existent_pattern), number=time_number_executions)
    results_article_2 = timeit.timeit(
        lambda: algoritms[alg](articles[1], non_existent_pattern), number=time_number_executions)
    results_total = results_article_1 + results_article_2

    non_existent_results_article_1.append([alg, results_article_1])
    non_existent_results_article_2.append([alg, results_article_2])
    non_existent_results_total.append([alg, results_total])

print("<====> Визначення часу для не існуючого слова <====>")
print_result("Стаття 1",
             long_results_article_1)
print_result("Стаття 2",
             long_results_article_2)
print_result("Загалом",
             long_results_total)
