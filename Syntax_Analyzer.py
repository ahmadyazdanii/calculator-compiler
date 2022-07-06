from argparse import ArgumentError
from Lexical_Analyzer import Tokenizer
from os import path
import sys

class Syntax_Analyzer:
    def __init__(self, tokens_list):
        self.commands = tokens_list
        self.variables = {}

    @property
    def commands(self):
        return self.__commands

    @commands.setter
    def commands(self, value):
        if isinstance(value, list):
            temp_list = []
            self.__commands = []
            for token in value:
                if token.type not in ["EOF", "NEW_LINE"]:
                    temp_list.append(token)
                else:
                    if len(temp_list) != 0:
                        self.__commands.append(temp_list)
                        temp_list = []
        else:
            raise TypeError("Tokens_list must be list")

    def run(self):
        for command in self.commands:
            self.tokens = iter(command)
            
            token = next(self.tokens)
            if token.type == "ID":
                token_layer_1 = next(self.tokens)
                if token_layer_1.type == "ASSIGN":
                    self.variables[token.value], op = self.cal_1(next(self.tokens))
                else:
                    raise SyntaxError("assign is missing")
            elif token.type == "PRINT":
                total_number, op = self.cal_1(next(self.tokens))
                print(total_number)
            else:
                raise SyntaxError("Invalid input")

    def cal_1(self, base_token):
        num_1, op = self.cal_2(base_token)
        if op is not None:
            while op.type in ["PLUS", "MINUS"]:
                op_ex = op
                num_2, op = self.cal_2(next(self.tokens))
                if op_ex.type == "PLUS":
                    num_1 += num_2
                else:
                    num_1 -= num_2
                if op is None:
                    break
        return num_1, op

    def cal_2(self, base_token):
        num_1, op = self.cal_3(base_token)
        if op is not None:
            while op.type in ["MUL"]:
                op_ex = op
                num_2, op = self.cal_3(next(self.tokens))
                if op_ex.type == "POW":
                    num_1 = pow(num_1, num_2)
                else:
                    num_1 *= num_2
                if op is None:
                    break
        return num_1, op
        
    def cal_3(self, base_token):
        num_1, op = self.cal_4(base_token)
        if op is not None:
            while op.type in ["POW"]:
                op_ex = op
                num_2, op = self.cal_4(next(self.tokens))
                if op_ex.type == "POW":
                    num_1 = pow(num_1, num_2)
                else:
                    num_1 *= num_2
                if op is None:
                    break
        return num_1, op

    def cal_4(self, base_token):
        try:
            num_1 = 0
            var = base_token
            if var.type == "NUM":
                num_1 = var.value
            elif var.type == "MINUS":
                next_var = next(self.tokens)
                if next_var.type == "NUM":
                    num_1 = next_var.value * -1
                elif next_var.type == "ID":
                    try:
                        num_1 = self.variables[next_var.value] * -1
                    except KeyError:
                        raise SyntaxError("{} is not declared in variables".format(next_var.value))
            elif var.type == "ID":
                try:
                    num_1 = self.variables[var.value]
                except KeyError:
                    raise SyntaxError("{} is not declared in variables".format(var.value))
            elif var.type == "OPEN_BRACKET":
                num_1, op_next = self.cal_1(next(self.tokens))
                if op_next and op_next.type != "CLOSE_BRACKET":
                    raise SyntaxError("close bracket is missing")
            else:
                raise SyntaxError("Invalid input")
            next_token = next(self.tokens)
        except StopIteration:
            next_token = None
        return num_1, next_token


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if path.isfile(file_path):
            tokenizer = Tokenizer(file_path)
            Syntax_Analyzer(tokenizer.get_tokens()).run()
        else:
            raise FileExistsError("File does not exist !")
    else:
        raise ArgumentError(None, "File path must set in first position of arguments !")