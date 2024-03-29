#importing Libraries
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

#Creating the CNN layers
classifier = Sequential()
classifier.add(Conv2D(32,(3,3),input_shape = (64,64,3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2,2)))
classifier.add(Flatten())
classifier.add(Dense(units = 128, activation = 'relu'))
classifier.add(Dense(units = 1, activation = 'sigmoid'))

#Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

#ImageDataGenerator for Image Augumentation
from keras.preprocessing.image import ImageDataGenerator

#rescaling the train and test data
train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

#defining the train and test set
training_set = train_datagen.flow_from_directory('../input/dataset/dataset/training_set',
                                                 target_size=(64, 64),
                                                 batch_size=16,
                                                 class_mode='binary')

test_set = test_datagen.flow_from_directory('../input/dataset/dataset/test_set',
                                            target_size=(64, 64),
                                            batch_size=16,
                                            class_mode='binary')

#fitting the model
history = classifier.fit_generator(training_set,
                         steps_per_epoch=8000,
                         epochs=10,
                         validation_data=test_set,
                         validation_steps=2000)
                    
#predicting the Image as dog or cat                                        
import numpy as np
from keras.preprocessing import image
test_image = image.load_img('../input/dataset/dataset/sample/cat_or_dog_2.jpg',target_size = (64,64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = classifier.predict(test_image)


training_set.class_indices

if result[0][0] == 0 :
    prediction = 'cat'
else:
    prediction = 'dog'
#getting the final answer    
print(prediction)
