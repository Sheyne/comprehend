def isspecial(s):
    return (s.startswith("@")
        or "?" in s
        or "*" in s)

class Graph(object):
    def __init__(self):
        self.d = {}
    def __getitem__(self, key):
        if isspecial(key):
            return self.d[key]
        else:
            return key
    def __setitem__(self, key, value):
        self.d[key] = value
    def __delitem__(self, key):
        pass    
    
g = Graph()
g["Hi?"] = "blue"
print g["Hi?"]