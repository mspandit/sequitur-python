from symbol import Symbol


class Rule(object):
    
    unique_rule_number = 1
    
    def __init__(self, grammar):
        super(Rule, self).__init__()
        self.guard = Symbol.guard(grammar, self)
        self.guard.join(self.guard)
        self.reference_count = 0
        self.unique_number = Rule.unique_rule_number
        Rule.unique_rule_number += 1
    
    def first(self): return self.guard.next

    def last(self): return self.guard.prev

    def increment_reference_count(self): self.reference_count += 1

    def decrement_reference_count(self): self.reference_count -= 1

    def print_rule(self, rule_set, output_array, line_length):
        """docstring for print_rule"""
        symbol = self.first()
        while not symbol.is_guard():
            line_length = symbol.print_rule(rule_set, output_array, line_length)
            symbol = symbol.next
        return line_length

    def print_rule_expansion(self, rule_set, output_array, line_length):
        """docstring for print_rule_expansion"""
        symbol = self.first()
        while not symbol.is_guard():
            line_length = symbol.print_rule_expansion(rule_set, output_array, line_length)
            symbol = symbol.next
        return line_length
        
