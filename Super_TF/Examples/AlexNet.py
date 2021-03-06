
from Model_interface.Model import Model
import tensorflow as tf
from Dataset_IO.Classification.Dataset_reader_classification import Dataset_reader_classification

_SUMMARY_           = True
_BATCH_SIZE_        = 5
_IMAGE_WIDTH_       = 299
_IMAGE_HEIGHT_      = 299
_IMAGE_CSPACE_      = 3
_CLASSES_           = 10
_MODEL_NAME_        = 'Inception_resnet_v2a'
_ITERATIONS_        = 200000
_TEST_INTERVAL_     = 100
_LEARNING_RATE_     = 0.01
_SAVE_DIR_          = 'G:\\TFmodels\\Vgg'
_RESTORE_           = False
_DATASET_PATH_      = 'Cifar10_train.tfrecords'
_DROPOUT_ = 0.7
_STATE_         = 'Train'
_SAVE_ITER_     = 2000
_GRAD_NORM_     = 0.5
_RENORM_        = False

def writer_pre_proc(images):
    print('adding to graph')
    resized_images = tf.image.resize_images(images, size=[_IMAGE_HEIGHT_,_IMAGE_WIDTH_])
    rgb_image_float = tf.image.convert_image_dtype(resized_images, tf.float32) 
    return rgb_image_float

def main():
    ''' Main function'''

    #Load minst data
    dummy_reader = Dataset_reader_classification(filename=_DATASET_PATH_, num_classes=_CLASSES_)
    dummy_reader.pre_process_image(writer_pre_proc)


    #Construct model
    
    with tf.name_scope('Alexnet'):
        Simple_DNN = Model(Model_name=_MODEL_NAME_, Summary=_SUMMARY_, \
                Batch_size=_BATCH_SIZE_, Image_width=_IMAGE_WIDTH_, Image_height=_IMAGE_HEIGHT_,\
               Image_cspace=_IMAGE_CSPACE_, Classes=_CLASSES_, Save_dir=_SAVE_DIR_, \
               State=_STATE_, Dropout=_DROPOUT_, Grad_norm=_GRAD_NORM_, Renorm=_RENORM_)
        Optimizer_params_adam = {'beta1': 0.9, 'beta2':0.999, 'epsilon':0.01}
        Simple_DNN.Set_optimizer(starter_learning_rate= _LEARNING_RATE_, Optimizer='ADAM', Optimizer_params=Optimizer_params_adam, decay_steps=10000)
        Simple_DNN.Construct_Accuracy_op()

    #Training block
    config = tf.ConfigProto(log_device_placement=True, allow_soft_placement=True)
    with tf.Session(config=config) as session:
        session.run(tf.global_variables_initializer())
        Simple_DNN.Construct_Writers()
        print('Writers constructed')
        Simple_DNN.Train_Iter(iterations=_ITERATIONS_, data=dummy_reader, restore=_RESTORE_, save_iterations=_SAVE_ITER_, log_iteration=_TEST_INTERVAL_)
        


if __name__ == "__main__":
    main()
