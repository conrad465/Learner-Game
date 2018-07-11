import os
import Net
import pickle
class Doggo():
    def __init__(self, n, s):
        self.sound = s
        self.name = n
        self.tricks = {"wag" : self.wag, "speak":self.speak, "dance":self.dance}

    def speak(self):
        print (self.name + " goes " + self.sound)

    def wag(self):
        print(self.name + " wag* wag* wag* wag*")

    def dance(self):
        print(self.name + " jumps*")

    def command(self, command):
        self.decider.respond(command)

    def respond(self, order):
        if self.name in order:
            tasks = {command : action for command, action in self.tricks.items() if command in order}
            for trick in tasks.values():
                trick()


dogs = [Doggo("Arfy", "wuff"), Doggo("Abe","raarhherrr"), Doggo("Blue","_____")]


def issue_command(command):
    for dog in dogs:
        dog.respond(command)


#issue_command("Blue speak")

path = os.path.dirname(os.path.abspath(__file__))
#
# for file in os.listdir(path + "/old_generations/" + gen):
#     print(file)
def hello():
    print("hello")

a = hello
b = hello

a()
n = Net.Net([10] , 10,[a,b])
pickle.dump( n, open( "save.p", "wb" ) )
