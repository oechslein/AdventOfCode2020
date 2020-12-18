from Utils import Parser
from input import PUZZLE_INPUT, TEST_INPUT


class CalcParser(Parser):
    def start(self):
        return self.expression()

    # Expression ==> Term ( ( "+" | "-" ) Term )*
    def expression(self):
        rv = self.match('term')
        while op := self.maybe_keyword('+', '-'):
            term = self.match('term')
            if op == '+':
                rv += term
            else:
                rv -= term

        return rv

    # Term ==> Factor ( ( "*" | "/" ) Factor )*
    def term(self):
        rv = self.match('factor')
        while op := self.maybe_keyword('*', '/'):
            term = self.match('factor')
            if op == '*':
                rv *= term
            else:
                rv /= term

        return rv

    # Factor ==> "(" Expression ")"
    def factor(self):
        if not self.maybe_keyword('('):
            return self.match('number')

        rv = self.match('expression')
        self.keyword(')')
        return rv


assert CalcParser().parse("4+5") == (4 + 5)
assert CalcParser().parse("(4+5)") == (4 + 5)
assert CalcParser().parse("(4+5)*3") == (4 + 5) * 3


class CalcParserReversed(Parser):
    def start(self):
        return self.expression()

    def expression(self):
        rv = self.match('term')
        while op := self.maybe_keyword('*', '/'):
            term = self.match('term')
            if op == '*':
                rv *= term
            else:
                rv /= term
        return rv

    def term(self):
        rv = self.match('factor')
        while op := self.maybe_keyword('+', '-'):
            term = self.match('factor')
            if op == '+':
                rv += term
            else:
                rv -= term
        return rv

    def factor(self):
        if not self.maybe_keyword('('):
            return self.match('integer')

        rv = self.match('expression')
        self.keyword(')')
        return rv


def parse_input(my_input):
    return my_input.strip().split('\n')


def calc_list(lines):
    return sum(CalcParserReversed().parse(line) for line in lines)


assert calc_list(parse_input(TEST_INPUT)) == (51 + 46 + 1445 + 669060 + 23340)
print(calc_list(parse_input(PUZZLE_INPUT)))
