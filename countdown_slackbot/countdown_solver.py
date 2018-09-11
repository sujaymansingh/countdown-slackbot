class InvalidExpressionError(ValueError):
    pass

subtract = lambda x,y: x-y
def add(x,y):
    if x<=y: return x+y
    raise InvalidExpressionError
def multiply(x,y):
    if x<=y or x==1 or y==1: return x*y
    raise InvalidExpressionError
def divide(x,y):
    if not y or x%y or y==1:
        raise InvalidExpressionError
    return x/y

add.display_string = '+'
multiply.display_string = '*'
subtract.display_string = '-'
divide.display_string = '/'

standard_operators = [ add, subtract, multiply, divide ]

class Expression(object): pass

class TerminalExpression(Expression):
    def __init__(self,value,remaining_sources):
        self.value = value
        self.remaining_sources = remaining_sources
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self.value)

class BranchedExpression(Expression):
    def __init__(self,operator,lhs,rhs,remaining_sources):
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs
        self.value = operator(lhs.value,rhs.value)
        self.remaining_sources = remaining_sources
    def __str__(self):
        return '('+str(self.lhs)+self.operator.display_string+str(self.rhs)+')'
    def __repr__(self):
        return self.__str__()

def ValidExpressions(sources,operators=standard_operators,minimal_remaining_sources=0):
    for value, i in zip(sources,range(len(sources))):
        yield TerminalExpression(value=value, remaining_sources=sources[:i]+sources[i+1:])
    if len(sources)>=2+minimal_remaining_sources:
        for lhs in ValidExpressions(sources,operators,minimal_remaining_sources+1):
            for rhs in ValidExpressions(lhs.remaining_sources, operators, minimal_remaining_sources):
                for f in operators:
                    try: yield BranchedExpression(operator=f, lhs=lhs, rhs=rhs, remaining_sources=rhs.remaining_sources)
                    except InvalidExpressionError: pass

def TargetExpressions(target,sources,operators=standard_operators):
    for expression in ValidExpressions(sources,operators):
        if expression.value==target:
            yield expression

def FindFirstTarget(target,sources,operators=standard_operators):
    for expression in ValidExpressions(sources,operators):
        if expression.value==target:
            return expression
    raise IndexError, "No matching expressions found"

def SolveProblem(target, numbers):
    import time
    start_time = time.time()
    target_expressions = list(TargetExpressions(target, numbers))
    target_expressions.sort(lambda x,y:len(str(x))-len(str(y)))
    return target_expressions[0]
    print "Found",len(target_expressions),"solutions, minimal string length was: "
    print target_expressions[0],'=',target_expressions[0].value
    print
    print "Took",time.time()-start_time,"seconds."
