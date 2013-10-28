# CompoundNode.py
# Mathijs Saey
# dvm prototype

import edge
import port
import runtime

from abstractnode import AbstractNode

class CompoundNode(AbstractNode):
	"""A Compound node represents a more complex node that contains subgraphs"""

	def __init__(self, inputs, outputs):
		super(CompoundNode, self).__init__(inputs, outputs)
		self.fillList(self.outputs, port.StopPort)
		self.fillList(self.inputs, port.OutputPort)
		self.controller = port.StopPort(self, -1)
		self.subgraphs = []

	def getInput(self, idx):
		return self.getFromList(self.inputs, port.OutputPort, idx)
	def getOutput(self, idx):
		return self.getFromList(self.outputs, port.StopPort, idx)

	def attach(self, subGraph):
		print subGraph
		for idx in xrange(0, len(subGraph.outputs)):
			src = subGraph.getOutput(idx)
			print "8==D",src
			dst = self.getOutput(idx)
			edge.Edge(src, dst)
		for idx in xrange(0, len(subGraph.inputs)):
			src = self.getInput(idx)
			dst = subGraph.getInput(idx)
			edge.Edge(src, dst)
		print "=====>", self.outputs#[0].edges[0].destination


	def addSubGraphs(self, lst):
		self.subgraphs = lst

	def receivedInput(self, idx):
		raise NotImplementedError("ReceivedInput is an abstract method!")

class SelectNode(CompoundNode):
	def __init__(self):
		super(SelectNode, self).__init__(0, 0)

	def __str__(self):
		id = super(SelectNode, self).__str__()
		return "Select node: (" + id + ")"

	def addSubGraphs(self, lst):
		super(SelectNode, self).addSubGraphs(lst)
		pred = self.subgraphs[0]
		edge.Edge(self.getInput(0), pred.getInput(0))
		edge.Edge(pred.getOutput(0), self.controller)

	def receivedInput(self, idx):
		if idx is -1:
			val = self.controller.value()
			graph = self.subgraphs[val + 1]

			self.outputs[0].clear()
			self.outputs[0].activate()
			self.attach(graph)
