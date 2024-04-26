import copy

class Person:
    def __init__(self):
        self.health = 100
        children1 = "test"
        children2 = "test"
        self.children = [children1, children2]

    def decrease_health(self):
        self.health -= 10

    def kill_children(self):
        self.children[:] = [child for child in self.children if False]

persons = []
for i in range(2):
    persons.append(Person())

# Method 1 of copying
persons_copy = []
persons_copy[:] = [person for person in persons]

# Method 2 of copying
persons_copy2 = []
persons_copy2 = copy.deepcopy(persons)

for person in persons_copy:
    person.kill_children()
    pass

for person in persons_copy:
    person.health = 0

for person in persons:
    print(f"persons health = {person.health} children")
    print(person.children)

print("persons_copy children")
for person in persons_copy:
    print(f"persons health = {person.health} children")
    print(person.children)

print("persons_copy2 children")
for person in persons_copy2:
    print(f"persons health = {person.health} children")
    print(person.children)