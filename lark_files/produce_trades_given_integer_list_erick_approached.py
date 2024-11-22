# -*- coding: utf-8 -*-
"""
Generate trades using Erik code 
"""

from typing import List

import random
from lark import Lark
from lark.grammar import NonTerminal, Terminal, Rule
from lark.lexer import TerminalDef

# Updated grammar with a "NUMBER" placeholder for numbers
 
grammar_str = """
rules: trade
     | rules trade

trade: "Trade(" person "," person "," xvalue "," yvalue ")"

person: "Alice" | "Bob" | "Charles"
xvalue: "Xvalue(" number ")"
yvalue: "Yvalue(" number ")"

number: "NUMBER"
"""

# Functions

## Function to create the parser
def get_parser_from_bnf_string(bnf_string: str) -> "Lark":
    """
    Create a Lark parser from a given BNF string.

    Parameters
    ----------
    bnf_string : str
        The BNF string to create a parser from.

    Returns
    -------
    Lark
        The created parser.

    Notes
    -----
    The 'start' rule is explicitly passed to the Lark constructor as "rules".
    The 'debug' parameter is set to True to enable debugging output.
    """
    parser = Lark(bnf_string, start="rules", debug=True)  # Explicitly pass the 'start' rule
    return parser

## Function that process the "Non-terminals"
def get_production_choices(value: NonTerminal, rules: List["Rule"]) -> List["Rule"]:
    """
    Return Finds all production rules for a given NonTerminal symbol (value).

    This function takes a NonTerminal value and a list of rules and returns a list of
    all the production choices/rules associated with the given NonTerminal value.

    Parameters
    ----------
    value : NonTerminal
        The NonTerminal symbol to get the production choices/rules from.
    rules : List[Rule]
        The list of rules (grammar rules from the parser) to search from.

    Returns
    -------
    List[Rule]
        A list of production choices/rules where the origin matches the provided NonTerminal symbol (value).

    Raises
    ------
    AssertionError
        If there are no production choices/rules associated with the given NonTerminal value (value).
    """
    
    production_choices = []
    # Iterates over the rules to find those that originate from the given NonTerminal symbol (value)
    for rule in rules:
        # Selects the production choices/rules associated with the Nonterminal rule stored in value 
        if value == rule.origin:
            production_choices.append(rule)
    # production_choices will have all the production choices/rules associated with Nonterminal rule stored in value 
    assert production_choices
    return production_choices

## Function that process the "Terminals"
def get_terminal_string(symbol: Terminal, terminals: List["TerminalDef"]) -> str:
    # Generate a number if symbol.name == "NUMBER" 
    """
    Return the string associated with a given Terminal symbol (symbol) from the list of terminals (terminals).
    I.e.  Converts terminal symbol into its string representation.

    # TODO Checkout if there is a better approach to handle "NUMBERS" terminals
    If the symbol is a "NUMBER" terminal, a random float between 10 and 100 is generated and returned as a string.

    Parameters
    ----------
    symbol : Terminal
        The Terminal symbol to get the string from.
    terminals : List[TerminalDef]
        The list of terminals (grammar terminals symbols from the parser) to search from.

    Returns
    -------
    str
        The string associated with the given Terminal symbol (symbol).

    Raises
    ------
    KeyError
        If the symbol is not found in the list of terminals (terminals).
    """
    if symbol.name == "NUMBER":
        # TODO Look if there is a better approached to handle "NUMBERS" terminals
        return str(round(random.uniform(10, 100), 1))  # Generate a random float between 10 and 100
    
    # Iterates through all terminals if symbol.name != "NUMBER"
    for terminal in terminals:
        # Selects the appropriate "string" or "regex" associated with the symbol Terminal
        if terminal.name == symbol.name:
            return terminal.pattern.value # Retrieves the "string" or "regex" associated with the symbol Terminal
    
    raise KeyError(symbol)

## Function that generates the sentence given the Grammar and the input list of integers 
def generate_sentence_from_grammar(inputs: List[int], parser: "Lark") -> str:
    """
    Generates a sentence by expanding the grammar's non-terminal symbols using production rules, guided by the input list of integers.

    This function works by iterating over the list of inputs and using each input to select a production rule from the grammar.
    The selected production rule is then used to generate symbols, which are then added to the list of symbols to be rewritten.
    The list of symbols to be rewritten is then processed until it is empty, at which point the function returns the generated sentence.

    Parameters
    ----------
    inputs : List[int]
        A list of integers used to decide which production rule from the grammar to apply at each step.
    parser : Lark
        The Lark parser object created from the grammar.

    Returns
    -------
    str
        The generated sentence.

    Raises
    ------
    IndexError
        If the list of inputs is not long enough to generate the desired sentence.
    """

    # Variables: 

    ## rewrite_symbols: A list of symbols (Terminals and NonTerminals) to be processed. It is dynamically updated, and its content at each step of the loop will depend on the input list of integers 
    ## MAX_CNT: Safety limit to prevent infinite loops
    ## cnt: A counter to track the current position in the inputs list
    ## sentence: A list to collect the sentence's terminal strings.

    # Initialization conditions for the loop
    rewrite_symbols = [parser.rules[0].origin] # Always start with the associated Nonterminal in the LHS of the first production rule 
    MAX_CNT = 100000
    cnt = 0
    sentence = []
    
    # Loop keeps going until there are no more symbols to process (i.e. rewrite_symbols symbols is empty) or the maximum count "MAX_CNT" is reached.
    while rewrite_symbols and cnt < MAX_CNT:
        
        # current_symbol: can be either a Terminal or a NonTerminal 
        current_symbol = rewrite_symbols.pop(0) # removes and returns the element at the start of rewrite_symbols
        
        # Note: rewrite_symbols: 
        ## The list "rewrite_symbols" gets expanded everytime "current_symbol" is a "NonTerminal". 
        ## It will be expanded by the RH of the rule associated with the NonTerminal and the production choice selected via the list of integers    
        
        ## However, at any step of the loop the list "rewrite_symbols" gets shrink everytime by one element due to "current_symbol = rewrite_symbols.pop(0)"
        
        # Note: sentence
        ## Only gets uptade when "current_symbol" is a Terminal, and evrytime "current_symbol" is a Terminal it gets expanded by the "string" or "regex" associated with that terminal
        
        # Check if current_symbol is a Terminal or a NonTerminal
        if not isinstance(current_symbol, NonTerminal):
            # Gets executed if it is a Terminal
            sentence.append(get_terminal_string(current_symbol, parser.terminals)) # Returns the "string" or "regex" associated with the Terminal
        else:
            # Gets executed if it is a NonTerminal
            production_choices = get_production_choices(current_symbol, parser.rules) # Returns the 
            
            # Check if cnt is within the bounds of inputs
            if cnt >= len(inputs):
                #raise IndexError(f"Not enough inputs provided. Needed at least {cnt + 1}, but got {len(inputs)}.")
                raise IndexError("Not enough inputs provided. Please provide a full list of integers to generate the desire Trade output.")
            
            # Cycle update condictions: 
            
            ## Calculates the residual between the integer in the list inputs at position cnt and the length of the production_choices of the NonTerminal given in "current_symbol" 
            idx = inputs[cnt] % len(production_choices)  
            
            ## Selects the production rule form production_choices by the idx index that results in the previous step
            symbols = production_choices[idx] 
            
            ## Extracts all the Terminal and NonTerminal symbols in the RHS of the associated production rule stored in "symbols"
            symbol_list = [symbol for symbol in symbols.expansion] 
            
            ## Updates recusively the rewrite_symbols list, so that in the next steps the symbols in "symbol_list" that were added to "rewrite_symbols" get processed as well in the following steps
            rewrite_symbols = symbol_list + rewrite_symbols 
            
            ## Update the counter "cnt" everytime current_symbol is a "NonTerminal"
            cnt += 1 
    
    assert not rewrite_symbols
    return "".join(sentence)


# Create Lark object
parser = get_parser_from_bnf_string(grammar_str)

# Inputs to generate the desired sentence

# One Trade 
inputs_one_trade = [0, 0, 0, 0, 0, 0, 0, 0] # 8 integers

# Two Trades
inputs_two_trades = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 16 integers

# Three Trades
inputs_three_trades = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 24 integers

# Updated Inputs List
# =============================================================================
# inputs_three_trades = [
#     1, 1, 0,     # `rules` decisions
#     0,           # `trade`
#     0, 0,        # First `trade` `person`s
#     0,           # `xvalue`
#     0,           # `number` in `xvalue`
#     0,           # `yvalue`
#     0,           # `number` in `yvalue`
#     0,           # `trade`
#     0, 0,        # Second `trade` `person`s
#     0,           # `xvalue`
#     0,           # `number` in `xvalue`
#     0,           # `yvalue`
#     0,           # `number` in `yvalue`
#     0,           # `trade`
#     0, 0,        # Third `trade` `person`s
#     0,           # `xvalue`
#     0,           # `number` in `xvalue`
#     0,           # `yvalue`
#     0            # `number` in `yvalue`
# ]
# =============================================================================

# Generate Sentence of Trades given the integer list of 
sentence = generate_sentence_from_grammar(inputs_three_trades , parser)
print(sentence)






