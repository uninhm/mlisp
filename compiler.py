from lexer import Lexer
from parser import ConstantDefinition, Parser, FunctionDefinition, IdentifierRef, Literal, FunctionCall, Keyword, If, Include
from langtypes import *

registers = ['rax', 'rdi', 'rsi', 'rdx', 'r10', 'r8', 'r9']

# TODO: Fix return type for built-in functions
# TODO: Check types for built-in functions
# TODO: Add generics
# TODO: Add more debug info into the generated assembly
# TODO: Follow function calling convention
# TODO: Optimize tail recursion
# TODO: Add casting
# TODO: Use stack for local variables
# TODO: Handle constants apart from variables
# TODO: Change int to int64, add uint64, int32, int16, etc. Handle sizes in registers where needed.
# TODO: Low priotiy: Add support for 128-bit integers

class Value:
    def __init__(self, typ, addr):
        self.typ = typ
        self.value = addr

class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.data = {}

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        elif self.parent:
            return self.parent[key]
        else:
            raise Exception('Undefined variable: ' + key)

    def __setitem__(self, key, value):
        self.data[key] = value


class Function:
    def __init__(self, name, ret_type, args, idx, scope):
        self.name = name
        self.ret_type = ret_type
        self.args = args
        self.idx = idx
        self.scope = scope

class Compiler:
    def print(self, msg):
        print(msg, file=self.file)

    def handle_keyword(self, expr, scope):
        if expr.op.name == 'syscall':
            for arg in expr.args:
                self.compile(arg, scope)
                self.print(f'push rax')
            for i in range(len(expr.args)-1, -1, -1):
                self.print(f"pop {registers[i]}")
            self.print("syscall")
        elif expr.op.name == 'getp':
            typ = self.get_type(expr.args[0], scope)
            if not isinstance(typ, Pointer):
                raise Exception(f'{expr.pos}: Expected pointer but got {typ}')
            self.compile(expr.args[0], scope)
            if sizeof(typ.typ) == 1:
                self.print(f'mov rdi, rax')
                self.print(f'xor rax, rax')
                self.print(f'mov al, {asm_size_repr(sizeof(typ.typ))} [rdi]')
            else:
                self.print(f'mov rax, {asm_size_repr(sizeof(typ.typ))} [rax]')
        elif expr.op.name == 'setp':
            typ = self.get_type(expr.args[0], scope)
            if not isinstance(typ, Pointer):
                raise Exception(f'{expr.pos}: Expected pointer')
            self.compile(expr.args[1], scope)
            self.print('push rax')
            self.compile(expr.args[0], scope)
            self.print('pop rdi')
            # TODO: Handle every possible size
            if sizeof(typ.typ) == 1:
                self.print(f'mov {asm_size_repr(sizeof(typ.typ))} [rax], dil')
            else:
                self.print(f'mov {asm_size_repr(sizeof(typ.typ))} [rax], rdi')
        elif expr.op.name == 'addr':
            if not isinstance(expr.args[0], IdentifierRef):
                raise Exception(f'{expr.pos}: Expected identifier')
            addr = scope[expr.args[0].name].value.split('[')[1][:-1] #TODO: Do this in a better way
            if '-' in addr:
                a, b = addr.split('-')
                self.print(f'mov rax, {a}')
                self.print(f'sub rax, {b}')
            else:
                a, b = addr.split('+')
                self.print(f'mov rax, {a}')
                self.print(f'add rax, {b}')
        elif expr.op.name == '|':
            self.compile(expr.args[1], scope)
            self.print('push rax')
            self.compile(expr.args[0], scope)
            self.print('pop rbx')
            self.print('or rax, rbx')
        elif expr.op.name == '&':
            self.compile(expr.args[1], scope)
            self.print('push rax')
            self.compile(expr.args[0], scope)
            self.print('pop rbx')
            self.print('and rax, rbx')
        elif expr.op.name == 'var': # TODO: This should be handled by the parser as a diferent expression
            typ = expr.args[0].typ
            if typ is None:
                raise Exception(f'{expr.pos}: Missing type at variable declaration')
            mem_size = self.mem_size
            self.mem_size += sizeof(typ)
            if self.debug:
                self.print(f'; {expr.args[0].name}: [mem+{mem_size}]')
            sz = asm_size_repr(sizeof(typ))
            scope[expr.args[0].name] = Value(typ, f'{sz} [mem+{mem_size}]')
            if len(expr.args) == 2:
                typ2 = self.get_type(expr.args[1], scope)
                if typ2 is None:
                    raise Exception(f'{expr.pos}: Undefined type')
                if typ != typ2:
                    raise Exception(f'{expr.pos}: Types don\'t match')
                if self.debug:
                    self.print(f'; {expr.args[0].name}: [mem+{mem_size}]')
                self.compile(expr.args[1], scope)
                if sizeof(typ) == 1:
                    self.print(f'mov {sz} [mem+{mem_size}], al')
                else:
                    self.print(f'mov {sz} [mem+{mem_size}], rax')
        elif expr.op.name == 'set':
            typ1 = self.get_type(expr.args[0], scope)
            typ2 = self.get_type(expr.args[1], scope)
            if typ1 != typ2:
                raise Exception(f'{expr.pos}: Expected {typ1} but got {typ2}')
            self.compile(expr.args[1], scope)
            # TODO: Handle every possible size
            if sizeof(typ1) == 1:
                self.print(f'mov {scope[expr.args[0].name].value}, al')
            else:
                self.print(f'mov {scope[expr.args[0].name].value}, rax')
        elif expr.op.name == 'reserve':
            if not isinstance(expr.args[0], Literal) and not isinstance(expr.args[0], IdentifierRef):
                raise Exception('Expected expected constant amount for memory reservation')
            self.print(f'mov rax, mem')
            self.print(f'add rax, {self.mem_size}')
            if isinstance(expr.args[0], Literal):
                self.mem_size += expr.args[0].value
            else:
                self.mem_size += int(scope[expr.args[0].name].value)
        elif expr.op.name == 'progn':
            for body_expr in expr.args:
                self.compile(body_expr, scope)
        elif expr.op.name == '<':
            self.compile(expr.args[1], scope)
            self.print(f'push rax')
            self.compile(expr.args[0], scope)
            self.print('pop rbx')
            self.print('mov rcx, 0')
            self.print('mov rdx, 1')
            self.print('cmp rax, rbx')
            self.print('cmovl rcx, rdx')
            self.print('mov rax, rcx')
        elif expr.op.name == '=':
            self.compile(expr.args[1], scope)
            self.print(f'push rax')
            self.compile(expr.args[0], scope)
            self.print('pop rbx')
            self.print('mov rcx, 0')
            self.print('mov rdx, 1')
            self.print('cmp rax, rbx')
            self.print('cmove rcx, rdx')
            self.print('mov rax, rcx')
        elif expr.op.name == '-':
            if len(expr.args) == 1:
                self.compile(expr.args[0], scope)
                self.print('neg rax')
            else:
                self.compile(expr.args[1], scope)
                self.print(f'push rax')
                self.compile(expr.args[0], scope)
                self.print('pop rbx')
                self.print('sub rax, rbx')
        elif expr.op.name == '+':
            self.compile(expr.args[1], scope)
            self.print(f'push rax')
            self.compile(expr.args[0], scope)
            self.print('pop rbx')
            self.print('add rax, rbx')
        elif expr.op.name == '*':
            self.compile(expr.args[1], scope)
            self.print(f'push rax')
            self.compile(expr.args[0], scope)
            self.print('pop rbx')
            self.print('imul rax, rbx')
        elif expr.op.name == '/':
            self.compile(expr.args[1], scope)
            self.print(f'push rax')
            self.compile(expr.args[0], scope)
            self.print('pop rbx')
            self.print('cqo')
            self.print('idiv rbx')
        elif expr.op.name == '%':
            self.compile(expr.args[1], scope)
            self.print(f'push rax')
            self.compile(expr.args[0], scope)
            self.print('pop rbx')
            self.print('xor rdx, rdx')
            self.print('div rbx')
            self.print('mov rax, rdx')
        elif expr.op.name == 'not':
            self.compile(expr.args[0], scope)
            self.print('mov rcx, 0')
            self.print('mov rdx, 1')
            self.print('test rax, rax')
            self.print('cmovz rcx, rdx')
            self.print('mov rax, rcx')
        else:
            raise Exception(f'Unknown keyword: {expr.op.name}')

    def compile_if(self, expr, scope):
        else_idx = self.else_idx
        self.else_idx += 1
        end_idx = self.end_idx
        self.end_idx += 1

        self.compile(expr.cond, scope)
        self.print(f'test rax, rax')
        self.print(f'jz else_{else_idx}')
        self.compile(expr.body, scope)
        # TODO: Optimize jumps when there is no else
        self.print(f'jmp end_{end_idx}')
        self.print(f'else_{else_idx}:')
        if expr.else_body is not None:
            self.compile(expr.else_body, scope)
        self.print(f'end_{end_idx}:')

    def compile_function_definition(self, expr, scope, isinner=False):
        func_idx = self.func_idx
        self.func_idx += 1
        end_idx = None
        if isinner:
            end_idx = self.end_idx
            self.end_idx += 1
        if self.debug:
            self.print(f'; ----- {expr.name} -----')
        self.print(f'func_{func_idx}:')
        self.print('push rbp')
        self.print('mov rbp, rsp')
        subscope = Scope(scope)
        offset = 16
        for arg in expr.args:
            if arg.typ is None:
                raise Exception('Expected type for argument')
            if self.debug:
                self.print(f'; {arg.name}: [rbp+{offset+8-sizeof(arg.typ)}]')
            sz = asm_size_repr(sizeof(arg.typ))
            subscope[arg.name] = Value(arg.typ, f'{sz} [rbp+{offset+8-sizeof(arg.typ)}]')
            offset += 8 # sizeof(arg.typ)
        scope[expr.name] = Value('func', Function(expr.name, expr.ret_type, expr.args, func_idx, subscope))
        if expr.ret_type is not None and self.get_type(expr.body[-1], subscope) != expr.ret_type:
            raise Exception(f'{expr.pos}: Expected return type {expr.ret_type} but got {self.get_type(expr.body[-1], subscope)}')
        for body_expr in expr.body:
            self.compile(body_expr, subscope)
        self.print('pop rbp')
        self.print('ret')
        if isinner:
            self.print(f'end_{end_idx}:')

    def get_type(self, expr, scope):
        if isinstance(expr, Literal):
            return expr.typ
        elif isinstance(expr, IdentifierRef):
            return scope[expr.name].typ
        elif isinstance(expr, FunctionCall) and isinstance(expr.op, Keyword):
            if expr.op.name in ('+', '-', '*', '/', '%'):
                return self.get_type(expr.args[0], scope)
            elif expr.op.name in ('print', '<', '=', 'not'):
                return Integer()
            elif expr.op.name == 'addr':
                return Pointer(self.get_type(expr.args[0], scope))
            elif expr.op.name == 'getp':
                typ = self.get_type(expr.args[0], scope)
                assert isinstance(typ, Pointer), f'{expr.pos}: got {expr.args[0]} of type {expr.args[0].typ}'
                return typ.typ
            elif expr.op.name == 'progn':
                return self.get_type(expr.args[-1], scope)
            elif expr.op.name == 'reserve':
                return Pointer()
            else:
                return Integer()
                # TODO: Handle every keyword
                # raise Exception(f'Unknown type for keyword: {expr.op.name}')
        elif isinstance(expr, FunctionCall):
            func = scope[expr.op.name].value
            return func.ret_type
        elif isinstance(expr, If):
            if self.get_type(expr.body, scope) != self.get_type(expr.else_body, scope):
                return None
            else:
                return self.get_type(expr.body, scope)
        else:
            raise Exception(f'Can\'t type check {type(expr)}')

    def compile_function_call(self, expr, scope):
        func = scope[expr.op.name]
        if func.typ != 'func':
            raise Exception(f'Expected function, got {func.typ}')
        func = func.value
        if len(expr.args) != len(func.args):
            raise Exception('Wrong number of arguments')
        for i in reversed(range(len(func.args))):
            if self.get_type(expr.args[i], scope) != func.args[i].typ:
                raise Exception(f'{expr.pos}: Argument {i} expected {func.args[i].typ}, got {self.get_type(expr.args[i], scope)}')
            self.compile(expr.args[i], scope)
            self.print('push rax')
        self.print(f'call func_{func.idx}')
        self.print(f'add rsp, {8*len(func.args)}')

    def compile(self, expr, scope):
        """
        Compile an expression into assembly code,
        write the assembly code to the output file
        and return the register where the result is stored.
        """
        if self.debug:
            self.print(f'; {expr.pos}: {expr}')
        if isinstance(expr, Include):
            raise Exception('Can\'t include inside an expression')
        elif isinstance(expr, Literal):
            if type(expr.value) == str: #TODO: Replace with lang type check
                self.str_literals.append(expr.value)
                self.print(f'mov rax, str_{len(self.str_literals)-1}')
            elif type(expr.value) == int:
                self.print(f'mov rax, {expr.value}')
            else:
                raise Exception(f'Unsupported literal type: {type(expr.value)}')
        elif isinstance(expr, ConstantDefinition):
            scope[expr.name] = Value(expr.value.typ, f'{expr.value.value}')
        elif isinstance(expr, IdentifierRef):
            if scope is None:
                raise Exception('IdentifierRef without scope')
            if isinstance(scope[expr.name].value, Function):
                raise Exception('Closures are not implemented')
            if sizeof(self.get_type(expr, scope)) == 1: #TODO: Handle every possible size
                self.print('xor rax, rax')
                self.print(f'mov al, {scope[expr.name].value}')
            else:
                self.print(f'mov rax, {scope[expr.name].value}')
        elif isinstance(expr, If):
            self.compile_if(expr, scope)
        elif isinstance(expr, FunctionDefinition):
            raise Exception('Can\'t define functions inside an expression')
            self.compile_function_definition(expr, scope, isinner=True)
        elif isinstance(expr, FunctionCall):
            if isinstance(expr.op, Keyword):
                self.handle_keyword(expr, scope)
            else:
                self.compile_function_call(expr, scope)
        else:
            raise Exception(f'Not implemented expression type: {type(expr)}')

    def footer(self):
        self.print('mov rax, 60')
        self.print('mov rdi, 0')
        self.print('syscall')

        if self.nasm:
            self.print('section .data')
        else:
            self.print('segment readable')

        for i, e in enumerate(self.str_literals):
            cms = ','.join(str(ord(c)) for c in e)
            self.print(f'str_{i}: db {cms},0')

        if self.nasm:
            self.print('section .bss')
            self.print(f'mem: resb {self.mem_size}')
        else:
            self.print('segment readable writable')
            self.print(f'mem: rb {self.mem_size}')

    def compile_include(self, expr, scope):
        lexer = Lexer()
        parser = Parser()
        with open(expr.path, 'r') as f:
            code = f.read()
        exprs = []
        for pres in parser.parse(lexer.make_tokens(expr.path, code)):
            if pres.error:
                raise Exception(f'{pres.error}')
            exprs.append(pres.result)
        self.exprs2.extend(self.compile_first_step(exprs, scope))

    def declare_var(self, expr, scope):
        typ = expr.args[0].typ
        if typ is None:
            raise Exception(f'{expr.pos}: Missing type at variable declaration')
        mem_size = self.mem_size
        self.mem_size += sizeof(typ)
        if self.debug:
            self.print(f'; {expr.args[0].name}: [mem+{mem_size}]')
        sz = asm_size_repr(sizeof(typ))
        scope[expr.args[0].name] = Value(typ, f'{sz} [mem+{mem_size}]')

    def set_var(self, expr, scope):
        typ = scope[expr.args[0].name].typ
        typ2 = self.get_type(expr.args[1], scope)
        if typ2 is None:
            raise Exception(f'{expr.pos}: Undefined type')
        if typ != typ2:
            raise Exception(f'{expr.pos}: Types don\'t match')
        self.compile(expr.args[1], scope)
        if sizeof(typ) == 1:
            self.print(f'mov {scope[expr.args[0].name].value}, al')
        else:
            self.print(f'mov {scope[expr.args[0].name].value}, rax')

    def header(self):
        if self.nasm:
            self.print('segment .text')
        else:
            self.print('format ELF64 executable 3')
            self.print('segment readable executable')

    def compile_first_step(self, exprs, scope):
        exprs2 = []
        for expr in exprs:
            if isinstance(expr, Include):
                self.compile_include(expr, scope)
            elif isinstance(expr, ConstantDefinition):
                self.compile(expr, scope)
            elif isinstance(expr, FunctionDefinition):
                self.compile_function_definition(expr, scope)
            elif isinstance(expr, FunctionCall) and expr.op.name == 'var':
                self.declare_var(expr, scope)
                exprs2.append(expr)
            else:
                exprs2.append(expr)
        return exprs2

    def compile_second_step(self, exprs, scope):
        for expr in exprs:
            if isinstance(expr, FunctionCall) and\
                    expr.op.name == 'var' and\
                    len(expr.args) == 2:
                self.set_var(expr, scope)
            else:
                self.compile(expr, scope)

    def compile_all(self, exprs):
        self.else_idx = 0
        self.end_idx = 0
        self.func_idx = 0
        self.debug = True
        self.mem_size = 0
        self.file = open('out.asm', 'w')
        self.str_literals = []
        self.nasm = False

        self.header()

        global_scope = Scope()

        self.exprs2 = []
        exprs2 = self.compile_first_step(exprs, global_scope)
        self.exprs2.extend(exprs2)

        if self.nasm:
            self.print('global _start')
            self.print('_start:')
        else:
            self.print('entry start')
            self.print('start:')

        self.compile_second_step(self.exprs2, global_scope)

        self.footer()
