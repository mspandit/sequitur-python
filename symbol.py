
class Symbol(object):
    """docstring for Symbol"""
    def __init__(self, value):
        from rule import Rule
        super(Symbol, self).__init__()
        self.next = None
        self.prev = None
        self.terminal = None
        self.rule = None
        
        if (str == type(value)):
            self.terminal = value
        elif (Symbol == type(value)):
            if value.terminal:
                self.terminal = value.terminal
            elif value.rule:
                self.rule = value.rule
                self.rule.increment_reference_count()
        elif (Rule == type(value)):
            self.rule = value
            self.rule.increment_reference_count()
        else:
            print "Did not recognize %s" % value

    digram_index = {}

    def join(self, right):
        """
        Links two symbols together, removing any old digram from the hash table.
        """
        if (self.next):
            self.delete_digram()
            
            """
            self is to deal with triples, where we only record the second
            pair of overlapping digrams. When we delete the second pair,
            we insert the first pair into the hash table so that we don't
            forget about it. e.g. abbbabcbb
            """
            
            if ((right.prev is not None) and (right.next is not None) and
                right.value() == right.prev.value() and
                right.value() == right.next.value()):
                Symbol.digram_index[right.hash_value()] = right
            if ((self.prev is not None) and (self.next is not None) and
                self.value() == self.next.value() and
                self.value() == self.prev.value()):
                Symbol.digram_index[self.hash_value()] = self
        self.next = right
        right.prev = self

    def delete(self):
        """
        Cleans up for symbol deletion: removes hash table entry and decrements
        rule reference count.
        """
        self.prev.join(self.next)
        if not self.is_guard():
            self.delete_digram()
            if self.rule:
                self.rule.decrement_reference_count()

    def delete_digram(self):
        """Removes the digram from the hash table"""
        if (self.is_guard() or self.next.is_guard()):
            return
        
        if (Symbol.digram_index.get(self.hash_value()) == self):
            Symbol.digram_index[self.hash_value()] = None

    def insert_after(self, symbol):
        """Inserts a symbol after this one"""
        symbol.join(self.next)
        self.join(symbol)

    def is_guard(self):
        """
        Returns true if this is the guard node marking the beginning and end of 
        a rule.
        """
        return self.rule and (self.rule.first().prev == self)

    def check(self):
        """
        Checks a new digram. If it appears elsewhere, deals with it by 
        calling match(), otherwise inserts it into the hash table
        """
        if (self.is_guard() or self.next.is_guard()):
            return None
        match = Symbol.digram_index.get(self.hash_value())
        if not match:
            Symbol.digram_index[self.hash_value()] = self
            return False
        if match.next != self:
            self.process_match(match)
        return True

    def expand(self):
        """
        This symbol is the last reference to its rule. It is deleted, and the
        contents of the rule substituted in its place.
        """
        left = self.prev
        right = self.next
        first = self.rule.first()
        last = self.rule.last()
        
        if (Symbol.digram_index[self.hash_value()] == self):
            Symbol.digram_index[self.hash_value()] = None
        left.join(first)
        last.join(right)
        Symbol.digram_index[last.hash_value()] = last

    def substitute(self, rule):
        """Replace a digram with a non-terminal"""
        prev = self.prev
        prev.next.delete()
        prev.next.delete()
        prev.insert_after(Symbol(rule))
        if not prev.check():
            prev.next.check()

    def process_match(self, match):
        """Deal with a matching digram"""
        from rule import Rule
        rule = None
        if (match.prev.is_guard() and match.next.next.is_guard()):
            # reuse an existing rule
            rule = match.prev.rule
            self.substitute(rule)
        else:
            # create a new rule
            rule = Rule()
            rule.last().insert_after(Symbol(self))
            rule.last().insert_after(Symbol(self.next))
            
            match.substitute(rule)
            self.substitute(rule)
            
            Symbol.digram_index[rule.first().hash_value()] = rule.first()

        # Check for an under-used rule
        if (rule.first().rule and (rule.first().rule.reference_count == 1)):
            rule.first().expand()
    
    def value(self):
        """docstring for value"""
        return (self.rule.unique_number if self.rule else self.terminal)

    def string_value(self):
        """docstring for string_value"""
        if self.rule:
            return "rule: %d" % self.rule.unique_number
        else:
            return self.terminal

    def hash_value(self):
        """docstring for hash_value"""
        return "%s+%s" % (self.string_value(), self.next.string_value())

    rule_set = None
    output_array = None
    line_length = None

    @staticmethod
    def print_rule(rule):
        """docstring for print_rule"""
        symbol = rule.first()
        while not symbol.is_guard():
            if symbol.rule is not None:
                rule_number = None
                if (Symbol.rule_set[symbol.rule.number] == symbol.rule):
                    rule_number = symbol.rule.number
                else:
                    rule_number = len(Symbol.rule_set)
                    symbol.rule.number = len(Symbol.rule_set)
                    Symbol.rule_set.append(symbol.rule)
                Symbol.output_array.append("%d " % rule_number)
                Symbol.line_length += len("%d " % rule_number)
            else:
                Symbol.output_array.append(Symbol.print_terminal(symbol.value()))
                Symbol.output_array.append(' ')
                Symbol.line_length += 2
            symbol = symbol.next

    @staticmethod
    def print_terminal(value):
        """docstring for print_terminal"""
        if (' ' == value):
            return '_'
        elif ("\n" == value):
            return "\n"
        else:
            return value

    @staticmethod
    def print_rule_expansion(rule):
        """docstring for print_rule_expansion"""
        symbol = rule.first()
        while not symbol.is_guard():
            if symbol.rule:
                Symbol.print_rule_expansion(symbol.rule)
            else:
                Symbol.output_array.append(Symbol.print_terminal(symbol.value()))
            symbol = symbol.next

    @staticmethod
    def print_grammar(s):
        """docstring for print_grammar"""
        Symbol.output_array = []
        Symbol.rule_set = [s]
    
        i = 0
        while i < len(Symbol.rule_set):
            Symbol.output_array.append("%s --> " % i)
            Symbol.line_length = len("%d   " % i)
            Symbol.print_rule(Symbol.rule_set[i])
        
            if i > 0:
                for j in range(Symbol.line_length, 50):
                    Symbol.output_array.append(' ')
                Symbol.print_rule_expansion(Symbol.rule_set[i])
            Symbol.output_array.append('\n');
            i += 1
        return "".join(Symbol.output_array)
