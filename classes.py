class Actor:
    def __init__(self, id, cost, groups):
        self.id = id
        self.cost = cost
        self.groups = groups

    def __str__(self):
        return "Actor[{}] with cost {}, groups {}".format(self.id,self.cost,self.groups)

    def __repr__(self):
        return "Actor[{}] with cost {}, groups {}".format(self.id,self.cost,self.groups)


    