import random
def display_board():
    # Funkcja, ktora przyjmuje jeden parametr zawierajacy biezacy stan tablicy
    # i wyswietla go w oknie konsoli.
    v1, v2, v3, v4, v5, v6, v7, v8, v9 = new_list[0], new_list[1], new_list[2], new_list[3], new_list[4], new_list[5], new_list[6], new_list[7], new_list[8]

    board = """
            +-------+-------+-------+
            |       |       |       |
            |   {0}   |   {1}   |   {2}   |
            |       |       |       |
            +-------+-------+-------+
            |       |       |       |
            |   {3}   |   {4}   |   {5}   |
            |       |       |       |
            +-------+-------+-------+
            |       |       |       |
            |   {6}   |   {7}   |   {8}   |
            |       |       |       |
            +-------+-------+-------+
        """.format(v1, v2, v3, v4, v5, v6, v7, v8, v9)
    print(board)
    
def enter_move():
    # Funkcja, ktora przyjmuje parametr odzwierciedlajacy biezacy stan tablicy,
    # prosi uzytkownika o wykonanie ruchu, 
    # sprawdza dane wejsciowe i aktualizuje tablice zgodnie z decyzja uzytkownika.
    global v1, v2, v3, v4, v5, v6, v7, v8, v9
    while True:
        x = int(input('Wprowadź liczbę od 0 do 10: '))
        if x > 0 and x < 10:
            if new_list[x - 1] == x:
                new_list[x - 1] = 'O'
                return new_list[x - 1]
        
def make_list_of_free_fields():
    # Funkcja, ktora przeglada tablice i tworzy liste wszystkich wolnych pol; 
    # lista sklada sie z krotek, a kazda krotka zawiera pare liczb odzwierciedlajacych rzad i kolumne.
    free_fields = [i for i in new_list if i != 'O' and i != 'X']
    return free_fields
def victory_for(free_fields):
    # Funkcja, ktora dokonuje analizy stanu tablicy w celu sprawdzenia
    # czy uzytkownik/gracz stosujacy "O" lub "X" wygral rozgrywke.
    koniec = 0
    result = 0
    v1, v2, v3, v4, v5, v6, v7, v8, v9 = new_list[0], new_list[1], new_list[2], new_list[3], new_list[4], new_list[5], new_list[6], new_list[7], new_list[8]
    if (v1 == 'O' and v2  == 'O' and v3 == 'O') or (v4  == 'O' and v5  == 'O' and v6 == 'O') or (v7  == 'O' and v8  == 'O' and v9 == 'O') or (v1  == 'O' and v5  == 'O' and v9 == 'O') or (v3  == 'O' and v5  == 'O' and v7 == 'O') or (v1  == 'O' and v4  == 'O' and v7 == 'O') or (v2  == 'O' and v5  == 'O' and v8 == 'O') or (v3 == 'O' and v6 == 'O' and v9 == 'O'):
        koniec += 1
        result = 1
        return result, koniec
    elif (v1 == 'X' and v2  == 'X' and v3 == 'X') or (v4  == 'X' and v5  == 'X' and v6 == 'X') or (v7  == 'X' and v8  == 'X' and v9 == 'X') or (v1  == 'X' and v5  == 'X' and v9 == 'X') or (v3  == 'X' and v5  == 'X' and v7 == 'X') or (v1  == 'X' and v4  == 'X' and v7 == 'X') or (v2  == 'X' and v5  == 'X' and v8 == 'X') or (v3 == 'X' and v6 == 'X' and v9 == 'X'):
        koniec += 1
        result = 2
        return result, koniec
    else:
        if len(free_fields) == 0:
            koniec += 1
            result = 3
            return result, koniec
    return result, koniec
def draw_move(free_fields):
    # Funkcja, ktora wykonuje ruch za komputer i aktualizuje tablice.
    x = random.choice(free_fields)
    new_list[x - 1] = 'X'

new_list = [1,2,3,4,'X',6,7,8,9]

while True:
    display_board()
    x = enter_move()
    display_board()
    free_fields = make_list_of_free_fields()
    draw_move(free_fields)
    result, koniec = victory_for(free_fields)
    if koniec == 1:
        break
if result == 1:
    print('Człowiek wygrałeś')
elif result == 2:
    print('Kąkuter wygrałeś')
else:
    print('Remisik')