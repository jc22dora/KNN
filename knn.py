import statistics
import math
import operator
import random
class knn:
    def __init__(self,k, trainingData, testData):
        self.k = k
        self.trainingData = self.transformData(trainingData)
        #self.testData = self.transformData(testData)
        self.testData = []
        self.generateTestData()
        self.classifications = []
        self.classificationData = []
        self.classifyTestData()


    def transformData(self, data):
        trainingData = [] #list of point obj's
        for i in data: #iterating through labels of dict
            label = i["label"]
            data = i["data"]
            for xy in data: #iterating through points in label data
                pt = point(label, xy[0], xy[1])
                trainingData.append(pt)
        return trainingData

    def euclideanVector(self, pt):
        distances = [] # list of lists
        for xy in self.trainingData:
            distances.append([self.euclideanDistance(xy.x, xy.y, pt.x, pt.y),xy.classLabel])
        return distances

    def euclideanDistance(self, x1, y1, x2, y2):
        return math.sqrt((x2-x1)**2+(y2-y1)**2)

    def classifyTestData(self):
        testData = self.testData
        data = []
        for pt in testData:
            data = self.euclideanVector(pt)
            self.getClassification(data)
        self.transformClassifications()
    def getClassification(self, data):
        ##
        #sort
        data = sorted(data, key=operator.itemgetter(0))
        ##
        distances, labels = [], []
        distances = [x[0] for x in data]
        labels = [x[1] for x in data]
        distances = distances[0:self.k]
        labels = labels[0:self.k]
        try:
            self.classifications.append(statistics.mode(labels))
        except:
            self.classifications.append(labels[0])
        
    def transformClassifications(self):
        testxy = [(test.x, test.y) for test in self.testData]
        classLabels = [label for label in self.classifications]
        for i in range(len(testxy)):
            pt = point(classLabels[i], testxy[i][0], testxy[i][1])
            self.classificationData.append(pt)
    def score(self):
        correct, total = 0, 0
        for test in self.classificationData:
            if test.x >=0: # q1, q4
                if test.y >= 0: #q1
                    if test.classLabel == "q1":
                        correct += 1
                else: #q2
                    if test.classLabel == "q4":
                        correct += 1

            else:
                if test.y >= 0: #q3
                    if test.classLabel == "q2":
                        correct += 1
                else: #q4
                    if test.classLabel == "q3":
                        correct += 1
            total += 1
        print("score: ",correct/total)
        return correct/total

    def generateTestData(self):
        n = len(self.trainingData)
        data = []
        for i in range(round(2*n)):
            eps = round(random.randrange(1,26)/random.randrange(27,76),2)


            q1x, q1y = random.randrange(0,5)+eps, random.randrange(0,5)+eps #q1
            q2x, q2y = -1*random.randrange(0,5)+eps, random.randrange(0,5)+eps #q2
            q3x, q3y = -1*random.randrange(0,5)+eps, -1*random.randrange(0,5)+eps #q3
            q4x, q4y = random.randrange(0,5)+eps, -1*random.randrange(0,5)+eps #q4
            
            q1 = point("", q1x, q1y)
            q2 = point("", q2x, q2y)
            q3 = point("", q3x, q3y)
            q4 = point("", q4x, q4y)

            data.append(q1)
            data.append(q2)
            data.append(q3)
            data.append(q4)
        self.testData = data
        


        
class point:
    def __init__(self, label, x, y):
        self.classLabel = label
        self.x = x
        self.y = y

if __name__ == "__main__":
    q1 = {"label": "q1", "data":[(2,2), (3,2), (4,2), (2,4), (3,4)]}
    q2 = {"label": "q2", "data":[(-3,1), (-4,2), (-4,3), (-3,4), (-4,4)]}
    q3 = {"label": "q3", "data":[(-3,-1), (-2,-2), (-3,-4), (-4,-4), (-3,-3)]}
    q4 = {"label": "q4", "data":[(1, -1), (1,-2), (3,-2), (3,-4), (3,-5)]}
    data = []
    data.append(q1)
    data.append(q2)
    data.append(q3)
    data.append(q4)
    testData = [{"label":"", "data":[(1.5,1.5),(-1.5,-1.5),(-1.5,1.5),(1.5,-1.5)]}]
    epochs = 15
    score = 0
    for epoch in range(epochs):
        ktest = knn(15, data, testData)
        print("epoch :", epoch)
        score += ktest.score()
        ktest.generateTestData()

    print("final score: ", score/epochs)