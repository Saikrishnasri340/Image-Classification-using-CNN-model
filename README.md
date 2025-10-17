# Image-Classification-using-CNN-mode

This project performs image classification to predict whether an image is real or computer-generated (AI-generated). It utilizes Convolutional Neural Networks (CNNs) and the Xception model for accurate feature extraction and classification. The dataset used for training and testing is sourced from Kaggle, containing a diverse collection of real and AI-generated images. This project can be used for educational purposes or as a foundation for building AI-generated image detection applications.


## Features


1. Binary Image Classification
 --Predicts whether an image is real or computer-generated (AI-generated).

2. Multiple Models Supported
 --Custom CNN: A 3-layer convolutional network for baseline performance.
 --Xception Model: Pre-trained on ImageNet for advanced feature extraction  and higher accuracy.

3. Dataset Handling
 --Uses a Kaggle dataset of real and AI-generated images.
 --Supports train, validation, and test splits.

4. Data Preprocessing
 --Automatic image resizing to 224x224 pixels.
 --Normalization of pixel values (scaling to [0,1]).
 --Data augmentation supported through ImageDataGenerator.

5. Model Training and Evaluation
 --Tracks training and validation accuracy and loss.
 --Evaluates model performance on a separate test set.

6. Model Saving
 --Save trained models (CNN_model.h5 and Xception_model.h5) for future inference.

7. Visualization
 --Plots training/validation accuracy and loss curves to monitor performance.

# Datasets

Link:
https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images?resource=download




 
