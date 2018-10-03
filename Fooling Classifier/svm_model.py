import helper
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
def fool_classifier(test_data): ## Please do not change the function defination...
    ## Read the test data file, i.e., 'test_data.txt' from Present Working Directory...
    
    
    ## You are supposed to use pre-defined class: 'strategy()' in the file `helper.py` for model training (if any),
    #  and modifications limit checking
    strategy_instance=helper.strategy() 
    #parameters={'gamma':20,'C':1, 'kernel':'liner', 'degree':3, 'coef0':0.1}
    parameters = {}
    parameters['gamma'] = "auto"
    parameters['C'] = 10
    parameters['kernel'] = "linear"
    parameters['degree'] = 3
    parameters['coef0'] = 0.0
    class_0_words = strategy_instance.class0 #二维数组
    class_1_words = strategy_instance.class1
    all_words = []
    for line in class_0_words:
        list_line = ' '.join(line)
        all_words.append(list_line)
    y_train = [0 for _ in range(len(all_words))]
    for line in class_1_words:
        list_line = ' '.join(line)
        all_words.append(list_line)
        y_train.append(1)
    Vectorizer = TfidfVectorizer()
    X_train = Vectorizer.fit_transform(all_words)
    tfidf_train = TfidfTransformer().fit(X_train)
    result = strategy_instance.train_svm(parameters, X_train, y_train)
#    print(X_train[0])
#    print(X_test[0])
    X_train_array = X_train.toarray()
#X_test_array = X_test.toarray()
    max_list_0 = []
    for i in range(len(X_train_array[0])):
        sum_all = 0
        count = 0
        for j in range(len(class_0_words)):
            sum_all += X_train_array[j][i]
            count += 1
        max_list_0.append(sum_all/count)
    max_list_1 = []
    for i in range(len(X_train_array[0])):
        sum_all = 0
        count = 0
        for j in range(len(class_0_words),len(class_0_words)+ len(class_1_words)):
            sum_all += X_train_array[j][i]
            count += 1
        max_list_1.append(sum_all/count)
    list_compare ={}
    for i in range(len(max_list_0)):
        list_compare[Vectorizer.get_feature_names()[i]] = max_list_0[i] - max_list_1[i]
    sort_dict = sorted(list_compare.items(),key = lambda x:x[1],reverse = True)[:20]
    print(sort_dict)
    test_data = []
    with open('test_data.txt', 'r') as file1:
        for line in file1:
            for i in sort_dict:
                line += ' ' + i[0]
            test_data.append(line)
    y_test = [1 for _ in range(len(test_data))]
    X_test_1 = Vectorizer.transform(test_data)
    X_test = tfidf_train.transform(X_test_1)
#print(Vectorizer.get_feature_names()[a])
    print(result.score(X_test,y_test))
    ## Write out the modified file, i.e., 'modified_data.txt' in Present Working Directory...
    
    
    ## You can check that the modified text is within the modification limits.
    #modified_data='./modified_data.txt'
    #assert strategy_instance.check_data(test_data, modified_data)
    #return strategy_instance ## NOTE: You are required to return the instance of this class.
fool_classifier('test_data.txt')
