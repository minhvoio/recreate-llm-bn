from __future__ import print_function
from bni_netica import *
from bni_netica import Net
import time

netDir = "../nets/collection/"

def mainTests():
	print("[Open NF_V1.dne]")
	myNet = Net(netDir+"NF_V1.dne")
	print()

	print("[Set to None (garbage collect)]")
	# This will trigger the deletion
	myNet = None
	print()

	print("[Re-open NF_V1.dne]")
	myNet = Net(netDir+"NF_V1.dne")
	print()

	print("Net name:", myNet.name())
	print("[Change name to NFAV1]")
	myNet.name("NFAV1")
	print("Check new net name:", myNet.name())
	print()

	print("Net title:", myNet.title())
	print("[Change title to 'Native Fish V1']")
	myNet.title("Native Fish A V1")
	print("Check new net title:", myNet.title())
	print()

	print("[Get RiverFlow node]")
	rf = myNet.node("RiverFlow")
	print(rf)

	print("RiverFlow number states:", rf.numberStates())
	print("RiverFlow node beliefs:", rf.beliefs())
	print("FishAbundance node beliefs:", myNet.node("FishAbundance").beliefs())
	print("P(All Evidence):", myNet.findingsProbability())
	print()

	print("[Set RiverFlow = state0]")
	rf.finding(0)
	print("RiverFlow node beliefs|RiverFlow=state0:", rf.beliefs())
	print("FishAbundance node beliefs|RiverFlow=state0:", myNet.node("FishAbundance").beliefs())
	print("New P(Evidence):", myNet.findingsProbability())
	print()

	print("[Clear findings]")
	myNet.node("RiverFlow").retractFindings()
	print("New P(Evidence):", myNet.findingsProbability())
	print()

	print("[Set RiverFlow = state0]")
	rf.finding(0)
	print("RiverFlow node beliefs|RiverFlow=state0:", rf.beliefs())
	print("[Clear all findings]")
	myNet.node("RiverFlow").retractFindings()
	print("RiverFlow node beliefs:", rf.beliefs())
	print()

	print("RiverFlow Virtual Evidence (Likelihoods):", rf.likelihoods())
	print("P(RiverFlow):", rf.beliefs())
	print()

	print("[Set RiverFlow Likelihoods = 0.3,0.2]")
	rf.likelihoods([0.3,0.2])
	print("New P(RiverFlow):", rf.beliefs())
	print("New Virtual Evidence:", rf.likelihoods())
	print()

	print("[Set RiverFlow Likelihoods = 0.4,0.2]")
	rf.likelihoods([0.4,0.2])
	print("New P(RiverFlow):", rf.beliefs())
	print("New Virtual Evidence:", rf.likelihoods())
	print()

	print("[Create node called TestA]")
	node = Node(myNet, "TestA")
	print()

	print("TestA states:", node.stateNames())
	print()

	print("[Add state called 'three']")
	node.addState('three')
	print("TestA states:", node.stateNames())
	print()

	print("[Rename state0 to 'one']")
	node.renameState(0, 'one')
	print("TestA states:", node.stateNames())
	print()

	print("[Rename all states to one,two,three]")
	node.renameStates(['one','two','three'])
	print("TestA states:", node.stateNames())
	print()
	
	print("[Reorder the states to three,one,two]")
	node.reorderStates(['three',0,1])
	print("New TestA states order:", node.stateNames())
	print()

	print("[Create node TestB with one state called 'a'")
	print(" (fails in GeNIe because doesn't allow it")
	print(" --- i.e. creates node with 2 states, wrongly named)]")
	node = Node(myNet, "TestB", ['a'])
	print("TestB states:", node.stateNames())
	print()

	print("[Create node TestC with 3 states, called a,b,c]")
	node = Node(myNet, "TestC", ['a','b','c'])
	print("TestC states:", node.stateNames())
	print()

	print("TestC CPT:", node.cpt1d())
	print()
	
	print("[Create continuous node TestD]")
	testD = myNet.addNode("TestD", [])
	print("Node type?", Node.typeName[testD.type()])
	print()
	
	newLevels = [0.2,0.6,1.8,3.4,9.7]
	print("[Set levels to {}]".format(newLevels))
	testD.levels(newLevels)
	print("Get TestD levels:", testD.levels())
	print()

	newLevels = [3,7,10]
	print("[Create continuous node TestE with levels {}]".format(newLevels))
	testE = myNet.addNode("TestE", newLevels)
	print("Node type?", Node.typeName[testE.type()])
	print("Levels", testE.levels())
	print()

	print("RiverFlow CPT:", rf.cpt1d())
	print()

	print("[Set TestC CPT with 0.3,0.3,0.3. Should give 1/3,1/3,1/3]")
	node.cpt1d([0.3,0.3,0.3])
	print("New TestC CPT:", node.cpt1d())
	print()

	print("[Add RiverFlow as parent to TestC]")
	node.addParents(["RiverFlow"])
	print("[Add FishAbundance as child of TestC]")
	node.addChildren(["FishAbundance"])
	print()

	print("1D CPT:", node.cpt1d())
	node.cpt1d([0.1,0.3,0.7,0.2,0.1,0.1])
	print("[Set TestC CPT to [0.1,0.3,0.7,0.2,0.1,0.1] using 1D array]")
	print("New 1D CPT:", node.cpt1d())
	print()

	print("2D CPT:", node.cpt())
	node.cpt([[0.1,0.3,0.2],[0.2,0.4,0.4]])
	print("[Set TestC CPT to [[0.1,0.3,0.2],[0.2,0.4,0.4]] using 2D array]")
	print("New 2D CPT:", node.cpt())
	print("New 1D CPT:", node.cpt1d())
	print()

	print("[Run through all nodes, and print names and titles]")
	for node in myNet.nodes():
		print(node.name(), node.title())
	print()

	print("[Run through all parents of FishAbundance, print names and titles]")
	for node in myNet.node("FishAbundance").parents():
		print(node.name(), node.title())
	print()

	print("RiverFlow's visual position:", rf.position())
	print("[Set RiverFlow's visual position to 120,400]")
	print("RiverFlow's visual position:", rf.position(120,400).position())
	print()

	fap = myNet.node("FishAbundance").parents()
	print("Combinations of parent states for FishAbundance: ", myNet.numberCombinations(fap))

	print("Parent state combinations for FishAbundance:")
	parentIndexes = [0]*len(fap)
	while 1:
		print([fap[i].state(pi).name() for i,pi in enumerate(parentIndexes)])
		if not myNet.nextCombination(parentIndexes, fap): break

	print("[Write net to file called output_NF_V1_test.dne]")
	myNet.write("output_NF_V1_test.dne")
	print()

	print("[Learning network]")
	myNet.experience(1000000)
	myNet.learn("../nets/NF_V1.csv", type = 'EM')
	myNet.write("../nets/output_NF_V1_test_learn.dne")
	
	#myNet.addNode('MyDecision', states = ['Choice1','Choice2'])
	print('Utilities:', myNet.node('D').expectedUtils())


# mainTests()

berkeleyAdmissionNet = Net(netDir+"Berkeley Admissions.neta")
CancerNeapolitanNet = Net(netDir+"Cancer Neapolitan.neta")
ChestClinicNet = Net(netDir+"ChestClinic.neta")
ClassifierNet = Net(netDir+"Classifier.neta")
CoronaryRiskNet = Net(netDir+"Coronary Risk.neta")
FireNet = Net(netDir+"Fire.neta")
MendelGeneticsNet = Net(netDir+"Mendel Genetics.neta")
RatsNet = Net(netDir+"Rats.neta")
WetGrassNet = Net(netDir+"Wet Grass.neta")
RatsNoisyOr = Net(netDir+"Rats_NoisyOr.dne")


print("Berkeley Admissions Net name:", berkeleyAdmissionNet.name())
print("Cancer Neapolitan Net name:", CancerNeapolitanNet.name())
print("Chest Clinic Net name:", ChestClinicNet.name())
print("Classifier Net name:", ClassifierNet.name())
print("Coronary Risk Net name:", CoronaryRiskNet.name())
print("Fire Net name:", FireNet.name())
print("Mendel Genetics Net name:", MendelGeneticsNet.name())
print("Rats Net name:", RatsNet.name())
print("Rat Noisy Or Net name:", RatsNoisyOr.name())
print("Wet Grass Net name:", WetGrassNet.name())

print()
for node in RatsNoisyOr.nodes():
	print(f"{node.name()} -> {[child.name() for child in node.children()]}")


import random

def add_noise_to_node_cpt(node, std=0.05, clip_min=0.05, clip_max=0.95):
	cpt = node.cpt()
	new_cpt = []

	for row in cpt:
		noisy_row = []
		for p in row:
			noise = random.gauss(0, std)
			noisy_p = p + noise
			if noisy_p < clip_min:
				noisy_p = clip_min
			elif noisy_p > clip_max:
				noisy_p = clip_max
			noisy_row.append(noisy_p)

		# Normalize the row to sum to 1
		row_sum = sum(noisy_row)
		normalized_row = [p / row_sum for p in noisy_row]
		new_cpt.append(normalized_row)

	node.cpt(new_cpt)
	return node

def add_noise_to_net(net, std=0.1, clip_min=0.05, clip_max=0.95):
	for node in net.nodes():
		try:
			if node.kind() == 0 and node.cpt() is not None: # kind 0 is discrete
				add_noise_to_node_cpt(node, std, clip_min, clip_max)
		except Exception as e:
			print(f"Error processing node {node.name()}: {e}")

	return net

import itertools
def print_node_cpt(node):
    print(f"\nCPT for node: {node.name()}")
    parent_names = [p.name() for p in node.parents()]
    print(f"Parents: {parent_names}")

    for i, row in enumerate(node.cpt()):
        parent_combo = next(itertools.islice(node.net.CombinationIterator(node.parents(), returnType="names"), i, None))
        row_str = ", ".join(f"{state}" for state in parent_combo)
        print(f"Given [{row_str}]: {['{:.3f}'.format(p) for p in row]}")

noisy_node = RatsNoisyOr.node("Social_Activity")
print_node_cpt(noisy_node)

# original_cpt = noisy_node.cpt()
# add_noise_to_node_cpt(noisy_node, std=0.03)
# print_node_cpt(noisy_node)

newNet = add_noise_to_net(RatsNoisyOr, std=0.03, clip_min=0.05, clip_max=0.95)
newNet.write("RatsNoisyOr_noisy2.dne")

