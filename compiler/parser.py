from os.path import dirname
from shutil import copy
from lark import Lark, Transformer
from constants import GRAMMAR

def rreplace(s, old, new):
    li = s.rsplit(old, 1) #Split only once
    return new.join(li)


includes = []


class PeriwinkleTree(Transformer):
    def __init__(self, path):
        super().__init__()
        self.directory = dirname(path)

    def import_(self, values):
        path = values[0].replace("\"", "")
        return compile_file(self.directory + "/" + path)

    def foreign_variable(self, values):
        return values[0] + "&"

    def include(self, values):
        basename = values[0].replace("\"", "")
        path = self.directory + "/" + basename
        copy(path, "out/include/external/" + basename)
        return "include \"external/" + basename + "\";"
        # return compile_file(self.directory + path)

    def all(self, values):
        return str(values[0])
            
    def start(self, values):
        return str('\n'.join(values))

    def block(self, values):
        return str('\n'.join(values))

    def integer(self, values):
        return str(values[0])

    def decimal(self, values):
        return str(values[0])

    def obj(self, values):
        return "Object()"

    def string(self, values):
        return str(values[0])

    def true(self, values):
        return "true"

    def false(self, values):
        return "false"

    def variable(self, values):
        return str(values[0])

    def identifier(self, values):
        return "" + str(values[0])

    def wrapped_expr(self, values):
        return "(" + str(values[0]) + ")"

    def if_statement(self, values):
        condition = values[0]
        body = values[1:]
        return "if " + condition + " {" + '\n'.join(body) + "\n}" 

    def while_loop(self, values):
        condition = values[0]
        body = values[1:]
        return "while " + condition + " {" + '\n'.join(body) + "\n}" 

    def for_loop(self, values):
        name = values[0]
        vector = values[1]
        body = values[2:]
        return "for " + name + " in " + vector + " {" + '\n'.join(body) + "}" 

    def read(self, values):
        return ".".join(values)

    def write(self, values):
        return ".".join(values[:-1]) + " = " + str(values[-1])

    def class_def(self, values):
        if len(values) > 1:
            return "let " + str(values[0]) + " = || {\n\tlet self = Object();\n" + '\n'.join(values[1:]) + "\n\treturn self; }"
        else:
            return "let " + str(values[0]) + " = || {\n\tlet self = Object();\n\treturn self;\n\n}"

    def subclass_def(self, values):
        if len(values) > 2:
            return "let " + str(values[0]) + " = || {\n\tlet self = " + str(values[1]) + "();\n" + '\n'.join(values[2:]) + "\n\treturn self; }"
        else:
            return "let " + str(values[0]) + " = || {\n\tlet self = " + str(values[1]) + "();\n\treturn self;\n\n}"

    def member_def(self, values):
        return "self." + str(values[0]) + " = " + str(values[1]) + ";"

    def class_function_no_args(self, values):
        return "|self| {" + '\n\t'.join(values) + " return self; }"

    def class_function_args(self, values):
        return "|self, " + str(values[0])[1:] + " { " + '\n\t'.join(values[1:]) + " return self;  }"

    def let_definition(self, values):
        return "let " + str(values[0]) + " = " + str(values[1])

    def regular_assign(self, values):
        return str(values[0]) + " = " + str(values[1])

    def instruction(self, values):
        return str(values[0]) + ";"

    def literal(self, values):
        return str(values[0])

    def index(self, values):
        return str(values[0]) + '[' + str(values[1]) + ']'

    def call(self, values):
        return str(values[0]) + "(" + str(values[1]) + ")"

    # def parameters(self, values):
    #     return "(" + ", ".join(values) + ")"

    def vector(self, values):
        return "[" + ", ".join(values) + "]"
        # return ", ".join(values)

    def lambda_args(self, values):
        return "|" + ", ".join(values) + "|"

    def args(self, values):
        return "|" + ", ".join(values) + "|"

    # def function_def(self, values):
    #     if len(values) > 1:
    #         return values[0] + "{" + values[1] + "}"
    #     else:
    #         return "|| {" + '\n'.join(values[0]) + "}"
    # def function_def_return(self, values):
    #     if len(values) > 1:
    #         return values[0] + "{" + values[1] + "}"
    #     else:
    #         return values[0] + " { }"
    # def function_no_args_def_return(self, values):
    #     return "|| {" + '\n'.join(values[0]) + "}"
    def function_no_args_def(self, values):
        return "|| {" + '\n'.join(values) + "}"

    def function_def(self, values):
        return values[0] + "{" + '\n'.join(values[1:]) + "}"

    def class_function_def_no_return(self, values):
        if len(values) > 1:
            return '|self, ' + values[0][1:] + "{" + values[1] + " return self; }"
        else:
            return "|| {" + values[0] + " return self; }"

    def class_function_def_return(self, values):
        if len(values) > 2:
            return '|self, ' + values[0][1:] + "{" + values[1] + values[2] + "}"
        elif len(values) > 1:
            return "|self| {" + values[0] + values[1] + "}"
        else:
            return "|self| {" + values[0] + "}"

    def method_retval(self, values):
        return "return self, " + str(', '.join(values)) + ';'

    def retval(self, values):
        return "return " + ', '.join(values) + ';'

    def method(self, values):
        # (NAME ".")+ NAME "(" parameters ")"
        names = values[:-1]
        parameters = values[-1]

        return '.'.join(names) + "(" + parameters + ")"

    def parameters(self, parameters):
        return ', '.join(parameters)

    def void_lambda_(self, values):
        return "|| { return " + str(values[0]) + "; }"

    def lambda_(self, values):
        return str(values[0]) + " { return " + str(values[1]) + "; }"

    def mod(self, values):
        return str(values[0]) + " % " + str(values[1])

    def multiply(self, values):
        return str(values[0]) + " * " + str(values[1])

    def add(self, values):
        return str(values[0]) + " + " + str(values[1])

    def subtract(self, values):
        return str(values[0]) + " - " + str(values[1])

    def divide(self, values):
        return str(values[0]) + " / " + str(values[1])

    def multiplyeq(self, values):
        return str(values[0]) + " *= " + str(values[1])

    def addeq(self, values):
        return str(values[0]) + " += " + str(values[1])

    def subtracteq(self, values):
        return str(values[0]) + " -= " + str(values[1])

    def divideeq(self, values):
        return str(values[0]) + " /= " + str(values[1])

    def modeq(self, values):
        return str(values[0]) + " %= " + str(values[1])

    def greater(self, values):
        return str(values[0]) + " > " + str(values[1])

    def less(self, values):
        return str(values[0]) + " < " + str(values[1])

    def greatereq(self, values):
        return str(values[0]) + " >= " + str(values[1])

    def lesseq(self, values):
        return str(values[0]) + " <= " + str(values[1])

    def eq(self, values):
        return str(values[0]) + " == " + str(values[1])

    def noteq(self, values):
        return str(values[0]) + " != " + str(values[1])

    def not_(self, values):
        return " not " + str(values[0])

    def or_(self, values):
        return str(values[0]) + " or " + str(values[1])

    def and_(self, values):
        return str(values[0]) + " and " + str(values[1])



def compile_file(path):
    script = PeriwinkleTree(path).transform(
                Lark(
                    GRAMMAR,
                    start='start',
                    parser='lalr',
                    lexer='standard',
                ).parse(open(path).read())
            )

    return script