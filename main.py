from random import sample
from collections import defaultdict

def define_card(new_card):
    eq = set()
    for item in new_card:
        eq |= set(item)
    new_card = eq - {'#', '-'}
    return new_card


class Card:
    def __init__(self):
        self.card = None
        self.create()

    def create(self):
        self.card = sorted(sample(list(range(1, 100)), k=15))
        app = defaultdict(list)
        for item in self.card:
            app[item // 10].append(item)
        for i in range(10):
            if len(app[i]) > 3:
                k = len(app[i]) - 3
                app[i] = app[i][:3]
                j = 1
                bag = set(app[(i + j) % 10]) - set('#')
                while len(bag) >= 3:
                    j += 1
                    bag = set(app[(i + j) % 10]) - set('#')
                new_set = list(set(range(((i + j) * 10) % 100, ((i + j + 1) * 10) % 101)) - bag)
                app[(i + j) % 10] = list(set(app[(i + j) % 10]) - set('#')) + sample(new_set, k=k)
                k = 3 - len(app[(i + j) % 10])
                app[(i + j) % 10] += ['#'] * k
            elif len(app[i]) < 3:
                k = 3 - len(app[i])
                app[i] += ['#'] * k
        result = []
        for i in range(3):
            result.append([app[key][i] for key in range(10)])
        self.card = result

    @property
    def is_empty(self):
        return len(define_card(self.card)) == 0

    def is_num_to_card(self, num):
        return any([item.count(num) for item in self.card])

    def cross_out(self, num):
        for item in self.card:
            try:
                index = item.index(num)
                item[index] = '-'
                break
            except ValueError:
                pass

    def out_print(self):
        s = ' ' + '_' * 30 + '\n'
        for item in self.card:
            s += '|'
            for char in item:
                s += f'{str(char):^3}'
            s += '|\n'
        s += ' ' + '-' * 30 + '\n'
        return s


class Comp:
    def __init__(self):
        self.card = Card()
        self.name = input('Введите имя игрока: ')
        print(f'Имя игрока: {self.name}')

    def step(self, num):
        print(self.card.out_print())
        if self.card.is_num_to_card(num):
            self.card.cross_out(num)
            print('Номер есть')
        else:
            print('Номера нет в карточке')
        return True


class Human:
    def __init__(self):
        self.card = Card()
        self.name = input('Введите имя игрока: ')
        print(f'Имя игрока: {self.name}')

    def step(self, num):
        print(self.card.out_print())
        ans = input('Зачеркнуть цифру (Д/Н)? ')
        while ans not in 'ДдНн':
            ans = input('Некорректный ввод. Зачеркнуть цифру (Д/Н)? ')
        if ans in 'Дд':
            if self.card.is_num_to_card(num):
                self.card.cross_out(num)
                return True
            else:
                return False
        else:
            if self.card.is_num_to_card(num):
                return False
            else:
                return True


class Game:
    bag = list(range(1, 100))

    def __init__(self):
        self.player1 = None
        self.player2 = None

    def menu(self):
        mtext = """      
        1. Один игрок с компьютером
        2. 2 игрока
        3. 2 Компьютера
        4. Выход
        """
        print(mtext)
        n = input('Введите номер пункта: ')
        while n not in '1234':
            n = input('Некорректный ввод. Введите номер пункта: ')
        return int(n)

    def start(self):
        n = self.menu()
        if n == 1:
            self.player1 = Human()
            self.player2 = Comp()
        elif n == 2:
            self.player1 = Human()
            self.player2 = Human()
        elif n == 3:
            self.player1 = Comp()
            self.player2 = Comp()
        else:
            print('Выбран выход')
            return None
        num = sample(self.bag, k=1)
        print(f'Выпал бочонок: {num[0]}')
        self.bag.remove(num[0])
        while not (self.player1.card.is_empty or self.player2.card.is_empty):
            step1 = self.player1.step(num[0])
            step2 = self.player2.step(num[0])
            if not step1 or not step2:
                break
            num = sample(self.bag, k=1)
            print(f'Выпал бочонок: {num[0]}')
            self.bag.remove(num[0])
        if self.player1.card.is_empty or not step1:
            loser = self.player1
            winner = self.player2
        else:
            loser = self.player1
            winner = self.player2
        print(winner.name, 'выиграл')
        print(loser.name, 'не выиграл')


if __name__ == '__main__':
    game = Game()
    game.start()