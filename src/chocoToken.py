#Class token to show its information
class Token:
    def __init__(self, _name="", _type="") -> None:
        self.name = _name
        self.type = _type
        self.line = 0
        self.column = 0
    def set_info(self,_name="",_type="",_line=0,_column=0):
        self.name = _name
        self.type = _type
        self.line = _line
        self.column = _column
    def print_token(self):
        space_occupied = len(self.name + self.type)
        spaces_to_align = " "*max(0,20-space_occupied)
        print("DEBUG SCAN - <",self.name,",",self.type,">",spaces_to_align, "FOUND AT (",self.line+1,":",self.column,")")

    