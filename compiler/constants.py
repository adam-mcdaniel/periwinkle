
CABLELANG_PRELUDE = r'''
include "std/list/list.cpp";
let pop = pop_fn&;
let push = append_fn&;
let remove = remove_fn&;
let len = len_fn&;
let range = range_fn&;


include "std/str/str.cpp";
let raw_to_string = raw_to_string_fn&;
let raw_type = raw_type_fn&;

include "std/io/io.cpp";
let put = put_fn&;
let putln = putln_fn&;

include "std/exported/exported.cpp";


let Object = || {
    let self = @;

    self.new = || {
        return self;
    };
    
    self.__bool__ = |self| {
        return self, false;
    };

    self.__str__ = |self| {
        return self, "<Object>";
    };

    self.__integer__ = |self| {
        return self, 0;
    };

    self.__decimal__ = |self| {
        return self, 0.0;
    };

    self.__list__ = |self| {
        return self, [];
    };

    self.__fn__ = |self| {
        return self, || { return @; };
    };

    self.__value__ = |self| {
        return self, @;
    };

    self.__type__ = |self| {
        return self, "Object";
    };

    return self;
};


let __case_none__ = |a, b, c| {
    if raw_type(a) == "NoneType" {
        return b;
    }

    if raw_type(a) != "NoneType" {
        return c;
    }
};


let value = |o| { return __case_none__(o, |a| {return a.__value__();} (o), o); };
let str = |o| { return __case_none__(o, |a| {return a.__str__();} (o), raw_to_string(o)); };
let boolean = |o| { return __case_none__(o, |a| {return a.__bool__();} (o), o); };
let integer = |o| { return __case_none__(o, |a| {return a.__integer__();} (o), o); };
let decimal = |o| { return __case_none__(o, |a| {return a.__decimal__();} (o), o); };
let function = |o| { return __case_none__(o, |a| {return a.__fn__();} (o), o); };
'''

GRAMMAR = r'''?start: ((all ";") | (all))*
?block: ((all ";") | (all))*

include: "include" STRING
import_: "import" STRING


all: instruction 
   | while
   | for
   | if
   | include
   | import_

identifier: NAME

instruction: expr
            | class_def


?expr: assignment
    | conditional
    | value
    | "(" expr ")" -> wrapped_expr
    | math

eq: expr "==" expr
    | expr "is" expr
noteq: expr "!=" expr
not_: "not" expr
and_: expr "and" expr
or_: expr "or" expr
add: expr "+" expr
addeq: (variable | read) "+=" expr
subtract: expr "-" expr
subtracteq: (variable | read) "-=" expr
multiply: expr "*" expr
multiplyeq: (variable | read) "*=" expr
divide: expr "/" expr
divideeq: (variable | read) "/=" expr
mod: expr "%" expr
modeq: (variable | read) "%=" expr
greater: expr ">" expr
less: expr "<" expr
greatereq: expr ">=" expr
lesseq: expr "<=" expr

?math: add
    | subtract
    | multiply
    | divide
    | mod
    | eq
    | noteq
    | not_
    | and_
    | or_
    | greatereq
    | lesseq
    | greater
    | less

lambda: args "=>" expr -> lambda_
      | "(" ")" "=>" expr -> void_lambda_

member_def: write
          | variable "=" class_method
class_def: "class" identifier "{" (member_def)* "}"
         | "class" identifier ":" identifier "{" (member_def)* "}" -> subclass_def
method_retval: "return" (expr ",")* expr
class_method: args "{" (instruction | class_if | class_for | class_while | method_retval)* "}" -> class_function_args
            | "(" ")" "{" (instruction | class_if | class_for | class_while | method_retval)* "}" -> class_function_no_args


?read: (identifier ".")+ identifier -> read
     | expr "." (identifier ".")* identifier -> read
?write: (identifier ".")+ identifier "=" expr


?assignment: "let" variable "=" expr -> let_definition
            | variable "=" expr -> regular_assign
            | write
            | addeq
            | subtracteq
            | multiplyeq
            | divideeq
            | modeq

index: expr "[" expr "]"
?limited_value: lambda
            | call
            | read
            | index
            | variable
            | literal
?value: limited_value
    | function


literal: NUMBER -> integer
    | FLOAT_NUMBER -> decimal
    | STRING -> string
    | vector
    | "@" -> obj
    | "true" -> true
    | "false" -> false

vector: "[" (expr ",")* (expr)* "]"

args: "(" (variable ",")* variable ")"
retval: "return" (expr ",")* expr
function: args "{" (block | retval)* "}" -> function_def
        | "(" ")" "{" (block | retval)* "}" -> function_no_args_def

while: "while" expr "{" block "}" -> while_loop
for: "for" identifier "in" expr "{" block "}" -> for_loop
if: "if" expr "{" block "}" -> if_statement

class_while: "while" expr "{" (block | method_retval)* "}" -> while_loop
class_for: "for" identifier "in" expr "{" (block | method_retval)* "}" -> for_loop
class_if: "if" expr "{" (block | method_retval)* "}" -> if_statement

conditional: "?" expr expr ":" expr

parameters: (expr ",")* (expr)*
call: (identifier ".")+ identifier "(" parameters ")" -> method
    | expr "." (identifier ".")* identifier "(" parameters ")" -> method
    | variable "(" parameters ")"
    | expr "(" parameters ")"


?variable: identifier
        | identifier "&" -> foreign_variable


NUMBER: /0|[1-9]\d*/i
FLOAT_NUMBER: /((\d+\.\d*|\.\d+)(e[-+]?\d+)?|\d+(e[-+]?\d+))/i
STRING : /[ubf]?r?("(?!"").*?(?<!\\)(\\\\)*?"|'(?!'').*?(?<!\\)(\\\\)*?')/i
NAME: /[a-zA-Z_]\w*/
COMMENT: /\/\/[^\n]*/
//COMMENT: /#[^\n]*/

%ignore /[\t \f\n]+/  // WS
%ignore /\\[\t \f\n]*\r?\n/   // LINE_CONT
%ignore COMMENT
'''