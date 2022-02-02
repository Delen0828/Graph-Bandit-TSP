from posixpath import split
import numpy as np
import os
from tqdm import tqdm

class Bandit:
    def __init__(self, node_id, arm_data, armNum):
        self.id = node_id
        self.data = arm_data
        self.count = np.ones(armNum)
        self.it = 0

    def decide(self, k=1):
        max_prob = -1.0
        for arm_id, prob in self.data.items():
            rho = np.sqrt(np.log(self.it+1)/self.count[arm_id-1])
            if prob+k*rho > max_prob:
                picked_arm = arm_id
                max_prob = prob+k*rho
        return picked_arm

    def update(self, picked_arm, isRight):
        new_prob = (self.data[picked_arm]*self.it+isRight)/(self.it+1)
        # print(self.id,new_prob)
        self.data[picked_arm] = new_prob
        self.it += 1

    def reset(self):
        self.it = 0


def graph_sort(origin_list):
    new_list = []
    end_id = sort_helper(origin_list, new_list, 1)
    # print("ending",end_id)
    return new_list, end_id


def sort_helper(origin_list, new_list, now_id):
    next_id = origin_list[now_id-1]
    new_list.append(now_id)
    # print("next",next_id)
    if next_id in new_list:
        return now_id
    else:
        return sort_helper(origin_list, new_list, next_id)
ans_path = 'tsp20_test_concorde.txt'
with open(ans_path, 'r') as ans_file:
	for parent,dirnames,filenames in os.walk('tsp20'):
		for filename in tqdm(filenames):
	# filename = 'tsp20/heatmaptsp20_0.txt'
			filepath=os.path.join(parent,filename)
			arr = []
			with open(filepath, 'r') as file_to_read:
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
						temp_l[j+1] = arr[i][j]
				temp_b = Bandit(i+1, temp_l, j+1)
				bandit_list.append(temp_b)
			# print(bandit_list[0].id,bandit_list[0].data)
			# print(x_list)

			ansline = ans_file.readline()
			ans = ansline.split('output')[1].strip()
			ans = list(map(int, ans.split(' ')))
			ans.pop()
			# print(ans)
			for t in range(100):
				picked_list = []
				for i in range(number):
					temp_picked = bandit_list[i].decide()
					picked_list.append(temp_picked)

				sorted_list, end_id = graph_sort(picked_list)
				# print("iter:", t, "route:", sorted_list)

				if end_id != int(ans[-1]):  # wrong case
					# print("end:",end_id,ans[-1])
					bandit_list[end_id-1].reset()
					bandit_list[end_id-1].update(picked_list[end_id-1], False)
					for i in range(number):
						if i != end_id-1:
							bandit_list[i].update(picked_list[i], True)
				else:  # right case
					for i in range(number):
						bandit_list[i].update(picked_list[i], True)
					# print(sorted_list, ans)
					if sorted_list == ans:
						break