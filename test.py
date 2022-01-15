import numpy as np

class Bandit:
	def __init__(self, node_id, arm_data, armNum):
		self.id=node_id
		self.data=arm_data
		self.count=np.ones(armNum)
		self.it=0
	def decide(self,k=1):
		max_prob=-1.0
		for arm_id,prob in self.data.items():
			rho=np.sqrt(np.log(self.it+1)/self.count[arm_id-1])
			if prob+k*rho>max_prob:
				picked_arm=arm_id
				max_prob=prob+k*rho
		return picked_arm

	def update(self,picked_arm,isRight):
		new_prob=(self.data[picked_arm]*self.it+isRight)/(self.it+1)
		# print(self.id,new_prob)
		self.data[picked_arm]=new_prob
		self.it+=1

def graph_sort(origin_list):
	new_list=[]
	end_id=sort_helper(origin_list,new_list,1)
	# print("ending",end_id)
	return new_list,end_id

def sort_helper(origin_list,new_list,now_id):
	next_id=origin_list[now_id-1]
	new_list.append(now_id)
	# print("next",next_id)
	if next_id in new_list:
		return now_id
	else:
		return sort_helper(origin_list,new_list,next_id)

filename = 'tsp20/heatmaptsp20_0.txt'
arr = []
with open(filename, 'r') as file_to_read:
	number = int(file_to_read.readline())
	while True:
		lines = file_to_read.readline()
		if not lines or lines[0] == 't':
			break
		l_tmp = lines.split()
		arr.append(list(map(float, l_tmp)))

bandit_list = []
for i in range(number):
	temp_l = {}
	for j in range(number):
		if arr[i][j] != 0.0:
			temp_l[j+1]=arr[i][j]
	temp_b=Bandit(i+1,temp_l,j+1)
	bandit_list.append(temp_b)
# print(bandit_list[0].id,bandit_list[0].data)
# print(x_list)

ans=[1, 8, 19, 7, 11, 4, 13, 20, 10, 5, 15, 9, 18, 3, 6, 12, 14, 2, 16, 17, 1]
for t in range(1500):
	picked_list=[]
	for i in range(number):
		temp_picked=bandit_list[i].decide()
		picked_list.append(temp_picked)
		# bandit_list[i].update(temp_picked,(temp_picked==ans[i+1]))
	sorted_list,end_id=graph_sort(picked_list)
	if end_id!=1: #wrong case
		# print("end:",end_id)
		bandit_list[end_id-1].update(picked_list[end_id-1],False)
		for i in range(number):
			if i!=end_id-1:
				bandit_list[i].update(picked_list[i],True)
	else: #right case
		for i in range(number):
			bandit_list[i].update(picked_list[i],True)
	# print(picked_list)
	print("iter:",t,"route:",sorted_list)
	# print(bandit_list[7].data)


