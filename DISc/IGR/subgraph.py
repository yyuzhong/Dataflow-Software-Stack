# subgraphs.py
# Mathijs Saey
# DISc

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

##
# \package IGR.subgraph
# \brief SubGraph definitions
# 
# IGR subgraphs. 
##

##
# SubGraph
# 
# An IGR subgraph is either a function body,
# or a part of the compound node. 
#
##
class SubGraph(object):

	def __init__(self, entry, exit, name, isFunc):
		super(SubGraph, self).__init__()
		self.name   = name
		self.entry  = entry
		self.exit   = exit
		self.nodes  = []
		self.value  = None
		self.isFunc = isFunc

	##
	# Printable subgraph
	##
	def __str__(self):
		pair = "(" + str(self.entry) + " | " + str(self.exit) + ")"
		return "'" + self.name + "' " + "subgraph " + pair

	##
	# Get an output port of the subgraph. 
	# This maps to the ports of the entry node.
	#
 	# This may seem counterintuitive, but this is seen
	# from the perspective of the inside of the subgraph.
	# In which case the output port is used to retrieve data
	# from the subgraph.
	##
	def getOutputPort(self, idx):
		return self.entry.getOutputPort(idx)

	##
	# Gets an input port of the subgraph.
	# This maps to the input of the return (exit) node.
	#
	# Once again this is seen from the inside of the subgraph.
	# If we want to add data to the subgraph, we try to return it
	# to the outside world, which is done through the exit node.
	##
	def getInputPort(self, idx):
		return self.exit.getInputPort(idx)

	##
	# Add a node to the node list of the
	# subgraph.
	##
	def addNode(self, node):
		self.nodes.append(node)

	##
	# See if a graph can be reduced to a 
	# constant value.
	##
	def isTrivial(self):
		return self.value is not None

	##
	# Attach a constant to a subgraph.
	##
	def reduce(self, value):
		self.value = value

	##
	# Remove a node.
	#
	# This only removes the node from the
	# node list. It does not clean up any 
	# edges possibly leading to the node.
	#
	# It silently fails if the node does not 
	# exist.
	##
	def removeNode(self, node):
		try:
			self.nodes.remove(node)	
		except ValueError: pass

	##
	# Replace a node.
	#
	# This replaces a node in the node list
	# of the subgraph by new. All of the in and
	# output ports of the node are added to new.
	##
	def replaceNode(self, node, new):
		idx = self.nodes.index(node)
		self.nodes[idx] = new

		new.inputs  = node.inputs
		new.outputs = node.outputs
		new.inputPorts = node.inputPorts
		new.outputPorts = node.outputPorts

		for port in new.inputPorts:
			port.node = new
		for port in new.outputPorts:
			port.node = new