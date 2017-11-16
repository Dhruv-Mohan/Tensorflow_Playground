
from Model_interface.Model import Model
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


_SUMMARY_           = False
_BATCH_SIZE_        = 50
_IMAGE_WIDTH_       = 28
_IMAGE_HEIGHT_      = 28
_IMAGE_CSPACE_      = 1
_CLASSES_           = 10
_MODEL_NAME_        = 'Lenet'
_ITERATIONS_        = 200
_LEARNING_RATE_     = 1e-4
_SAVE_DIR_          = 'E:/Ttest'
_RESTORE_           = True

def main():
    ''' Main function'''

    #Load minst data
    mnist = input_data.read_data_sets('MNIST_data', one_hot=True)


    #Construct model
    with tf.name_scope('LeNeT'):
        Simple_DNN = Model(Model_name=_MODEL_NAME_, Summary=_SUMMARY_, \
            Batch_size=_BATCH_SIZE_, Image_width=_IMAGE_WIDTH_, Image_height=_IMAGE_HEIGHT_, Image_cspace=_IMAGE_CSPACE_, Classes=_CLASSES_, Save_dir=_SAVE_DIR_)

        Simple_DNN.Construct_Model()


    #Set loss
        with tf.name_scope('Cross_entropy'):
            Simple_DNN.Set_loss(tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(labels=Simple_DNN.model_dict['Output_ph'], logits=Simple_DNN.model_dict['Output'])))



    #Set optimizer

        with tf.name_scope('Train'):
            Simple_DNN.Set_optimizer(tf.train.AdamOptimizer(_LEARNING_RATE_))

        #Construct op to check accuracy
        Simple_DNN.Construct_Accuracy_op()
        Simple_DNN.Construct_Predict_op()
    #Training block
    with tf.Session() as session:
        session.run(tf.global_variables_initializer())
        Simple_DNN.Construct_Writers()
        Simple_DNN.Train_Iter(iterations=_ITERATIONS_, data=mnist.train, restore=_RESTORE_)
        Predictions = Simple_DNN.Predict(input_data = mnist.train.next_batch(10)[0])


if __name__ == "__main__":
    main()