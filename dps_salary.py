def main():
    salary = calculate_salary()
    print(salary)


def calculate_salary():
    """
    Считает зарплату сотрудника ДПС, считывая исходные данные с клавиатуры.

    :returns: зарплата сотрудника
    """
    sum_of_fines = 0
    speed_of_car, number_of_car = read_data()
    while not detect_chief(number_of_car):
        if speed_of_car > 60:
            sum_of_fines += calculate_fine(number_of_car)
        speed_of_car, number_of_car = read_data()
    return sum_of_fines


def read_data():
    """
    Считывает следущую строку данных.

    :returns: tuple(int, str) - скорость, номер машины
    """
    data = input().split()
    return int(data[0]), data[1]


def detect_chief(number_of_car):
    """
    Проверяет, принадлежит ли данный номер начальнику.

    :param number_of_car: номер автомобиля
    :returns: True, если номер принадлежит начальнику, иначе False
    """
    return number_of_car == "A999AA"


def calculate_fine(number_of_car):
    """
    Считает штраф для автомобиля с конкретным номером.

    :param number_of_car: номер автомобиля
    :returns: Целое число, размер штрафа
    """
    if is_super_number(number_of_car):
        return 1000
    elif is_good_number(number_of_car):
        return 500
    else:
        return 100


def is_super_number(number_of_car):
    """
    Проверяет, является ли номер «крутым» (совпадение трёх цифр)

    :param number_of_car: номер автомобиля
    :returns: True, если номер «крутой», иначе False
    """
    return number_of_car[1] == number_of_car[2] == number_of_car[3]


def is_good_number(number_of_car):
    """
    Проверяет, является ли номер «хорошим» (совпадение двух цифр)

    :param number_of_car: номер автомобиля
    :returns: True, если номер «хороший», иначе False
    """
    return number_of_car[1] == number_of_car[2] or \
           number_of_car[1] == number_of_car[3] or \
           number_of_car[2] == number_of_car[3]


if __name__ == "__main__":
    main()
