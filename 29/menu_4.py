def run():
    # Welcome message
    print("4. Waiting List Size Prediction !\n")

    COURSE_CODE = input("Input Course Code >>  ") # course code
    LECTURE_NUMBER = input("Input Lecture Number >>  ") # course code
    TIME_SLOT = input("Input Time Slot >>  ") # course code




    # Setup
    print("Start Data Preparation")
    import pymongo
    import collections
    import datetime
    import pickle

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

    # Main execution
    dataDict = getData(COURSE_CODE, LECTURE_NUMBER)

    print("Organizing all data for the corrsponding target")
    dataList = []
    for k, v in dataDict.items(): 
        print(k, v)
        dataList.append([k,v])

    # Datetime Objects
    MINUTES_30 = datetime.timedelta(minutes=30)
    LAST_DATETIME = dataList[-1][0]

    # Preprocessing
    print("Preprocessing the target dataset: step 1")
    fullHeadDataList = []
    fullDataList = []

    # Iterate through the available data
    for k, v in dataDict.items(): 
        
        ##### Add to data lists #####
        fullDataList.append(mergeDict({"datetime":k}, v))
        fullHeadDataList.append(mergeDict({"datetime":k}, v))
        
        # Get the time of the next data
        print(k, v)
        k_next = k + MINUTES_30
        
        # If the the next data is unavailable, iterate until the next available data is found
        # Ends when reaching the end of the entire dataset
        while((k_next) not in dataDict) and (k_next <= LAST_DATETIME):
    
            ##### Add to data lists #####
            fullDataList.append({"datetime":k_next})
            fullHeadDataList.append(mergeDict({"datetime":k_next}, v))
            
            # Get the time of the next data
            print(k_next, "-")
            k_next = k_next + MINUTES_30
    

    # Preprocess step 2
    print("Preprocessing the target dataset: step 2")
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
    
    # Save to file
    print("Saving preprocessed target dataset to file: data.pickle")
    with open('data.pickle', 'wb') as handle:
        pickle.dump(fullHeadTailDataList, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    




    # Prediction
    print("Ready for predicion")

    # Load file
    print("Loading the data.pickle as dataset")
    with open('data.pickle', 'rb') as handle:
        fullHeadTailDataList = pickle.load(handle)

    print("Importing required libraries for prediction")
    import numpy as np
    from keras.models import Sequential, model_from_json
    from keras.preprocessing import sequence
    from keras.layers import Dense, Embedding, LSTM, Dropout

    # Prepare data
    print("Preparing two datasets: Enrol+Quota+Wait and Wait-only")
    fullHeadTailDataListEQW = []
    for item in fullHeadTailDataList:
        fullHeadTailDataListEQW.append([item['enrol'],item['quota'],item['wait']])

    fullHeadTailDataListWAIT = []
    for item in fullHeadTailDataList:
        fullHeadTailDataListWAIT.append(item['wait'])

    def getPredictableData(_datetime):
        index = -1
        # Capture datetime
        for ind,row in enumerate(fullHeadTailDataList):
            if (row['datetime'] == _datetime):
                index = ind
                
        print("Index of Predictable Data:", index)
        
        
        # Found corresponding datetime
        if (index != -1):
            res = np.asarray(fullHeadTailDataListEQW[index-1:index+1])
            print("Predictable Data:", res)
            return np.swapaxes(res,0,1).reshape(1,3,2)
        else:
            return np.zeros(1)

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

    def readModel(modelFilenamePrefix):
        structureFilename = modelFilenamePrefix + ".json" 
        with open(structureFilename, "r") as f:
            model_json = f.read()
        model = model_from_json(model_json)

        weightFilename = modelFilenamePrefix + ".h5" 
        model.load_weights(weightFilename)
        return model

    # Apply lookback
    print("Apply lookback on the dataset")
    _,dataY = create_dataset(fullHeadTailDataListWAIT, 2)
    dataX,_ = create_dataset(fullHeadTailDataListEQW, 2)

    print(dataX.shape)
    print(dataY.shape)

    






    # Main execution
    print("Executing")
    print("N1, N2, N3, N4, N5")
    print("Warning: This is a stub.\n")

    return