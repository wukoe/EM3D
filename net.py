# build on class based on tensorflow
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import dm
from tensorflow.examples.tutorials.mnist import input_data


# CNN structure
class recnet(object):
    def __init__(self, initopt, *args):
        if initopt == 'new':
            flagNew=True
        elif initopt == 'load':
            flagNew=False
        else:
            raise Exception("invalid init option")


        ### Initialize the graph
        if flagNew:
            cnnlayer, fcnlayer = args[0], args[1]
            cnnlNum = len(cnnlayer)
            fcnlNum = len(fcnlayer) # number of FC layers.
            self.NP = {}

            self.NP['filterSize'] = [x[0] for x in cnnlayer] # filter size
            self.NP['convStride'] = [x[1] for x in cnnlayer]  # convolution strides
            self.NP['filterNum'] = [x[2] for x in cnnlayer]  # feature map number
            self.NP['poolSize'] = [x[3] for x in cnnlayer]  # maxpooling filter size
            self.NP['poolStride'] = [x[4] for x in cnnlayer]  # maxpooling filter strides

            self.NP['fclSize'] = [x[0] for x in fcnlayer]
            self.NP['bDrop'] = [x[1] for x in fcnlayer]

            self.NN = [{} for k in range(1+cnnlNum+1+fcnlNum)]

            initrandn = tf.truncated_normal_initializer(0, stddev=0.1)

        else:
            self.NN = args[0]
            self.NP = args[1]
            cnnlNum, fcnlNum = len(self.NP['filterSize']), len(self.NP['fclSize'])

        #
        self.X = tf.placeholder(tf.float32, [None, 100,100])
        self.Y = tf.placeholder(tf.float32, [None, 100,100])
        # self.fcnKeepProb = tf.placeholder(tf.float32, [fcnlNum])
        # self.flagTrain = tf.placeholder(tf.bool, [1,1])


        ### Architecture construction.
        # Multiple convolution layers.
        self.NN[0]['act'] = tf.reshape(self.X, [-1,28,28,1])  # first layer as input

        for k in range(cnnlNum):
            li=1+k
            if flagNew:
                self.NN[li]['W'] = tf.Variable(initrandn(self.NP['filterSize'][k] + self.NP['filterNum'][k]))
                self.NN[li]['B'] = tf.zeros(self.NP['filterNum'][k])

            self.NN[li]['conv'] = tf.nn.relu(tf.nn.conv2d(self.NN[li-1]['act'], self.NN[li]['W'], strides=self.NP['convStride'][k],
                                                          padding='SAME') + self.NN[li]['B'])
            self.NN[li]['act'] = tf.nn.max_pool(self.NN[li]['conv'], ksize=self.NP['poolSize'][k],strides=self.NP['poolStride'][k],
                                                padding='SAME')

        # Fully Connected layers.
        self.NN[cnnlNum+1]['act'] = tf.reshape(self.NN[cnnlNum]['act'], [-1, self.NP['fclSize'][0][0]])

        for k in range(fcnlNum):
            li=cnnlNum+2+k
            if flagNew:
                self.NN[li]['W'] = tf.Variable(initrandn(self.NP['fclSize'][k]))
                self.NN[li]['B'] = tf.zeros(self.NP['fclSize'][k][1])

            temp = tf.nn.relu(tf.matmul(self.NN[li-1]['act'], self.NN[li]['W']) + self.NN[li]['B'])
            if self.NP['bDrop'][k][0]:
                # use Drop-out for this layer
                self.NN[li]['act'] = tf.nn.dropout(temp, self.NP['bDrop'][k][1])
            else:
                self.NN[li]['act'] = temp

        # Output
        pred = tf.nn.softmax(self.NN[1+cnnlNum+fcnlNum]['act'])


        ### Training & Evaluation.

        # Set Training
        cost = - tf.reduce_sum(self.Y * tf.log(pred)) # Cost
        self.trainOp = tf.train.GradientDescentOptimizer(1e-3).minimize(cost)
        # or: tf.train.AdamOptimizer(1e-4).minimize(CrossEntropy)

        # Accuracy.
        CorrectPrediction = tf.equal(tf.argmax(pred, 1), tf.argmax(self.Y, 1))
        self.acc = tf.reduce_mean(tf.cast(CorrectPrediction, tf.float32))

    # @property
    # def getNN(self):
    #     return self.NN


# """Small config."""
# class netConfig(object):
#     init_scale = 0.1
#     learning_rate = 1.0
#     max_grad_norm = 5
#     num_layers = 2    # numb layer of hidden units (LSTM)
#     num_steps = 20    # step unfold?
#     hidden_size = 200 # hidden layer units
#     keep_prob = 1.0
#     lr_decay = 0.5
#     vocab_size = 10000
#     batch_size = 20
#     max_epoch = 4
#     max_max_epoch = 13

def dataproc(imgtrain,imglabel):
    pass
    return (trim, trlb)

def train_epoch(sess, net, data, opt):
    snum=len(data[0])
    batchI=dm.cutseg(snum,opt['batchSize'])
    batchNum=len(batchI)
    batchOrder=np.random.permutation(batchNum)
    for k in range(batchNum):
        idx=batchI[batchOrder[k]]
        _ = sess.run([net.trainOp], feed_dict={net.X: data[0][idx[0]:idx[1],:], net.Y: data[1][idx[0]:idx[1],:]})
        # ps=sess.run([net.s],feed_dict={net.X:batch[0], net.Y:batch[1], net.fcnKeepProb:[0.5 for k in range(len(PFCN))]})

    # Test accuracy
    acc=sess.run([net.acc], {net.X: data[0], net.Y: data[1]})
    return acc

### Main
def main(opt,*args):
    # Config [filter size, conv strides, filter num, pool size, pool strides]
    PCNN=(([5, 5, 1], [1, 1, 1, 1], [32], [1, 2, 2, 1], [1, 2, 2, 1]),
        ([5,5,32], [1,1,1,1], [64], [1,2,2,1], [1,2,2,1]))
    PFCN=(([7 * 7 * 64, 1024], [True, 0.5]),
          ([1024, 10], [False, 0.5]))

    # Load data.
    import dataloader
    data=[]
    data[0] = dataloader.imgtiff('/media/wb/Working/devWorks/EM3D/train-input.tif')
    data[1] = dataloader.imgtiff('/media/wb/Working/devWorks/EM3D/train-input.tif')

    data=dataproc(data)

    # Set up graph.
    if len(args) == 0:
        flagNewGraph=True
        with tf.Graph().as_default() as G:
            net=recnet('new', PCNN, PFCN)
    else:
        flagNewGraph=False
        G = args[0]
        with G.as_default():
            net=recnet('load', args[1], args[2])

    with tf.Session(graph=G) as sess:
        sess.run(tf.initialize_all_variables())

        lor = []
        for k in range(opt['epochNum']):
            tp = train_epoch(sess, net, data, opt)
            lor.append(tp)
            print('|',end='')
    print('\n')
    plt.plot(lor)

    return (G,net.NN,net.NP)