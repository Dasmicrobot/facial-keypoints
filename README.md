[//]: # (Image References)

[image1]: ./images/obamas_with_keypoints.png "Facial Keypoint Detection"

# Facial Keypoint Detection

![Facial Keypoint Detection][image1]

## Webapp with OpenCV

`app` directory contains web application which serves as a demo to show how face 
features are detected by using a webcam.

App uses OpenCV with HAAR cascade to detect features on faces.

[Read more](app/README.md)

## Jupyter Notebook (CV_project.ipynb)

- First part shows how to use OpenCV to work with face recognition
- Second part uses Tensorflow to build CNN and achieve similar outcomes as OpenCV


### Requirements

1. Create (and activate) a new environment with Python 3.5 and the `numpy` package.

	- __Linux__ or __Mac__: 
	```
	conda create --name aind-cv python=3.5 numpy
	source activate aind-cv
	```
	- __Windows__: 
	```
	conda create --name aind-cv python=3.5 numpy scipy
	activate aind-cv
	```

2. Install/Update TensorFlow.
	- Option 1: __To install TensorFlow with GPU support__, follow [the guide](https://www.tensorflow.org/install/) to install the necessary NVIDIA software on your system.
	```
	pip install tensorflow-gpu==1.1.0
	```
	- Option 2: __To install TensorFlow with CPU support only__:
	```
	pip install tensorflow==1.1.0
	```

4. Install/Update Keras.
 ```
pip install keras -U
```

5. Switch [Keras backend](https://keras.io/backend/) to TensorFlow.
	- __Linux__ or __Mac__: 
	```
	KERAS_BACKEND=tensorflow python -c "from keras import backend"
	```
	- __Windows__: 
	```
	set KERAS_BACKEND=tensorflow
	python -c "from keras import backend"
	```

6. Install a few required pip packages (including OpenCV).
```
pip install -r requirements.txt
```

### Data

All of the data you'll need to train a neural network is in the subdirectory `data`. In this folder are a zipped training and test set of data.

1. Navigate to the data directory
```
cd data
```

2. Unzip the training and test data (in that same location). If you are in Windows, you can download this data and unzip it by double-clicking the zipped files. In Mac, you can use the terminal commands below.
```
unzip training.zip
unzip test.zip
```

You should be left with two `.csv` files of the same name. You may delete the zipped files.

*Troubleshooting*: If you are having trouble unzipping this data, you can download that same training and test data on [Kaggle](https://www.kaggle.com/c/facial-keypoints-detection/data).

Now, with that data unzipped, you should have everything you need!
