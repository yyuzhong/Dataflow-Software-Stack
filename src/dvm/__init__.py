# __init__.py
# Mathijs Saey
# dvm

# The MIT License (MIT)
#
# Copyright (c) 2013, 2014 Mathijs Saey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import instructions
import runtime
import tokens

from instructions 	import addOperationInstruction, addSink, addStopInstruction, addContextChange, addContextRestore
from runtime 		import run

def addLiteral(inst, port, value):
	t = tokens.createLiteral(inst, port, value)
	runtime.addToken(t)

def bindCall(inst, func, funcRet):
	inst = instructions.getInstruction(inst)
	inst.bind(func, funcRet)

def addDestination(srcKey, srcPort, dstKey, dstPort):
	inst = instructions.getInstruction(srcKey)
	inst.addDestination(srcPort, dstKey, dstPort)


## TEST CODE ##


def tOP(a,b):
	return a + b

# function
fStart = addSink()
body = addOperationInstruction(tOP, 2)
fEnd = addContextRestore()

addDestination(fStart, 0, body, 0)
addDestination(fStart, 1, body, 1)
addDestination(body, 0, fEnd, 0)

# call
ret = addSink()
call = addContextChange(ret)
pEnd = addStopInstruction()

bindCall(call, fStart, fEnd)
addDestination(ret, 0, pEnd, 0)

addLiteral(call, 0, "top")
addLiteral(call, 1, "kek")

run()

