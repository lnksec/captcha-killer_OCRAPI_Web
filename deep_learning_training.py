from keras.models import *
from keras.layers import *

'''
    ����keras��ܵ����ѧϰģ��(����32λϵͳ�½���ѵ��)
    ԭ��ַ��https://blog.csdn.net/weixin_34959771/article/details/112337901
'''
input_tensor = Input((height, width, 3))
x = input_tensor
for i in range(4):
    x = Convolution2D(32*2**i, 3, 3, activation='relu')(x)
    x = Convolution2D(32*2**i, 3, 3, activation='relu')(x)
    x = MaxPooling2D((2, 2))(x)

x = Flatten()(x)
x = Dropout(0.25)(x)
x = [Dense(n_class, activation='softmax', name='c%d'%(i+1))(x) for i in range(4)]
model = Model(input=input_tensor, output=x)

model.compile(loss='categorical_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])
'''ѵ��ģ��'''
model.fit_generator(gen(), samples_per_epoch=51200, nb_epoch=5,
                    nb_worker=2, pickle_safe=True,
                    validation_data=gen(), nb_val_samples=1280)
'''ѵ��ģ��'''
X, y = next(gen(1))
y_pred = model.predict(X)
plt.title('real: %s\npred:%s'%(decode(y), decode(y_pred)))
plt.imshow(X[0], cmap='gray')