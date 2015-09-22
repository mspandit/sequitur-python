from symbol import Symbol
from rule import Rule

class Grammar(object):
    """docstring for Grammar"""
    def __init__(self):
        super(Grammar, self).__init__()
        self.digram_index = {}
        self.root_production = Rule()

    def train_string(self, string):
        """docstring for train_string"""
        input_sequence = [c for c in string]
        if (0 < len(input_sequence)):
            self.root_production.last().insert_after(Symbol(input_sequence.pop(0)))
        while (0 < len(input_sequence)):
            self.root_production.last().insert_after(Symbol(input_sequence.pop(0)))
            self.root_production.last().prev.check()

    def print_rule(self, rule, output_array):
        """docstring for print_rule"""
        symbol = rule.first()
        while not symbol.is_guard():
            if symbol.rule:
                if (symbol.rule in self.rule_set):
                    rule_index = self.rule_set.index(symbol.rule, False)
                else:
                    rule_index = len(self.rule_set)
                    self.rule_set.append(symbol.rule)
                output_array.append("%d " % rule_index)
                self.line_length += len("%d " % rule_index)
            else:
                output_array.append("%s " % self.print_terminal(symbol.value()))
                self.line_length += len("%s " % self.print_terminal(symbol.value()))
            symbol = symbol.next

    def print_terminal(self, value):
        """docstring for print_terminal"""
        if (' ' == value):
            return '_'
        elif ("\n" == value):
            return "\n"
        else:
            return value

    def print_rule_expansion(self, rule, output_array):
        """docstring for print_rule_expansion"""
        symbol = rule.first()
        while not symbol.is_guard():
            if symbol.rule:
                self.print_rule_expansion(symbol.rule, output_array)
            else:
                output_array.append(self.print_terminal(symbol.value()))
            symbol = symbol.next

    def print_grammar(self):
        """docstring for print_grammar"""
        output_array = []
        self.rule_set = [self.root_production]
    
        i = 0
        for rule in self.rule_set:
            output_array.append("%s --(%d)--> " % (i, rule.reference_count))
            self.line_length = len("%s --(%d)--> " % (i, rule.reference_count))
            self.print_rule(rule, output_array)
        
            if i > 0:
                output_array.append(' ' * (57 - self.line_length))
                self.print_rule_expansion(rule, output_array)
            output_array.append('\n');
            i += 1
        return "".join(output_array)
