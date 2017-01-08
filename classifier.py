
import pandas
import numpy

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix

from keras.layers import Dense, Activation, LSTM, SimpleRNN, GRU, Dropout, Input, Merge, Lambda, Embedding
from keras.models import Sequential, Model, load_model
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.regularizers import l2
from keras.utils import np_utils


class Classifier(object):
    def __init__(self, input_dim, batch_size=128, epochs=500):
        self.input_dim = input_dim
        self.batch_size = batch_size
        self.epochs = epochs
        self._model()


    def _model(self):
        self.model = Sequential()

        self.model.add(Dense(1024, input_dim=self.input_dim, init='uniform', activation='relu'))
        self.model.add(Dropout(0.5))
        # self.model.add(Dense(2048, activation='relu'))
        # self.model.add(Dropout(0.5))
        # self.model.add(Dense(1024, activation='relu'))
        # self.model.add(Dropout(0.5))
        # self.model.add(Dense(512, activation='relu'))
        # self.model.add(Dropout(0.5))
        # self.model.add(Dense(256, activation='relu'))
        # self.model.add(Dropout(0.5))
        # self.model.add(Dense(128, activation='relu'))
        # self.model.add(Dropout(0.5))
        # self.model.add(Dense(64, activation='relu'))
        # self.model.add(Dropout(0.5))
        # self.model.add(Dense(32, activation='relu'))
        # self.model.add(Dropout(0.5))
        
        self.model.add(Dense(3, activation='softmax'))

        self.model.compile(loss='categorical_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])


    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train,
                       shuffle=True,
                       nb_epoch=self.epochs,
                       batch_size=self.batch_size,
        )

        
    def evaluate(self, X_test, y_test):
        score, acc = self.model.evaluate(X_test, y_test, batch_size=self.batch_size)
        print
        print 'Test score:', score
        print 'Test accuracy:', acc

        
    def predict(self, X_test, verbose=1):        
        y = self.model.predict_classes(X_test, verbose=verbose)
        p = self.model.predict_proba(X_test, verbose=verbose)
        return y, p



def main():
    DATASET = 'train.tsv'
    LABELS = 'labels.tsv'

    numpy.random.seed(7) #used in the shuffle keras function 

    scaler = MinMaxScaler(feature_range=(0, 1))
    X = scaler.fit_transform(pandas.read_csv(DATASET).values)
    y = np_utils.to_categorical(pandas.read_csv(LABELS).values)

    test_size = int(X.shape[0]*0.3)
    X_test, y_test = X[0:test_size], y[0:test_size]
    X_train, y_train = X[test_size:], y[test_size:]
    
    print X.shape, y.shape
    classifier = Classifier(820)
    classifier.train(X_train, y_train)
    classifier.evaluate(X_test, y_test)

    y_pred, p = classifier.predict(X_test)

    y_pred = y_pred
    
    print(classification_report(numpy.argmax(y_test, axis=1), y_pred))
    print('*'*80)
    print(confusion_matrix(numpy.argmax(y_test, axis=1), y_pred))
if __name__ == '__main__':
    main()
