class Player:
    def __init__(self):
        self.__number = "default"
        self.__name = "default"
        self.__symbol = "default"
        self.__color = "default"
        self.__wins = 0

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value):
        self.__number = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def symbol(self):
        return self.__symbol

    @symbol.setter
    def symbol(self, value):
        self.__symbol = value

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value

    @property
    def wins(self):
        return self.__wins

    @wins.setter
    def wins(self, increment):
        self.__wins += increment

