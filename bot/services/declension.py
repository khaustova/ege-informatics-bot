def get_assignment_word(n: int) -> str:
    """
    Возвращает склонение слова "задание" в зависимости от количества
    """
    
    n %= 100
    ind = 0
    if n >= 5 and n <= 20:
        ind = 0
        
    n %= 10
    if n == 1:
        ind = 1
    elif n >= 2 and n <= 4:
        ind = 2
    else:
        ind = 0
    
    pairs = {
        0: 'заданий',
        1: 'задание',
        2: 'задания'
    }
    
    return pairs[ind]