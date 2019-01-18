# 1. Объявление возможных типов событий
QUEST_SPEAK, QUEST_HUNT, QUEST_CARRY = "QSPEAK", "QHUNT", "QCARRY"

# 2. Описание персонажа
# Опишем персонажа, который будет взаимодействовать с цепочкой обязанностей

class Character:
    def __init__(self):
        self.name = "Nagibator"
        self.xp = 0
        self.passed_quests = set()
        self.taken_quests = set()

# 3. Опишем класс события
# При возникновении определенного события запускается цепочка обязанностей, которая может это событие обрабатывать.

class Event:
    def __init__(self, kind):
        self.kind = kind

# 4. Опишем базовое звено цепочки обязанностей
# Элементарный обработчик просто передает событие следующему звену цепочки, если таковое имеется.

class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, char, event):
        if self.__successor is not None:
            self.__successor.handle(char, event)

# 5. Опишем обработчики квестов
# Для каждого квеста напишем обработчик и определим событие, при котором этот обработчик будет срабатывать.

class HandleQSpeak(NullHandler):
    def handle(self, char, event):
        if event.kind == QUEST_SPEAK:
            xp = 100
            quest_name = "Поговорить с фермером"
            if event.kind not in (char.passed_quests | char.taken_quests):
                print(f"Квест получен: \"{quest_name}\"")
                char.taken_quests.add(event.kind)
            elif event.kind in char.taken_quests:
                print(f"Квест сдан: \"{quest_name}\"")
                char.passed_quests.add(event.kind)
                char.taken_quests.remove(event.kind)
                char.xp += xp
        else:
            print("Передаю обработку дальше")
            super().handle(char, event)


class HandleQHunt(NullHandler):
    def handle(self, char, event):
        if event.kind == QUEST_HUNT:
            xp = 300
            quest_name = "Охота на крыс"
            if event.kind not in (char.passed_quests | char.taken_quests):
                print(f"Квест получен: \"{quest_name}\"")
                char.taken_quests.add(event.kind)
            elif event.kind in char.taken_quests:
                print(f"Квест сдан: \"{quest_name}\"")
                char.passed_quests.add(event.kind)
                char.taken_quests.remove(event.kind)
                char.xp += xp
        else:
            print("Передаю обработку дальше")
            super().handle(char, event)


class HandleQCarry(NullHandler):
    def handle(self, char, event):
        if event.kind == QUEST_CARRY:
            xp = 200
            quest_name = "Принести дрова из сарая"
            if event.kind not in (char.passed_quests | char.taken_quests):
                print(f"Квест получен: \"{quest_name}\"")
                char.taken_quests.add(event.kind)
            elif event.kind in char.taken_quests:
                print(f"Квест сдан: \"{quest_name}\"")
                char.passed_quests.add(event.kind)
                char.taken_quests.remove(event.kind)
                char.xp += xp
        else:
            print("Передаю обработку дальше")
            super().handle(char, event)

# 6. Опишем квестгивера
# Квестгивер будет хранить цепочку обработчиков и список событий, на которые он может реагировать. Список событий можно пополнять.
# Метод handle_quests генерирует все доступные события и передает их на обработку цепочке.

class QuestGiver:
    def __init__(self):
        self.handlers = HandleQSpeak(HandleQHunt(HandleQCarry(NullHandler())))
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def handle_quests(self, char):
        for event in self.events:
            self.handlers.handle(char, event)

# 7. Создадим квестгивера и дадим ему все возможные события

events = [Event(QUEST_CARRY), Event(QUEST_HUNT), Event(QUEST_SPEAK)]

quest_giver = QuestGiver()

for event in events:
    quest_giver.add_event(event)

# 8. Проверим работы цепочки обязанностейй на примере, аналогичном предыдущему

player = Character()

quest_giver.handle_quests(player)
print()
player.taken_quests = {QUEST_CARRY, QUEST_SPEAK}
quest_giver.handle_quests(player)
print()
quest_giver.handle_quests(player)

# Видно, что цепочка обязанностей работает, и квесты, обработка которых невозможна на данном этапе, передаются по ней дальше
