import shutil as sh
import sys
import os
from random import random
try : filename = sys.argv[1:][0]
except IndexError :
  print('File Name Not Provided!')
  exit()
file = open(filename,'r')
instructions = file.read()
strict = False
instructions = instructions.replace('{\n','{').replace('\\\n','').replace('?\n','?').replace('\n}','}').replace(',\n',',').replace(':\n',';').replace('\n',';').split(';')

file.close()
i = 0
cmd_cmdArgSep = '@_'
cmd_ArgSep = ' '
nullArgOp = '0'
safe = True
stopLoop = False
isFunctionRunning = False
c_argumentsObject = {}
c_funcData = {}
arthOp = '+-*/%<>~^|&!'
indentationMark = '  '
Vars = {'object':'<empty>','cache':'null'}
SuperVars = {'version':'pydi-5.0','auth':'yaver','i':None,'n1':-1,'returnee':None,'nl':'\n',
'cache' : '#CACHE', 'chn' : ':', 'bs' : '(','bc': ')'
}
Scopes = {}
UniversalFuncs = ['str','int','bool','len','complex','type','long','NOT','NEG','float','input','abs','typeOf','rand','list','split','of','replace','rsplit','trim','triml','trimr']
MathFuncs = ['sin','cos','tan','cot','cosec','sec','sqrt','gcd']
Functions =  {}
math = ''
operatorSeparator = '¢'
whichFunctionRunning = ''
warnings = True
WarningsObject = {'disableWarningMessage':'Simply Turn Off Warings By Runing "warnings False"'}
cachedExprs = {}
imports = []
libs = []
module_ext = '.hx.py'
moddir = 'modules'


Errors = [
  'UnknownError',
  'SizeNotDeclaredError',
  'DatabaseNotFoundError',
  'DatabaseCorruptedError',
  'UnsafeToProceed',
  'Value Not Of Given Type',
  'IllegalTypeError',
  'InvalidExpressionError',
  'InvalidCommandError',
  'SafeModeError',
  'File Was Not Found.',
  'Invalid Python.',
  'VaribleNotFound',
  'ArgumentsError',
  'Invalid Functional Group.',
  'Only command given.',
  'Function was not found.',
  'MismatchInArgumentsError',
  'NoArgumentsInGlobalError',
  'FunctionalStatementError',
  'InvalidArgumentError',
  'Cannot Delete Super Varibles. Super Varibles Are Immutable',
  'Arguments Are Not Avalible In Global Block.',
  'Object Was Not Found.',
  'Varible Was Not Found.',
  'Argument Was Not Found.',
  'Super Varible Was Not Found.',
  'Key Was Not Found.',
  'Arguments Not Formatted As Expected.',
  'Index Not Found In String.',
  'The Module Was Not Found.',
  'Illegal Name Of Module Given During Import.',
  'Module resulted in an error.'
]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    E = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def a2o(arr):
  obj = {}
  for i in range(0,len(arr)):
    obj[str(i)] = arr[i]
  return obj



def of(string,i):
  if(str(i).isdecimal()):
    i = int(i)
    if(i > len(string)):
      Error(29)
    else : return string[i]
  else: Error(5)



def Error(index,line = None):
  global i,safe
  line = line or i
  lenE = len(Errors[index])
  lenL = len(instructions[i-1])
  length = lenL + 16
  minlength =  lenE
  if(lenL > lenE):
    pass
  lineInfoLength = len('At : line' + str(line))
  ErrorString = f'''{length*'_'}__
|{' '*length}|
|{' '*length}|
| >>    "{instructions[line-1]}"    << |
|{' '*length}|
|{' '*length}|
|{' '*((length - lineInfoLength)//2)}At line {line} {' '*((length - lineInfoLength)//2)} |
|{' '*length}|
|{((bcolors.FAIL)+' '*((length - minlength)//2)) + Errors[index] + (" "*((length - minlength)//2)) + bcolors.E }|
|{' '*length}|
{length*'¯'}¯¯
'''
  print(ErrorString)
  #print('|' + ('¯¯'*(len(instructions[line-1]))+10) + '\n|\n|At :\n|\n|\n|>       '+instructions[line-1] +'      <\n|\n|\n|\n|',Errors[index],f'\n| : at line {line} on file {filename}  \n|' + ('__'*25) )
  if safe:
    print ("No Changes Made")
    exit()

NEG = lambda n:n*-1
NOT = lambda cond: not eval(parseExpr(str(cond)))
typeOf = lambda t: type(t).__name__
trim = lambda s: s.strip()
triml = lambda s: s.lstrip()
trimr = lambda s: s.rstrip()
rand = lambda i : random() * i
replace = lambda string,a,b: string.replace(a,b)
rsplit = lambda s,d,l = -1: a20(s.rsplit(d,l))
split = lambda s,d,l = -1: a2o(s.split(d,l))


def writeFile(args,data):
  filename =  eval(parseExpr(objectifyArgs(args)['f']))
  f = open(filename,'w')
  f.write(str(eval(parseExpr(data))))
  f.close()

def readFile(path):
  if(os.path.exists(path)):
    f = open(path,'r')
    data = f.read()
    f.close()
  else:
    Error(10)
    data = ''
  return data

def addVar(name,value,isGlobal,scope):
  if isGlobal:
    Vars[name] = value
  else:
    if not scope in Scopes:
      Scopes[scope] = {}
    Scopes[scope][name] = value

def createVar(arg,cmdArgs):
  argA = arg.split('=',1)
  if not ':' in argA[0]:  
    updateVar(arg)
    return
  varName = arg.split('=',1)[0].split(':',1)[1]
  varType = arg.split('=',1)[0].split(':',1)[0]
  varVal = eval(parseExpr(arg.split('=')[1]))
  isGlobal = True if cmdArgs == '0' else False
  scope = None if isGlobal else objectifyArgs(cmdArgs)['sc']
  try:
    if(varType == 'int'):
      addVar(varName,int(varVal),isGlobal,scope)
    elif(varType == 'str'):
      addVar(varName,str(varVal),isGlobal,scope)
    elif(varType == 'float'):
      addVar(varName,float(varVal),isGlobal,scope)
    elif(varType == 'bool'):
      varVal = False if varVal == 'False' else True
      addVar(varName,varVal,isGlobal,scope)
    else:
      Error(6)
  except:
    Error(5)


def removeSpaces(expr):
  expr = expr.split("'")
  i = 0
  while i < len(expr):
    if (i % 2 == 0): expr[i] = expr[i].replace(' ','')
    else : expr[i] = "'" + expr[i] + "'"
    i += 1
  return ''.join(expr)


def parseExpr(expr):
  exk = expr
  err = False
  current_ops = getOperators(expr)
  exprs = removeOperators(expr)
  for i in range(0,len(exprs)):
    exprObject = exprs[i].replace(')','(').split('(')
    startingBrackets = False
    exprIndex = None
    for j in range(0,len(exprObject)):
      if exprObject[j]:
        exprs[i] = exprObject[j]
        exprsIndex = j
        startingBrackets = True
      else:
        exprObject[j]= ')' if startingBrackets else '('
    if(exprs[i][0] == '$'):
      if(exprs[i][1] == '$'):
        if(exprs[i][2:] in SuperVars):
          exprs[i] = 'SuperVars["'+exprs[i][2:]+'"]'
        else:
          err = True
          Error(26)
      elif isFunctionRunning:
        if '..' in exprs[i]:
          exprs[i] = exprs[i][1:].split('..',1)
          exprs[i] = 'c_funcData[whichFunctionRunning]["c_argumentsObject"]["' + exprs[i][0] + '"]["' + str(eval(parseExpr(exprs[i][1]))) + '"]'
        elif('.' in exprs[i]):
          exprs[i] = exprs[i][1:].split('.',1)
          exprs[i] = 'c_funcData[whichFunctionRunning]["c_argumentsObject"]["' + exprs[i][0] + '"]["' + exprs[i][1] + '"]'
        else:
          exprs[i] = 'c_funcData[whichFunctionRunning]["c_argumentsObject"]["' + exprs[i][1:] + '"]'
      else:
        print(exprs[i])
        err = True
        Error(22)
    elif(exprs[i][0] == "'" and exprs[i][-1] == "'"):
      pass
    elif(exprs[i][0].isdecimal()):
      pass
    elif(exprs[i][0] == ':' and ':' != exprs[i][1] and exprs[i].count(':') % 2 == 0):
       func = exprs[i].split(':',2)[1]
       funcExpr = exprs[i].split(':',2)[2]
       exprs[i] = parseFunclExpr(func,funcExpr)
    elif('..' in exprs[i] and '..' != exprs[i][0:2]):
       exprs[i] = exprs[i].split('..')
       if(exprs[i][0] in Scopes):
         if (eval(parseExpr(exprs[i][1])) in Scopes[exprs[i][0]]):
           exprs [i] = 'Scopes["' + exprs[i][0] +'"][' + parseExpr(exprs[i][1]) + ']'
         else:
           Error(27)
           err = True
           exprs[i] = ''
       else:
         err = True
         Error(23)
         exprs[i] = ''
    elif('.' in exprs[i] and '.' != exprs[i][0]):
      exprs[i] = exprs[i].split('.')
      if (exprs[i][0] in Scopes):
        if (exprs[i][1] in Scopes[exprs[i][0]]):
          exprs[i] = 'Scopes["' + exprs[i][0] + '"]["' + exprs[i][1] + '"]'
        else:
          exprs[i] = ''
          err = True
          Error(27)
      else:
        Error(23)
        err = True
        exprs[i] = ''
    elif(exprs[i] == 'False' or exprs[i] == 'True'):
      pass
    elif exprs[i][0] == '{' and exprs[i][-1] == '}':
      if(exprs[i][1:-1] in Scopes):
        exprs[i] = 'Scopes["' + exprs[i][1:-1] + '"]'
      else:
        Error(23)
        err = True
    else:
      if exprs[i] in Vars:
        exprs[i] = 'Vars["'+exprs[i]+'"]'
      else:
        Error(24)
        err = True
    exprObject[exprsIndex] = exprs[i]
    exprs[i] =  ''.join(exprObject)
  expr = ''
  for i in range(0,len(exprs)):
    expr += exprs[i]
    if i<len(current_ops):
      expr += current_ops[i]
  if 'int(input(' in expr and warnings:
    print(f'{bcolors.WARNING}Warning{bcolors.E}: Tried to convert uncontrolled user input into type `int`, most probably going to result in an error if not handled properly. To Disable ' + WarningsObject['disableWarningMessage'])
  return '""' if err else expr



def parseFunclExpr(func,expr):

  global math
  expr = expr.split(",")
  for i in range(0,len(expr)):
    expr[i] = eval(parseExpr(expr[i]))
    if(typeOf(expr[i]) == 'str'):
      expr[i] = '"' + expr[i] + '"'
    elif(typeOf(expr[i]) in ['float','int','bool']):
      expr[i] = str(expr[i])
    
  expr = ','.join(expr)
  if(func in UniversalFuncs):
    return f'{func}({expr})'
  elif func in MathFuncs:
    if not math: import math
    return f'math.{func}({expr})'
  else:
    Error(14)



def printOut(arg):
  try:
    print(eval(parseExpr(arg)))
  except KeyError:
    Error(12)
  except Exception as e:
    print(e)
    Error(7)

def getOperators(expr):
  operators = []
  string = False
  for c in expr:
    if c == "'": string = not string
    if string : continue
    if c in arthOp:
      if(c == '|'):
        operators.append(' or ')
      elif(c == '~'):
        operators.append(' == ')
      elif(c == '^'):
        operators.append(' != ')
      elif(c == '&'):
        operators.append(' and ')
      else:
        operators.append(c)
    
  return operators


def removeOperators(expr):
  string = False
  exprList = list(expr)
  for c in exprList:
    if c == "'" : string = not string
    if string : continue
    if c in arthOp:
      expr = expr.replace(c,operatorSeparator)
  return expr.split(operatorSeparator)


def objectifyArgs(args):
  if(args == '0'):
      return {}
  args = args.split(',')
  args_t = {}
  for j in range(0,len(args)):
      args_t[args[j].split(':',1)[0]] = args[j].split(':',1)[1]
  return args_t


def Function(args,instrs):
  return {'args':args,'instrs':instrs}

def createDb(name,dbArgs):
  name = eval(parseExpr(name))
  if(os.path.exists(name)):
    sh.rmtree(name)
  os.mkdir(name)
  open(name + '/index.db','w')
  if dbArgs and dbArgs != nullArgOp:
    dbArgs = objectifyArgs(dbArgs)
    if(dbArgs['r'] and dbArgs['c']):
      f = open(name + '/size.native','w')
      f.write(dbArgs['r']+',')
      f.write(dbArgs['c'])
      f.close()

def initDbStruc(path):
  global i
  if os.path.exists(path+'/size.native'):
    f = open(path+'/size.native','r')
    f.close()
    sizes = f.read().split(',')
    r = sizes[0]
    c = sizes[1]
    # Tobe Created
  else:
    Error(1)

def parsePrimitveObject(pre_obj):
  pre_obj = pre_obj[1:-1].split(',')
  obj = {}
  for i in range(0,len(pre_obj)):
    if(':' in pre_obj[i]):
      pre_obj[i] = pre_obj[i].split(':')
      obj[pre_obj[i][0]] = eval(parseExpr(pre_obj[i][1]))
    else:
      if(pre_obj[i][0:2] == '$$'):
        if pre_obj[i][2:] in SuperVars:
          obj[pre_obj[i]] = SuperVars[pre_obj[i][2:]]
        else:
          Error(26)
      else:
        if pre_obj[i] in Vars:
          obj[pre_obj[i]] = Vars[pre_obj[i]]
        else:
          Error(24)
  return obj 

def updateObject(arg):
  arg = arg.split('=',1)
  objectName = arg[0]
  objectValue = arg[1]
  if not objectName in Scopes:
    Scopes[objectName] = {}
    Scopes[objectName] = parsePrimitveObject(objectValue)
  else:
    Scopes[objectName].update(parsePrimitveObject(objectValue))



def openInDb(db,path):
  global i
  if os.path.exists(db):
    if os.path.exists(db + '/' + path):
      f = open(db + '/' + path,'r')
      return  f
    else:
      Error(3)
  else:
    Error(2)
 
def updateVar(arg):
  varName = arg.split('=')[0]
  varVal = arg.split('=')[1]
  if '..' in varName and varName[0:2] != '..':
    varName = varName.split('..')
    if not varName[0] in Scopes : Scopes[varName[0]] = {}
    Scopes[varName[0]][eval(parseExpr(varName[1]))] = eval(parseExpr(varVal))
    return
  elif '.' in varName and varName[0] != '.':
    varName = varName.split('.')
    if not varName[0] in Scopes : Scopes[varName[0]] = {}
    Scopes[varName[0]][varName[1]] = eval(parseExpr(varVal))
    return
  addVar(varName,eval(parseExpr(varVal)),True,'')
  

def writeToDb(args,value):
  db = args['db']
  f = openInDb(db,'index.db')
  if(f != None):
    f = f.read()
    if(not f):
      initDbStruc(db)

def read(cmdArgs,arg):
  arg = eval(parseExpr(arg))
  if 'v' in objectifyArgs(cmdArgs):
    addVar(objectifyArgs(cmdArgs)['v'],readFile(arg),True,'')
  else:
    SuperVars['returnee'] = readFile(arg)

def condLoop(arg):
  global i,warnings
  if warnings and (arg in ['True','False']) : print(f"Warining : Condition '{arg}' is always going to be {arg}. @ 'while {arg}' at line {i} . To supress the warning use ({arg})")
  cond = parseExpr(arg)
  z = i
  if not eval(cond):
    for j in range(z,len(instructions)):
      if (instructions[j][0:2] != '  ' and len(instructions[j].strip()) != 0) or len(instructions)-1 == j:
        i = j
        return
  else:
    while(eval(cond)):
      for j in range(z,len(instructions)):
        if instructions[j][0:2] != '  ' and len(instructions[j].strip()) != 0:
          i = j
          break
        else:
          instr = parseInstructions(instructions[j].lstrip())
          if stopLoop: 
            i = len(instructions) + i - 1
            return
          execute(instr['cmd'],instr['cmdArgs'],instr['arg'])
        i = j + 1 if len(instructions) == int(j)+1 else i

def loop(count):
  if '||' in count:
    count = count.split('||',2)
    jump = eval(parseExpr(count[1]))
    count = count[0]
  else:
    jump = 1
  count = int(eval(parseExpr(count)))
  currentLoopInstr = []
  gi = 0
  SuperVars['n'] = 1
  if isFunctionRunning:
    global whichFunctionRunning,stopLoop
    c_funcData[whichFunctionRunning]['c_blockIndex'] += 1
    for j in range(c_funcData[whichFunctionRunning]['c_blockIndex'],len(c_funcData[whichFunctionRunning]['instrs'])):
      if c_funcData[whichFunctionRunning]['instrs'][j][2:4] == '  ':
        currentLoopInstr.append(c_funcData[whichFunctionRunning]['instrs'][j][2:])
        c_funcData[whichFunctionRunning]['c_blockIndex'] = j - 1
      else : 
        c_funcData[whichFunctionRunning]['c_blockIndex'] = j - 1
        break
  else:
    global i
    while i < len(instructions):
      if instructions[i][0:2] != '  ' and len(instructions[i].replace(' ','')) != 0:
        break
      currentLoopInstr.append(instructions[i])
      i += 1
  for j in range(0,int(count)):
    SuperVars['i'] = gi
    for k in range(0,len(currentLoopInstr)):
      instr = parseInstructions(currentLoopInstr[k].lstrip())
      if stopLoop :
        stopLoop = False
        return
      execute(instr['cmd'],instr['cmdArgs'],instr['arg'])
    gi += jump
  SuperVars['i'] = None

def createFunction(arg):
  if ':' in arg:
    name = arg.split(':',1)[0]
    params = arg.split(':',1)[1].split(',')
  else:
    name = arg
    params = []
  instrs = []
  global i
  while i < len(instructions):
    if instructions[i][0:2] != '  ' and len(instructions[i].replace(' ','')) != 0: break
    instrs.append(instructions[i])
    i += 1
  Functions[name] = Function(params, instrs)



def delete(arg):
  if(arg[0] == '$'):
    if(arg[1] == '$'):
      Error(21)
    elif isFunctionRunning:
      if(arg[1:] in c_funcData[whichFunctionRunning]['c_argumentsObject']):
        del c_funcData[whichFunctionRunning]['c_argumentsObject'][arg[1:]]
      else:
        Error(25)
    elif not isFunctionRunning:
      Error(22)
  elif(arg[0] == '{' and arg[-1] == '}'):
    if(arg[1:-1] in Scopes):
      del Scopes[arg[1:-1]]
    else:
      Error(23)
  else:
    if(arg in Vars):
      del Vars[arg]
    else:
      Error(24)
      

def call(arg,cmdArgs):
  global c_argumentsObject,isFunctionRunning,c_funcData,whichFunctionRunning
  if ':' in arg:
    name = arg.split(':',1)[0]
    arguments = arg.split(':',1)[1]
    if ('=') in arguments : 
      arguments = arguments.rsplit('=',1)
      varible = arguments[1]
      arguments = arguments[0].split(',')
    else:
      varible = None
      arguments = arguments.split(',')
  else:
    if '=' in arg:
      arg = arg.rsplit('=',1)
      varible = arg[1]
      name = arg[0]
    else:
      name = arg
      varible = None
    arguments = []
    
  if not name in Functions:
    Error(16)
    return
  whichFunctionRunning = name
  c_funcData[name] = Functions[name]
  if len(c_funcData[name]['args']) != len(arguments):
    Error(17)
    return
  isFunctionRunning = True
  whichFunctionRunning = name
  c_funcData[name]['c_argumentsObject'] = {}
  for i in range(0, len(arguments)):
    c_funcData[name]['c_argumentsObject'][c_funcData[name]['args'][i]] = eval(parseExpr(arguments[i]))
  c_funcData[whichFunctionRunning]['c_blockIndex'] = 0
  while c_funcData[name]['c_blockIndex'] < len(c_funcData[name]['instrs']):
    whichFunctionRunning = name
    instr = parseInstructions(c_funcData[name]['instrs'][c_funcData[name]['c_blockIndex']].lstrip())
    if instr['cmd'] == 'return':
      if varible:
        Vars[varible] = eval(parseExpr(instr['arg']))
      else:
        SuperVars['returnee'] = eval(parseExpr(instr['arg']))
      isFunctionRunning = False
      c_argumentsObject = {}
      c_funcData[name] = {}
      return
    execute(instr['cmd'],instr['cmdArgs'],instr['arg'])
    isFunctionRunning = True
    c_funcData[name]['c_blockIndex'] += 1
  isFunctionRunning = False
  c_argumentsObject = {}
  c_funcData[name] = {}

def terinary(arg):
  arg = arg.split('?')
  cond = eval(parseExpr(removeSpaces(arg[0])))
  toBeExecuted = 1 if cond else 2
  arg[toBeExecuted] = arg[toBeExecuted].split(',')
  for i in range(0,len(arg[toBeExecuted])):
    instrs = parseInstructions(arg[toBeExecuted][i].strip())
    execute(instrs['cmd'],instrs['cmdArgs'],instrs['arg'])

def init_cond_statement(cond):
  pass

def exitProgram(arg):
  if not arg in ['force','program','block','function','loop']:
    Error(20)
    return
  if(arg == 'program'):
    if not safe : exit()
    else :
      print('Failed To Exit. Try turning off safe mode first.')
      return
  elif arg == 'loop':
    global stopLoop
    stopLoop = True

def as_obj(arg):
  try:
    arg = arg.split('=',1)
    value = eval(parseExpr(arg[1]))
    if(type(value).__name__  == 'dict'):
      Scopes[arg[0]] = value
    else:
      Error(5)
  except:
    Error(28)


def expression(arg):
  arg = removeSpaces(arg)
  if('+=' in arg): arg = [arg.split('+=',1),'+=']
  elif('-=' in arg): arg = [arg.split('-=',1),'-=']
  elif('*=' in arg): arg = [arg.split('*=',1),'*=']
  elif('/=' in arg): arg = [arg.split('/=',1),'/=']
  elif('=' in arg): arg = [arg.split('=',1),'=']
  else:
    try:
      SuperVars['returnee'] = eval(parseExpr(arg))
    except:
      Error(8)
      return
  var = arg[0][0]
  expr = arg[0][1]
  operator = arg[1]
  if len(operator) == 2:
    expression = var + "=" + var + operator[0] + expr
  else:
    expression = var + "=" + expr
  updateVar(expression)

def import_module(module_name):
  if('/' in module_name or '\\' in module_name):
    Error(31)
    return
  module = readFile(moddir + '/' + module_name + module_ext)
  try:
    exec(module,globals(),globals())
    libs.append(module_name)
  except Exception as e:
    Error(32)
  
  
def createLambda(arg):
  arg = arg.split(':',2)
  name = arg[0]
  arguments = arg[1].split(',')
  if len(arguments) == 1 and arguments[0] == '' : arguments = []
  expression = ['return ' + arg[2]]
  Functions[name] = Function(arguments, expression)
  

def execute(cmd,cmdArgs,arg):
  global safe,warnings,moddir
  if(cmd == 'pass'):
    pass
  elif(cmd == 'var'):
    createVar(arg,cmdArgs)
  elif(cmd in ['print','>>']):
    printOut(arg)
  elif(cmd == 'safe'):
    safe = False if arg == 'False' else True
  elif(cmd == 'py'):
    try:
      Error(9) if safe else exec(eval(parseExpr(arg)))
    except:
      Error(11)
  elif(cmd == 'import'):
    import_module(arg)
  elif(cmd == 'read'):
    read(cmdArgs,arg)
  elif(cmd == 'write'):
    writeFile(cmdArgs,arg)
  elif(cmd == 'type'):
    print(typeOf(eval(parseExpr(arg))))
  elif(cmd == 'loop'):
    loop(arg)
  elif(cmd in ['$','update','let']):
    updateVar(arg)
  elif(cmd == 'while'):
    condLoop(arg)
  elif(cmd == 'printE'):
    print(parseExpr(arg))
  elif(len(cmd) > 0 and cmd[0] == '#'):
    pass
  elif(cmd in ['=>','lambda','Ⲗ']):
    createLambda(arg)
  elif(cmd == 'BLOCK'):
    createFunction(arg)
  elif(cmd == 'CALL' or cmd == '()'):
    call(arg,cmdArgs)
  elif(cmd in ['{}','object']):
    updateObject(arg)
  elif(cmd in ['if','?']):
    terinary(arg)
  elif(cmd in ['end','exit']):
    exitProgram(arg)
  elif(cmd == 'warnings'):
    warnings = eval(parseExpr(arg))
  elif(cmd == "@"):
    if warnings : print('"Warning : @ ' + arg + '" cannot do : To Supress ' + WarningsObject['disableWarningMessage'])
  elif(cmd == 'del'):
    delete(arg)
  elif(cmd == 'obj'):
    as_obj(arg)
  elif(cmd == 'moddir'):
    moddir = str(eval(parseExpr(arg)))
  elif(cmd == 'str'):
    addVar(arg.split('=',1)[0],arg.split('=',1)[1][1:-1] ,True,'')
  elif (cmd in imports):
    eval(cmd+'(arg)')
  else:
    expression(cmd + arg)


def parseInstructions(instruction):
  global i
  try:
    if not instruction.strip():
      return {'cmd':'#','arg':'5','cmdArgs':0}
    cmd = instruction.split(cmd_ArgSep,1)[0]
    if not cmd in ['?','if'] :
      arg = removeSpaces(instruction.split(cmd_ArgSep,1)[1])
    else:
      arg = instruction.split(cmd_ArgSep,1)[1]
    if len(cmd.split(cmd_cmdArgSep)) == 2:
      cmdArgs = cmd.split(cmd_cmdArgSep)[1]
      cmd = cmd.split(cmd_cmdArgSep)[0]
    else:
      cmdArgs = '0'
  except:
    Error(15,i+1)
    return {'cmd':'#','arg':'5','cmdArgs':0}
  return {'cmd':cmd,'arg':arg,'cmdArgs':cmdArgs}

while i < len(instructions):
  parsedInstr = parseInstructions(instructions[i])
  cmd = parsedInstr['cmd']
  cmdArgs = parsedInstr['cmdArgs']
  arg = parsedInstr['arg']
  i += 1
  execute(cmd,cmdArgs,arg)
