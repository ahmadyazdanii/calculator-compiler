from os import path
from re import match

token_types = {
    'NUM',
    'ASSIGN',
    'MUL',
    'PLUS',
    'POW',
    'MINUS',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',
    'ID',
    'PRINT',
    'NEW_LINE',
    'EOF'}

class Token:
    __tokens = {}
    
    def __new__(cls, type, value):
        key = (type, value)
        if key not in cls.__tokens:
            obj = super().__new__(cls)
            obj.type = type
            obj.value = value
            cls.__tokens[key] = obj
        return cls.__tokens[key]

    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        return self.__value

    @type.setter
    def type(self, value):
        if value in token_types:
            self.__type = value
        else:
            raise ValueError("Token type must be in {}".format(token_types))

    @value.setter
    def value(self, value):
        self.__value = value
    
    def __repr__(self):
        return "({}, {})".format(self.type, self.value)

class Tokenizer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tokens = []

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, value):
        if isinstance(value, str):
            if path.isfile(value):
                self.__file_path = value
            else:
                raise FileExistsError("The {} not found".format(value))
        else:
            raise TypeError("file_path's type must be string")

    def fetch_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as FILE:
            file_content = FILE.read()
        return file_content

    def __generate_tokens(self):
        file_content = self.fetch_file()
        self.tokens = []
        index = 0
        
        while index < len(file_content):
            char = file_content[index]
            if char == "+":
                self.tokens.append(Token("PLUS", char))
            elif char == "-":
                self.tokens.append(Token("MINUS", char))
            elif char == "*":
                self.tokens.append(Token("MUL", char))
            elif char == "^":
                self.tokens.append(Token("POW", char))
            elif char == "=":
                self.tokens.append(Token("ASSIGN", char))
            elif char == "(":
                self.tokens.append(Token("OPEN_BRACKET", char))
            elif char == ")":
                self.tokens.append(Token("CLOSE_BRACKET", char))
            elif char == "\n":
                new_line_match = match(r'\n+', file_content[index:])
                self.tokens.append(Token("NEW_LINE", '\\n'))
                index += new_line_match.end() - 1
            elif match(r'[0-9]', char):
                number_match = match(r'[0-9]+(\.[0-9]+)?', file_content[index:])
                self.tokens.append(Token("NUM", float(number_match.group())))
                index += number_match.end() - 1
            elif match(r'[a-zA-Z]', char):
                print_match = match(r'print\s+', file_content[index:])
                if print_match:
                    self.tokens.append(Token("PRINT", print_match.group()))
                    index += print_match.end() - 1
                else:
                    id_match = match(r'[a-zA-Z]+(\w+)?', file_content[index:])
                    self.tokens.append(Token("ID", id_match.group()))
                    index += id_match.end() - 1
            else:
                if match(r'[\t\s]', char):
                    ignore_match = match(r'[\t\s]+', file_content[index:])
                    index += ignore_match.end() - 1
                else:
                    raise ValueError("The '{}' in index '{}' is invalid charecter".format(char, index))
            index += 1
        if(self.tokens[-1].type == "NEW_LINE"):
            self.tokens[-1] = Token("EOF", "EOF")
        else:
            self.tokens.append(Token("EOF", "EOF"))

    def get_tokens(self, generate_tokens_anytime=False):
        if generate_tokens_anytime:
            self.__generate_tokens()
        else:
            if len(self.tokens) == 0:
                self.__generate_tokens()
        return self.tokens

if __name__ == "__main__":
    t = Tokenizer("./cal.txt")
    print(t.get_tokens())