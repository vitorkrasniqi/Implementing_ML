from developing_the_model import *

def compile():
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

compile()

model.save("my_model.h5")
