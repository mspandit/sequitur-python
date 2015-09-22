from symbol import Symbol

class Rule(object):
    """
    The guard node in the linked list of symbols that make up the rule.
    It points forward to the first symbol in the rule, and backwards to the last
    symbol in the rule. Its own value points to the rule data structure, so that
    symbols can find out which rule they're in.
    """
    
    unique_rule_number = 1
    
    def __init__(self):
        super(Rule, self).__init__()
        self.reference_count = 0 # # of times the rule is used in the grammar
        self.guard = Symbol(self)
        self.reference_count = 0
        self.guard.join(self.guard)
        
        self.unique_number = Rule.unique_rule_number
        Rule.unique_rule_number += 1

    def __str__(self):
        """docstring for __str__"""
        return "Rule { reference_count: %d, unique_number: %d }" % (self.reference_count, self.unique_number)
    
    def first(self):
        """docstring for first"""
        return self.guard.next

    def last(self):
        """docstring for last"""
        return self.guard.prev

    def increment_reference_count(self):
        """docstring for increment_reference_count"""
        self.reference_count += 1

    def decrement_reference_count(self):
        """docstring for decrement_reference_count"""
        self.reference_count -= 1

    