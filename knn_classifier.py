import random
import math
import time
from multiprocessing.dummy import Pool as ThreadPool


def minkowski(arr1,arr2,p=2):
	if len(arr1) != len(arr2):
		return None
	distance = 0
	for i,j in zip(arr1,arr2):
		distance += math.pow(abs(float(i)-float(j)),p)
	return math.pow(distance,(float(1)/float(p)))

def generate_series(size,percentage):
	train_size = int(size * percentage / 100)
	train_index = []
	for i in range(train_size):
		index = random.randint(0,size)
		while index in train_index:
			index = random.randint(0,size)
		train_index.append(index)
	train_index.sort()
	return train_index

def train_test_split(data,label,percentage=66):
	size = len(data)
	train_index = generate_series(size,percentage)
	train_data = []
	test_data = []
	train_label = []
	test_label = []

	for i in range(size):
		if i in train_index:
			train_data.append(data[i])
			train_label.append(label[i])
		else:
			test_data.append(data[i])
			test_label.append(label[i])

	return train_data,train_label,test_data,test_label

def get_max_vote(d):
	v = list(d.values())
	k = list(d.keys())
	vote = k[v.index(max(v))]
	return vote

def get_voted_label(arr,neighbors):
	labels = {}
	for i in range(neighbors):
		try:
			labels[arr[i][1]]+=1
		except:
			labels[arr[i][1]]=1
	return get_max_vote(labels)

def read_data(filename,delimitter=","):
	data = []
	labels = []
	
	with open(filename) as f: lines = [line.rstrip('\n') for line in f]
	for line in lines:
		tokens = line.split(delimitter)
		labels.append(tokens[len(tokens)-1])
		data.append(tokens[0:len(tokens)-1])
	f.close()

	return data,labels


class knn:


	def __init__(self,threads=8,neighbors=5):
		self.threads = threads
		self.neighbors = neighbors
		self.ratio = 0


	def fit(self,train_data,train_label):
		self.train_data = train_data
		self.train_label = train_label


	def predict(self,test_sample):
		distances = []
		for train_d,train_l in zip(self.train_data,self.train_label):
			distances.append((minkowski(train_d,test_sample),train_l))
		distances.sort()
		voted_label = get_voted_label(distances,self.neighbors)
		return voted_label


	def test_one(self,test_sample,test_label):
		if self.predict(test_sample) == test_label:
			self.ratio += 1
			return True
		else:
			return False


	def test_some(self,test_data,test_label,test_size):
		ratio = 0
		for i in range(test_size):
			if self.test_one(test_data[i],test_label[i]):
				ratio += 1
		return float(ratio) / float(test_size)


	def test_all(self,test_data,test_label):
		size = len(test_data)
		return self.test_some(test_data,test_label,size)

data,label = read_data("preoprocessed_kdd_data")
print("File read successfully")
train_x, train_y, test_x, test_y = train_test_split(data,label)
print("Train and test sets created")
knn = knn()
knn.fit(train_x,train_y)
print("Model trained")
start = time.time()
print(knn.test_some(test_x,test_y,500))
print("Model tested in " + str(time.time() - start))
print(knn.ratio)