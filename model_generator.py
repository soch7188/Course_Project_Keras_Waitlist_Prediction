import pymongo
import collections
import datetime
import pickle
import numpy as np
from keras.models import Sequential, model_from_json
from keras.preprocessing import sequence
from keras.layers import Dense, Embedding, LSTM, Dropout

host = "127.0.0.1"
database_name = "hkust"

# Connect to MongoDB
client = pymongo.MongoClient(host)
db = client[database_name]

print("Database Connected")

def arr(_in): return [x for x in _in]

def mergeDict(x,y): return {**x, **y}

def getData(_courseCode, _sectionId):
    res = dict()
    course = arr(db.courses.find({"code":_courseCode}))
    for sec in course[0]["sections"]:
        if (sec["sectionId"] == _sectionId):
            res[sec["recordTime"]] = {"quota":sec["quota"],"enrol":sec["enrol"],"wait":sec["wait"]}
    res = collections.OrderedDict(sorted(res.items()))
    return res




##### MAIN #####
def run(_courseCode, _lectureNumber):
    COURSE_CODE = _courseCode
    LECTURE_NUMBER = _lectureNumber
    

    # Main execution
    dataDict = getData(COURSE_CODE, LECTURE_NUMBER)

    # print("Organizing all data for the corrsponding target")
    dataList = []
    for k, v in dataDict.items(): 
        # print(k, v)
        dataList.append([k,v])

    # Datetime Objects
    MINUTES_30 = datetime.timedelta(minutes=30)
    LAST_DATETIME = dataList[-1][0]

    # Preprocessing
    fullHeadDataList = []
    fullDataList = []

    # Iterate through the available data
    for k, v in dataDict.items(): 
        
        ##### Add to data lists #####
        fullDataList.append(mergeDict({"datetime":k}, v))
        fullHeadDataList.append(mergeDict({"datetime":k}, v))
        
        # Get the time of the next data
        k_next = k + MINUTES_30
        
        # If the the next data is unavailable, iterate until the next available data is found
        # Ends when reaching the end of the entire dataset
        while((k_next) not in dataDict) and (k_next <= LAST_DATETIME):
    
            ##### Add to data lists #####
            fullDataList.append({"datetime":k_next})
            fullHeadDataList.append(mergeDict({"datetime":k_next}, v))
            
            # Get the time of the next data
            k_next = k_next + MINUTES_30
    

    # Preprocess step 2
    fullHeadTailDataList = []
    first_nonavail = True
    for ind,row in enumerate(fullDataList):
        if 'enrol' in row:
            fullHeadTailDataList.append(row)
            first_nonavail = True
        else:
            # Keep the pre avail row the same
            if (first_nonavail):
                preAvailRow = fullHeadTailDataList[-1]
            first_nonavail = False
                
            tmp_ind = ind
            
            # Keep rolling to the next available row and jump out
            while('enrol' not in fullDataList[tmp_ind+1]): tmp_ind = tmp_ind + 1
                
            # Get the next available row
            nextAvailRow = fullDataList[tmp_ind+1]
            
            newRow = {"datetime":row["datetime"], 
                    "quota": (preAvailRow["quota"]+nextAvailRow["quota"])/2,
                    "enrol": (preAvailRow["enrol"]+nextAvailRow["enrol"])/2,
                    "wait": (preAvailRow["wait"]+nextAvailRow["wait"])/2}
            
            fullHeadTailDataList.append(newRow)
    
    # # Save to file
    # with open('data.pickle', 'wb') as handle:
    #     pickle.dump(fullHeadTailDataList, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    

    # # Load file
    # print("Loading the data.pickle as dataset")
    # with open('data.pickle', 'rb') as handle:
    #     fullHeadTailDataList = pickle.load(handle)


    # Prepare data
    fullHeadTailDataListEQW = []
    for item in fullHeadTailDataList:
        fullHeadTailDataListEQW.append([item['enrol'],item['quota'],item['wait']])

    fullHeadTailDataListWAIT = []
    for item in fullHeadTailDataList:
        fullHeadTailDataListWAIT.append(item['wait'])


    def create_dataset(dataset, look_back=1): 
        X, Y = [], []
        for i in range(len(dataset)-look_back):
            a = dataset[i:i+look_back]
            X.append(a)
            Y.append(dataset[i + look_back]) 
        return np.array(X), np.array(Y)
    
    def saveModel(model, modelFilenamePrefix):
        structureFilename = modelFilenamePrefix + ".json" 
        model_json = model.to_json()
        with open(structureFilename, "w") as f:
            f.write(model_json)
            
        weightFilename = modelFilenamePrefix + ".h5" 
        model.save_weights(weightFilename)
        # print("Saved model:", modelFilenamePrefix)


    # Apply lookback
    # print("Apply lookback on the dataset")
    _,dataY = create_dataset(fullHeadTailDataListWAIT, 2)
    dataX,_ = create_dataset(fullHeadTailDataListEQW, 2)

    # print(dataX.shape)
    # print(dataY.shape)


    ##### MODELS #####
    # Sequential.weights.

    # Model 1
    def train1(X,Y,_dim):
        X = np.asarray(X)
        Y = np.asarray(Y)
        
        # print(X[0])

        model = Sequential()
        model.weights.clear()
        model.add(Dense(8, input_dim=_dim, activation='relu'))
        model.add(Dense(4, activation='relu'))
        model.add(Dense(1, activation='relu'))

        model.compile(loss="mean_squared_error", optimizer="adam", metrics=["mae"])
        model.fit(X, Y, epochs=50, batch_size=4, validation_split=0.2)

        scores = model.evaluate(X, Y)
        # print("{}: {}".format(model.metrics_names[1], scores[1]*100))

        return model

    # Model 2
    def train2(X,Y,_dim):
        X = np.asarray(X)
        Y = np.asarray(Y)
        
        # print(X[0])

        model = Sequential()
        model.weights.clear()
        model.add(Dense(16, input_dim=_dim, activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(1, activation='relu'))

        model.compile(loss="mean_squared_error", optimizer="adam", metrics=["mae"])
        model.fit(X, Y, epochs=30, batch_size=4, validation_split=0.2)

        scores = model.evaluate(X, Y)
        # print("{}: {}".format(model.metrics_names[1], scores[1]*100))

        return model

    # Model 3
    def train3(X,Y,_dim):
        X = np.asarray(X)
        Y = np.asarray(Y)
        
        # print(X[0])

        model = Sequential()
        model.weights.clear()
        model.add(Dense(16, input_dim=_dim, activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(1, activation='relu'))

        model.compile(loss="mean_squared_error", optimizer="adam", metrics=["mae"])
        model.fit(X, Y, epochs=30, batch_size=4, validation_split=0.2)

        scores = model.evaluate(X, Y)
        # print("{}: {}".format(model.metrics_names[1], scores[1]*100))

        return model

    # Model 4
    def train4(X,Y, timestep=1, dim=1):
        # Reshape to fit the LSTM model
        X = np.swapaxes(X,1,2)
            
        # Model
        model = Sequential()
        model.weights.clear()
        model.add(LSTM(4, input_shape=(timestep,dim)))
        model.add(Dropout(0.2))
        model.add(Dense(1, activation='relu'))
        model.compile(loss="mean_squared_error", optimizer="adam", metrics=["mae"])
        model.fit(X, Y, epochs=30, batch_size=4, validation_split=0.2)

        # Model
        # model = Sequential()
        # model.add(LSTM(3, return_sequences=True, input_shape=(timestep, dim)))
        # model.add(LSTM(2))
        # model.add(Dense(1, activation='relu'))
        # model.compile(loss="mean_squared_error", optimizer="adam", metrics=["mae"])
        # model.fit(X, Y, epochs=30, batch_size=4, validation_split=0.2)

        # Ealuation
        scores = model.evaluate(X, Y)
        # print("{}: {}".format(model.metrics_names[1], scores[1]*100))
        
        return model

    # Model 4
    def train5(X,Y, timestep=1, dim=1):
        # Reshape to fit the LSTM model
        X = np.swapaxes(X,1,2)
            
        # Model
        model = Sequential()
        model.weights.clear()
        model.add(LSTM(8, input_shape=(timestep,dim)))
        model.add(Dense(1, activation='relu'))
        model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["mae"])
        model.fit(X, Y, epochs=30, batch_size=4, validation_split=0.2)

        # Ealuation
        scores = model.evaluate(X, Y)
        # print("{}: {}".format(model.metrics_names[1], scores[1]*100))
        
        return model

    dataX_NN = dataX.reshape(len(dataX), 6)
    dataY_NN = dataY.reshape(len(dataY), 1)

    # Training
    print("Model 1 Training Start")
    model1 = train1(dataX_NN, dataY_NN, 6)
    saveModel(model1, "models/"+COURSE_CODE+"-"+LECTURE_NUMBER+"-"+"model1")

    print("Model 2 Training Start")
    model2 = train2(dataX_NN, dataY_NN, 6)
    saveModel(model2, "models/"+COURSE_CODE+"-"+LECTURE_NUMBER+"-"+"model2")

    print("Model 3 Training Start")
    model3 = train3(dataX_NN, dataY_NN, 6)
    saveModel(model3, "models/"+COURSE_CODE+"-"+LECTURE_NUMBER+"-"+"model3")

    print("Model 4 Training Start")
    model4 = train4(dataX,dataY,3,2)
    saveModel(model4, "models/"+COURSE_CODE+"-"+LECTURE_NUMBER+"-"+"model4")

    print("Model 5 Training Start")
    model5 = train5(dataX,dataY,3,2)
    saveModel(model5, "models/"+COURSE_CODE+"-"+LECTURE_NUMBER+"-"+"model5")


    # Main execution
    print(COURSE_CODE, LECTURE_NUMBER, "Completed")


    return


# Load course list


with open('courseList.pickle', 'rb') as handle:
    courseList = pickle.load(handle)


print(courseList)

for course in courseList:
    run(course["code"],course["sectionId"])

# run("COMP4632","L1")