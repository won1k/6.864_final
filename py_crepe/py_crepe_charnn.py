from keras.models import Model
from keras.optimizers import SGD
from keras.layers import Input, Dense, Dropout, Flatten
from keras.layers.convolutional import Convolution1D, MaxPooling1D


def model(filter_kernels, dense_outputs, maxlen, vocab_size, nb_filter, pooling):
    # input: 2D tensor of integer indices of characters (eg. 1-57). 
    # input tensor has shape (samples, maxlen)
    model = Sequential()
    model.add(Embedding(max_features, 30)) # embed into dense 3D float tensor (samples, maxlen, 256)
    model.add(Reshape(1, maxlen, 256)) # reshape into 4D tensor (samples, 1, maxlen, 256)
    # VGG-like convolution stack
    model.add(Convolution2D(32, 3, 3, 3, border_mode='full')) 
    model.add(Activation('relu'))
    model.add(Convolution2D(32, 32, 3, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(poolsize=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    # then finish up with Dense layers



    # #Define what the input shape looks like
    # inputs = Input(shape=(maxlen, vocab_size), name='input', dtype='float32')

    # #All the convolutional layers...
    # conv = Convolution1D(nb_filter=nb_filter, filter_length=filter_kernels[0],
    #                      border_mode='valid', activation='tanh',
    #                      input_shape=(maxlen, vocab_size))(inputs)
    # conv = MaxPooling1D(pool_length=pooling)(conv)

    #conv1 = Convolution1D(nb_filter=nb_filter, filter_length=filter_kernels[1],
    #                      border_mode='valid', activation='relu')(conv)
    #conv1 = MaxPooling1D(pool_length=3)(conv1)

    # conv2 = Convolution1D(nb_filter=nb_filter, filter_length=filter_kernels[2],
    #                       border_mode='valid', activation='relu')(conv1)

    # conv3 = Convolution1D(nb_filter=nb_filter, filter_length=filter_kernels[3],
    #                       border_mode='valid', activation='relu')(conv2)

    # conv4 = Convolution1D(nb_filter=nb_filter, filter_length=filter_kernels[4],
    #                       border_mode='valid', activation='relu')(conv3)

    # conv5 = Convolution1D(nb_filter=nb_filter, filter_length=filter_kernels[5],
    #                       border_mode='valid', activation='relu')(conv4)
    # conv5 = MaxPooling1D(pool_length=3)(conv5)
    # conv5 = Flatten()(conv5)
    conv = Flatten()(conv)

    #Two dense layers with dropout of .5
    z = Dropout(0.5)(Dense(dense_outputs, activation='relu')(conv))#(conv5))
    z = Dropout(0.5)(Dense(dense_outputs, activation='relu')(z))

    #Output dense layer with softmax activation
    pred = Dense(1, activation='linear', name='output')(z)

    model = Model(input=inputs, output=pred)

    sgd = SGD(lr=0.01, momentum=0.9)
    model.compile(loss='mean_squared_error', optimizer=sgd,
                  metrics=['accuracy'])

    return model
