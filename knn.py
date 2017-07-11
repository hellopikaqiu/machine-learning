import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_features(data):
	features = []
	for key in data.keys():
		features.append(key)
	features.remove("label")
	return features

def feature_selection(data):	
	from sklearn.feature_selection import SelectKBest
	from sklearn.feature_selection import chi2
	from sklearn.feature_selection import f_classif

	features = get_features(data)
	X = data[features]
	y = data["label"]

	selector = SelectKBest(score_func=chi2,k=5)
	selector.fit(X,y)
	indexes_selected = selector.get_support(indices=True)
	
	selected_features = []
	for i in indexes_selected:
		selected_features.append(features[i])

	print "[+] Selected features -> " + bcolors.OKBLUE + str(selected_features) + bcolors.ENDC
	return data[selected_features]


def with_feature_selection(data):
	print bcolors.HEADER + bcolors.UNDERLINE + "Testing with selected features" + bcolors.ENDC
	
	features = get_features(data)
	X = feature_selection(data)
	y = data["label"]
	
	X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=0)
	
	knn = KNeighborsClassifier(n_neighbors = 5)
	
	start = time.time()
	knn.fit(X_train,y_train)

	print "[+] Classifier trained in " + bcolors.OKGREEN +  str(time.time() - start)   + bcolors.ENDC
	
	start = time.time()
	score = knn.score(X_test,y_test)
	
	print "[+] Model Evaluated in " + bcolors.OKGREEN + str(time.time()-start)   + bcolors.ENDC
	print "[!] Test score is " + bcolors.OKBLUE + str(score)   + bcolors.ENDC
	print bcolors.BOLD + bcolors.WARNING + "-------------------------------------------------" + bcolors.ENDC

def with_full_features(data):
	print bcolors.HEADER + bcolors.UNDERLINE + "Testing with full data" + bcolors.ENDC
	
	features = get_features(data)
	X = data[features]
	y = data["label"]
	
	X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=0)
	
	knn = KNeighborsClassifier(n_neighbors = 5)
	
	start = time.time()
	knn.fit(X_train,y_train)

	print "[+] Classifier trained in " + bcolors.OKGREEN + str(time.time() - start)   + bcolors.ENDC
	
	start = time.time()
	score = knn.score(X_test,y_test)
	
	print "[+] Model Evaluated in " + bcolors.OKGREEN + str(time.time()-start)   + bcolors.ENDC
	print "[!] Test score is " + bcolors.OKBLUE + str(score)   + bcolors.ENDC
	print bcolors.BOLD + bcolors.WARNING + "-------------------------------------------------" + bcolors.ENDC

def test_with_real(data,test_filename):
	
	#X = feature_selection(data)
	X = data[get_features(data)]
	y = data["label"]
	knn = KNeighborsClassifier(n_neighbors = 5)
	knn.fit(X,y)

	test_file = open(test_filename,"r")
	lines = []
	for line in test_file:
		line = line.replace("\n","")
		tokens = line.split(",")
		lines.append(tokens)
	test_file.close()

	print len(lines)
	test_results = []
	for i in range(len(lines)):
		print i
		print lines[i]
		test_results.append(knn.predict(lines[i]))

	count_dict = {}
	for i in test_results:
		try:
			count_dict[i]+=1
		except:
			count_dict[i]=1
	
	print count_dict

def main():
	filename="preprocessed_kddcup_data"
	path="/home/frkn/Desktop/applied_ml/kddcup/new/"
	data = pd.read_csv(path+filename)

	#with_full_features(data)
	#with_feature_selection(data)
	test_with_real(data,"preprocessed_attack")


main()