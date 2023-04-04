#Class token to show its information
class Token:
    def __init__(self, _name="", _type="") -> None:
        self.name = _name
        self.type = _type
    def print_token(self):
        print("<",self.name,",",self.type,">")

    