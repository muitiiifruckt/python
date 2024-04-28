class Robot:
    def __init__(self,name,color,weight,company):
        self.name = name
        self.color = color
        self.weight = weight
        self.company = company
    def __repr__(self):
        return (f"name {self.name} , color {self.color}, weight {self.weight}, company {self.company}")
class Student:
    def __init__(self,name,course,group,college):
        self.name = name
        self.college = college
        self.course = course
        self.group = group
    def __repr__(self):
        return (f"name {self.name} , course {self.course}, group {self.group}, college {self.college}")
    def show(self):
        return (f"name {self.name} , course {self.course}, group {self.group}, college {self.college}")


Robot_1 = Robot("tom","red","30","Alfa")
Robot_2 = Robot("jemmy","blue","45","google")
Robot_3 = Robot("orbit","yellow","10","Waes")
Aizat_Murtazi2n = Student("Aiz1at","9","09-141","KPFU")
Aizat_Murtazi1n = Student("Ai2zat","9","09-141","KPFU")
Aizat_Murtazi3n = Student("Aiza1t","9","09-141","KPFU")
print(Robot_1)
print(Aizat_Murtazi3n.show())