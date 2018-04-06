#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        logical_expression
# Purpose:     Contains logical_expression class, inference engine,
#              and assorted functions
#
# Created:     09/25/2011
# Last Edited: 07/22/2013  
# Notes:       *This contains code ported by Christopher Conly from C++ code
#               provided by Dr. Vassilis Athitsos
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so put it in a list which is
#               passed by reference. We can also now pass just one variable in
#               the class and the function will modify the class instead of a
#               copy of that variable. So, be sure to pass the entire list to a
#               function (i.e. if we have an instance of logical_expression
#               called le, we'd call foo(le.symbol,...). If foo needs to modify
#               le.symbol, it will need to index it (i.e. le.symbol[0]) so that
#               the change will persist.
#              *Written to be Python 2.4 compliant for omega.uta.edu
#-------------------------------------------------------------------------------

import sys
from copy import copy

#-------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos
class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []


def print_expression(expression, separator):
    """Prints the given expression using the given separator"""
    if expression == 0 or expression == None or expression == '':
        print '\nINVALID\n'

    elif expression.symbol[0]: # If it is a base case (symbol)
        sys.stdout.write('%s' % expression.symbol[0])

    else: # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':  # It's the beginning of a connective
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print '\nUnexpected end of input.\n'
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    word = ''
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):
    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
         expression.connective[0].lower() != 'or' and \
         expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
#-------------------------------------------------------------------------------

# Add all your functions here

# Reading all Symbols
def readingSymbols(expression, symbols):

    if expression.symbol[0]:
        symbols.append(expression.symbol[0])
    for subexpression in expression.subexpressions:
        readingSymbols(subexpression, symbols)

# Extending the symbols along with the model.
def extend(model, symb, value):

    model[symb] = value
    return model


# TT Check for all the function
# Pseudo Code
# function TTCheckall with KB, alpha, symbols, model as parameters
# if symbols empty
#   if PLTRUE with KB, Model then PLTRUE with alpha,model
#   else return true #when KB is false, always return true
# else do
#   p = first symbols  
#   rest = rest symbols
# return TTCheckall with KB, alpha, rest, model union p = true and TTCheckall with KB, alpha, rest, model union p = false

def ttCheckAll(knowledgeBase,alpha,symbols, model):

    if not symbols:
        if plTrue(knowledgeBase, model):
            return plTrue(alpha, model)
        else:
            return True
    pi = symbols[0]
    re = symbols[1:]
    return ttCheckAll(knowledgeBase, alpha, re, extend(model,pi,True) ) \
            and ttCheckAll(knowledgeBase, alpha, re, extend(model,pi,False))

# Inorder to check all the connectives like or, and, not, if, iff, xor
def plTrue(expression, model):

    if expression.connective[0].lower() == 'or':
        flags = True
        for f, subexpression in enumerate(expression.subexpressions):
            if(f == 0):
                flags = plTrue(subexpression, model)
                continue;
            flags = flags or plTrue(subexpression, model)
        return flags

    elif expression.connective[0].lower() == 'and':
        flags = True
        for f, subexpression in enumerate(expression.subexpressions):
            if(f == 0):
                flags = plTrue(subexpression, model)
                continue;
            flags = flags and plTrue(subexpression, model)
        return flags

    elif expression.connective[0].lower() == 'not':
        flags = not plTrue(expression.subexpressions[0], model)
        return flags

    elif expression.connective[0].lower() == 'if':
        expression1 = plTrue(expression.subexpressions[0], model)
        expression2 = plTrue(expression.subexpressions[1], model)
        return ((not expression1) or expression2)

    elif expression.connective[0].lower() == 'iff':
        expression1 = plTrue(expression.subexpressions[0], model)
        expression2 = plTrue(expression.subexpressions[1], model)
        return ((not expression1) or expression2) and ((not expression2) or expression1)

    elif expression.connective[0].lower() == 'xor':
        flags = True
        for f, subexpression in enumerate(expression.subexpressions):
            if(f == 0):
                flags = plTrue(subexpression, model)
                continue;
            flags = flags ^ plTrue(subexpression, model)
        return flags
    return model[expression.symbol[0]] \

# function TTEntails with KB, alpha returns true or false
# inputs - KB, the knowledge base, a sentence in propositional logic
# alpha, the query, a sentence in propositional logic
# symbols - a list of the propositional symbols in KB and alpha
# return TTCheckall with KB, alpha, symbols, empty model

# Inorder to check the symbols and statements with knowledge base,this TT Entails does that.
def TTEntails(knowledge_base, statement, negationStatement, symbolsList):
    
    try:
        outputFile = open('result.txt','w')
    except:
        print('Output file creation failed')
    knowledgeBase1 = []
    symbol1 = []
    model = symbolsList.copy();
    readingSymbols(knowledge_base, knowledgeBase1)
    readingSymbols(statement, symbol1)
    knowledgeBase1 = list(set(knowledgeBase1))
    symbol1 = list(set(symbol1))
    knowledgeBase1.extend(symbol1)
    symbols = list(set(knowledgeBase1))
    for symbl in model.keys():
        try:
            symbols.remove(symbl)
        except Exception:
            pass
    statementTrue = ttCheckAll(knowledge_base,statement,symbols,model)
    statementFalse = ttCheckAll(knowledge_base,negationStatement,symbols,model)
    if statementTrue == True and statementFalse == True:
        outputFile.write('Both True and False')
        print 'Both True and False'
    elif statementTrue == True and statementFalse == False:
        outputFile.write('Definitely True')
        print 'Definitely True'
    elif statementTrue == False and statementFalse == True:
        outputFile.write('Definitely False')
        print 'Definitely False'
    elif statementTrue == False and statementFalse == False:
        outputFile.write('Possibly True, Possibly False')
        print 'Possibly True, Possibly False'
    else:
        outputFile.write('Error')
    print
    outputFile.close()

         