from naive_bayes import NaiveBayes
import csv
import pandas as pd

class EmotionDetector:
    def __init__(self):
        # 0 - эмоции
        # 1 - предложение

        self.naive_bayes = NaiveBayes([0, 1])
        # self.test=pd.read_csv('data\\feedback.csv').apply(lambda x: x.lower() )

        # 0 - эмоции
        # 1 - предложение
        self.naive_bayes = NaiveBayes([0, 1])


    def train(self):
        train = pd.read_csv('data\\data(training).csv', delimiter=';', encoding='CP1251', header=None).apply(lambda x: x.str.lower())
        train.columns = ['X', 'Y']
        print('Количесво отзывов в обучающем наборе: ' + str(train.shape[0]))
        train_emotions = train[train['Y'] == 'эмоции']
        train_propose = train[train['Y'] == 'предложение']
        for i in train_emotions.index:
            self.naive_bayes.train(0, train_emotions['X'][i])

        for i in train_propose.index:
            self.naive_bayes.train(1, train_propose['X'][i])

    def classify(self):
        train = pd.read_csv('data\\data(testing).csv', delimiter=';', encoding='CP1251', header=None).apply(lambda x: x.str.lower())
        train.columns = ['X', 'Y']
        # train.columns = ['X']
        results = []
        for i in train.index:
            res = self.naive_bayes.classify(train['X'][i])
            cur_class='эмоции' if res==0 else 'предложение'
            results.append({'X': train['X'][i], 'prediction': cur_class, 'Y': train['Y'][i]})
            # results.append({'X': train['X'][i], 'prediction': res})
                # print(res)
        top_features = self.naive_bayes.get_stat()[:100]
        self._write_results(results, top_features)

    def _write_results(self, results, top_features):
        open('results(14.12).csv', 'w').close()
        open('top_features.csv', 'w').close()
        with open('results(14.12).csv', 'w+', newline='') as results_csv:
            writer = csv.DictWriter(results_csv, fieldnames=['sentences', 'prediction', 'Y'], delimiter=';')
            # writer = csv.DictWriter(results_csv, fieldnames=['sentences', 'prediction'], delimiter=';')
            writer.writeheader()
            for result in results:
                writer.writerow({'sentences': result['X'], 'prediction': result['prediction'], 'Y': result['Y']})
                # writer.writerow({'sentences': result['X'], 'prediction': result['prediction']})
        with open('top_features.csv', 'w+', newline='') as results_csv:
            writer = csv.DictWriter(results_csv, fieldnames=['feature', 'weight'], delimiter=';')
            writer.writeheader()
            for feature in top_features:
                writer.writerow({'feature': feature[0], 'weight': float(feature[1])})

    def cross_check(self):
        predicted=pd.read_csv('results(14.12).csv', sep=';', encoding='CP1251')
        print('Количесво отзывов в тестовом наборе: '+str(predicted.shape[0]))
        count_zero_mistakes=0
        count_ones_mistakes=0
        for i in predicted.index:
            if predicted['prediction'][i]=='эмоции' and predicted['Y'][i]=='предложение':
                count_zero_mistakes+=1
            if predicted['prediction'][i]=='предложение' and predicted['Y'][i]=='эмоции':
                count_ones_mistakes+=1
        print('Эмоции как предложение: '+str(count_zero_mistakes))
        print('Предложение как эмоции: '+str(count_ones_mistakes))
        print('Точность классификации: '+str(1-((count_zero_mistakes+count_ones_mistakes)/predicted.shape[0])))

if __name__ == "__main__":
    detector=EmotionDetector()
    detector.train()
    detector.classify()
    detector.cross_check()
