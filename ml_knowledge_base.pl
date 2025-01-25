% ------------------------------
% Machine Learning Categories
% ------------------------------
category(supervised, "Supervised Learning").
category(unsupervised, "Unsupervised Learning").
category(reinforcement, "Reinforcement Learning").
category(semi_supervised, "Semi-Supervised Learning").
category(deep_learning, "Deep Learning").

% ------------------------------
% Algorithms and Their Categories
% ------------------------------
algorithm("Linear Regression", supervised).
algorithm("Logistic Regression", supervised).
algorithm("Decision Tree", supervised).
algorithm("Random Forest", supervised).
algorithm("Support Vector Machine", supervised).
algorithm("K-Nearest Neighbors", supervised).
algorithm("K-Means", unsupervised).
algorithm("DBSCAN", unsupervised).
algorithm("PCA", unsupervised).
algorithm("Hierarchical Clustering", unsupervised).
algorithm("Q-Learning", reinforcement).
algorithm("Deep Q-Network", reinforcement).
algorithm("GAN", deep_learning).
algorithm("Convolutional Neural Network", deep_learning).
algorithm("Recurrent Neural Network", deep_learning).
algorithm("Transformer", deep_learning).

% ------------------------------
% Descriptions for Algorithms
% ------------------------------
description("Linear Regression", "Linear Regression predicts numerical values based on a linear relationship between features.").
description("Logistic Regression", "Logistic Regression is used for binary classification problems.").
description("Decision Tree", "Decision Trees classify data by splitting it based on feature thresholds.").
description("Random Forest", "Random Forest is an ensemble method using multiple decision trees.").
description("Support Vector Machine", "Support Vector Machines are used for classification and regression tasks.").
description("K-Nearest Neighbors", "K-Nearest Neighbors is a classification algorithm that finds the closest neighbors to a data point.").
description("K-Means", "K-Means clusters data into groups based on similarity.").
description("DBSCAN", "DBSCAN is a density-based clustering algorithm that identifies core, border, and noise points.").
description("PCA", "Principal Component Analysis is a dimensionality reduction technique.").
description("Hierarchical Clustering", "Hierarchical Clustering creates a hierarchy of clusters.").
description("Q-Learning", "Q-Learning is a reinforcement learning algorithm for decision-making.").
description("Deep Q-Network", "Deep Q-Networks use deep learning to enhance Q-Learning.").
description("GAN", "Generative Adversarial Networks generate new data by learning from existing data.").
description("Convolutional Neural Network", "CNNs are used for image and video data analysis.").
description("Recurrent Neural Network", "RNNs process sequential data like time series or text.").
description("Transformer", "Transformers are neural networks used for natural language processing tasks.").

% ------------------------------




% ------------------------------
% Advantages of Algorithms
% ------------------------------
advantage("Linear Regression", "Simple to implement and interpret.").
advantage("Logistic Regression", "Good for binary classification tasks.").
advantage("Decision Tree", "Easy to visualize and interpret.").
advantage("Random Forest", "Reduces overfitting by averaging multiple trees.").
advantage("Support Vector Machine", "Effective for high-dimensional spaces.").
advantage("K-Means", "Efficient for clustering large datasets.").
advantage("DBSCAN", "Can find clusters of arbitrary shapes.").
advantage("PCA", "Reduces dimensionality to speed up computations.").
advantage("GAN", "Generates realistic images or data samples.").

% ------------------------------
% Disadvantages of Algorithms
% ------------------------------
disadvantage("Linear Regression", "Assumes a linear relationship between features.").
disadvantage("Logistic Regression", "Cannot handle complex relationships without transformations.").
disadvantage("Decision Tree", "Prone to overfitting.").
disadvantage("Random Forest", "Hard to interpret due to ensemble nature.").
disadvantage("Support Vector Machine", "Computationally expensive for large datasets.").
disadvantage("K-Means", "Sensitive to the number of clusters (k).").
disadvantage("DBSCAN", "Struggles with varying densities in data.").

% ------------------------------
% Application Areas
% ------------------------------
application("Linear Regression", "Predicting house prices.").
application("Logistic Regression", "Spam email classification.").
application("Decision Tree", "Customer segmentation.").
application("Random Forest", "Fraud detection.").
application("Support Vector Machine", "Image classification.").
application("K-Means", "Market segmentation.").
application("DBSCAN", "Identifying outliers in datasets.").
application("PCA", "Reducing dimensions in image datasets.").
application("Convolutional Neural Network", "Facial recognition.").
application("Recurrent Neural Network", "Predicting stock prices.").
application("Transformer", "Machine translation (e.g., English to French).").

% ------------------------------
% Query Rules
% ------------------------------
% Find category of an algorithm
find_category(Algorithm, CategoryName) :-
    algorithm(Algorithm, Category),
    category(Category, CategoryName).

% Find description of an algorithm
find_description(Algorithm, Description) :-
    description(Algorithm, Description).




% Find advantages of an algorithm
find_advantage(Algorithm, Advantage) :-
    advantage(Algorithm, Advantage).

% Find disadvantages of an algorithm
find_disadvantage(Algorithm, Disadvantage) :-
    disadvantage(Algorithm, Disadvantage).

% Find application areas of an algorithm
find_application(Algorithm, Application) :-
    application(Algorithm, Application).
