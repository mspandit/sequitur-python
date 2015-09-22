import unittest
from symbol import Symbol
from rule import Rule

class TestSequitur(unittest.TestCase):
    def test_sequitur(self):
        """docstring for test_sequitur"""
        s = Rule()
        input_sequence = [c for c in "Hello, world!"]
        if (0 < len(input_sequence)):
            s.last().insert_after(Symbol(input_sequence.pop(0)))
        while (0 < len(input_sequence)):
            s.last().insert_after(Symbol(input_sequence.pop(0)))
            s.last().prev.check()
        
        self.assertEqual("0 --> H e l l o , _ w o r l d ! \n", Symbol.print_grammar(s))

    def test_sequitur_base(self):
        """docstring for test_sequitur_base"""
        Symbol.digram_index = {}
        s = Rule()
        input_sequence = [c for c in "abcabdabcabd"]
        if (0 < len(input_sequence)):
            s.last().insert_after(Symbol(input_sequence.pop(0)))
        while (0 < len(input_sequence)):
            s.last().insert_after(Symbol(input_sequence.pop(0)))
            s.last().prev.check()
        
        pg = Symbol.print_grammar(s)
        self.assertEqual("0 --> 1 1 \n1 --> 2 c 2 d                                       abcabd\n2 --> a b                                           ab\n", pg)

if __name__ == '__main__':
    unittest.main()
