import os
import shutil as sh
file = open('db.str.py','r')
instructions = file.read().split('\n')
file.close()
i = 0
cmd_cmdArgSep = '@_'
cmd_ArgSep = ' '
nullArgOp = '0'
safe = False
arthOp = '+-*/%<>~^|&!'
indentationMark = '--'
Vars = {}
SuperVars = {'test':0,'version':'pydi-1.4.alpha','auth':'yaver','i':None}
Scopes = {}
UniversalFuncs = ['str','int','bool','len','complex','type','long','NOT','NEG','float']

Errors = [
  'UnknownError',
  'SizeNotDeclaredError',
  'DatabaseNotFoundError',
  'DatabaseCorruptedError',
  'UnsafeToProceed',
  'ValueNotOfGivenTypeError',
  'IllegalTypeError',
  'InvalidExpressionError',
  'InvalidCommandError',
  'SafeModeError',
  'FileNotFoundError',
  'InvalidPython',
  'VaribleNotFound',
  'ArgumentsError',
  'InvalidFunctionalGroupError'

]


def Error(index):
  global i,safe
  print('\n\nAt : "'+instructions[i-1]+'"\n',Errors[index],f'\n : at line {i}')
  if safe:
    print ("No Changes Made")
    exit()

NEG = lambda n:n*-1
  

NOT = lambda cond: not eval(parseExpr(str(cond)))
  
def writeFile(args,data):
  f = open(objectifyArgs(args)['f'],'w')
  f.write(str(eval(parseExpr(data.replace('_',' ')))))
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
  varName = arg.split('=')[0].split(':')[1]
  varType = arg.split('=')[0].split(':')[0]
  varVal = arg.split('=')[1]
  isGlobal = True if cmdArgs == '0' else False
  scope = None if isGlobal else objectifyArgs(cmdArgs)['scope']
  try:
    if(varType == 'int'):
      addVar(varName,int(varVal),isGlobal,scope)
    elif(varType == 'str'):
      addVar(varName,varVal.replace('_',' '),isGlobal,scope)
    elif(varType == 'float'):
      addVar(varName,float(varVal),isGlobal,scope)
    elif(varType == 'bool'):
      varVal = False if varVal == 'False' else True
      addVar(varName,varVal,isGlobal,scope)
    else:
      Error(6)
  except:
    Error(5)

def parseExpr(expr):
  err = False
  current_ops = getOperators(expr)
  exprs = removeOperators(expr)
  for i in range(0,len(exprs)):
    if(exprs[i][0] == '$'):
      if(exprs[i][1] == '$'):
        exprs[i] = 'SuperVars["'+exprs[i].replace('$','')+'"]'
      else:
        exprs[i] = 'Vars["'+exprs[i].replace('$','')+'"]'
    elif(exprs[i][0] == "'" and exprs[i][-1] == "'"):
      exprs[i] = exprs[i].replace('_',' ')
    elif(exprs[i][0].isdecimal()):
      pass
    elif(exprs[i][0] == ':' and ':' != exprs[i][1] and exprs[i].count(':') % 2 == 0):
       func = exprs[i].split(':',2)[1]
       funcExpr = exprs[i].split(':',2)[2]
       exprs[i] = parseFunclExpr(func,funcExpr)
    elif('@' in exprs[i]):
      exprs[i] = 'Scopes["' + exprs[i].replace('@','"]["') + '"]'
    elif(exprs[i] == 'False' or exprs[i] == 'True'):
      pass
    else:
      Error(7)
      err = True
  expr = ''
  for i in range(0,len(exprs)):
    expr += exprs[i]
    if i<len(current_ops):
      expr += current_ops[i]
  return '""' if err else expr


def parseFunclExpr(func,expr):
  if(not func in UniversalFuncs):
    Error(14)
  if(func == 'int'):
    return f'{func}({parseExpr(expr)}' + '''.replace("'"," "))'''
  return f'{func}({parseExpr(expr)})'

def printOut(arg):
  try:
    print(eval(parseExpr(arg)))
  except KeyError:
    Error(12)
  except :
    Error(7)

def getOperators(expr):
  operators = []
  for c in expr:
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
  for c in arthOp:
    expr = expr.replace(c,',')
  return expr.split(',')


def objectifyArgs(args):
  if(args == '0'):
      return {}
  args = args.split(',')
  args_t = {}
  for j in range(0,len(args)):
      args_t[args[j].split(':')[0]] = args[j].split(':')[1]
  return args_t


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

def loop(count):
  count = int(eval(parseExpr(count)))
  currentLoopInstr = []
  gi = 0
  global i
  while i < len(instructions):
    if instructions[i][0:2] != '--':
      break
    currentLoopInstr.append(instructions[i])
    i += 1
  for j in range(0,int(count)):
    SuperVars['i'] = gi
    for k in range(0,len(currentLoopInstr)):
      instr = parseIntdCommands(currentLoopInstr[k])
      execute(instr['cmd'],instr['cmdArgs'],instr['arg'])
    gi += 1
  SuperVars['i'] = None

def parseIntdCommands(instruction):
 instruction = instruction[2:]
 cmd = instruction.split(cmd_ArgSep)[0]
 arg = instruction.split(cmd_ArgSep)[1].replace(' ','')
 if len(cmd.split(cmd_cmdArgSep)) == 2:
    cmdArgs = cmd.split(cmd_cmdArgSep)[1]
    cmd = cmd.split(cmd_cmdArgSep)[0]
 else:
    cmdArgs = '0'
 return {'cmd':cmd,'arg':arg,'cmdArgs':cmdArgs}
 
def updateVar(arg):
  varName = arg.split('=')[0]
  varVal = arg.split('=')[1]
  addVar(varName,eval(parseExpr(varVal)),True,'')
  

def writeToDb(args,value):
  db = args['db']
  f = openInDb(db,'index.db')
  if(f != None):
    f = f.read()
    if(not f):
      initDbStruc(db)

def read(cmdArgs,arg):
  if 'v' in objectifyArgs(cmdArgs):
    addVar(objectifyArgs(cmdArgs)['v'],readFile(arg),True,'')
  else:
    print(readFile(arg))

def condLoop(arg):
  global i
  cond = parseExpr(arg)
  if not eval(cond):
    while i < len(instructions):
      if not instructions[i][0:2] == '--':
        break
      i += 1
  else:
    z = i
    while(eval(cond)):
      for j in range(z,len(instructions)):
        if not instructions[j][0:2] == '--':
          i = j
          break
        else:
          instr = parseIntdCommands(instructions[j])
          execute(instr['cmd'],instr['cmdArgs'],instr['arg'])
        i = j + 1 if len(instructions) == int(j)+1 else i
      

def execute(cmd,cmdArgs,arg):
  global safe
  if(cmd == 'createDb'):
    createDb(arg,cmdArgs)
  elif(cmd == 'wDb'):
    writeToDb(objectifyArgs(cmdArgs),arg)
  elif(cmd == 'var'):
    createVar(arg,cmdArgs)
  elif(cmd == 'print'):
    printOut(arg)
  elif(cmd == 'safeMode'):
    safe = False if arg == 'False' else True
  elif(cmd == 'py'):
    try:
      Error(9) if safe else exec(eval(parseExpr(arg)))
    except:
      Error(11)
  elif(cmd == 'read'):
    read(cmdArgs,arg)
  elif(cmd == 'write'):
    writeFile(cmdArgs,arg)
  elif(cmd == 'type'):
    print(type(eval(parseExpr(arg))))
  elif(cmd == 'loop'):
    loop(arg)
  elif(cmd == 'update' or cmd == 'let' or cmd == '$'):
    updateVar(arg)
  elif(cmd == 'while'):
    condLoop(arg)
  elif(cmd == 'printE'):
    print(parseExpr(arg))
  elif(cmd == '#'):
    pass
  else:
    Error(8)
    print(cmd)

while i < len(instructions):
  if len(instructions[i].replace(' ','')) == 0:
      i += 1
      continue
  cmd = instructions[i].split(cmd_ArgSep,1)[0]
  arg = instructions[i].split(cmd_ArgSep,1)[1].replace(' ','')
  if len(cmd.split(cmd_cmdArgSep)) == 2:
    cmdArgs = cmd.split(cmd_cmdArgSep)[1]
    cmd = cmd.split(cmd_cmdArgSep)[0]
  else:
    cmdArgs = '0'
  i += 1
  execute(cmd,cmdArgs,arg)
