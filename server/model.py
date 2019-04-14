"""

This creates the model object that:

1. creates an instance of the appropriate model
2. trains a model given the right data
3. stores the weights and generally manages the instance of the model

"""

# from keras.applications.inception_v3 import InceptionV3
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K


class Model:

	"""

	Instance variables

		directory - where to store the images and weights of the model

	Instance Methods

		train(img_urls, annotations)
		predict(img_url)

	"""

	def __init__(self, directory):
		self.directory = directory
		self.create_model()

	def create_model():
		"""
		Creates object classification model

		Model:

		"""

		# create the base pre-trained model
		base_model = InceptionV3(weights='imagenet', include_top=False)
		# add a global spatial average pooling layer
		x = base_model.output
		x = GlobalAveragePooling2D()(x)
		# let's add a fully-connected layer
		x = Dense(1024, activation='relu')(x)
		# and a logistic layer -- let's say we have 200 classes
		predictions = Dense(1, activation='softmax')(x)
		# this is the model we will train
		model = Model(inputs=base_model.input, outputs=predictions)

    def train_generator(img_urls, annotations, batch_size=8):
