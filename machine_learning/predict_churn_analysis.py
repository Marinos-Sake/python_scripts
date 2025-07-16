import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load and inspect the dataset
customer_churn = pd.read_csv('Customer_Churn.csv')

print(customer_churn.head())  # Display first 5 rows

print("Columns of dataset: ")
print(customer_churn.columns)  # Show column names

print("\nChecking for missing values: ")
print(customer_churn.isnull().sum())  # Check for missing values in each column

print("Info customers: ")
print(customer_churn.info())  # Show dataframe info: data types and non-null counts

print("Checking feature correlations with target variable (Churn):")
corr_matrix = customer_churn.corr()
print(corr_matrix['Churn'].sort_values(ascending=False))  # Correlations with target variable

# Drop less important features from the feature set
x = customer_churn.drop(['Churn', 'Call  Failure', 'Age', 'Age Group'], axis=1)
y = customer_churn['Churn']  # Target variable

# Split data into training (85%) and testing (15%) sets
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.15, random_state=42)

# Initialize and train the Random Forest Classifier with balanced class weights
model = RandomForestClassifier(n_estimators=500, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Print accuracy and classification report
print("Accuracy: ", accuracy_score(y_test, y_pred))
print("Classification report: ", classification_report(y_test, y_pred))

# Compute the confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Create string labels for confusion matrix cells (e.g. True Positives)
labels = np.array([["True Negatives", "False Positives"],
                   ["False Negatives", "True Positives"]])

# Combine labels and counts (e.g. "True Positives\n46")
annot = np.array([[f"{labels[i, j]}\n{cm[i, j]}" for j in range(2)] for i in range(2)])

# Set figure size for better visualization
plt.figure(figsize=(8, 6))

# Plot heatmap of confusion matrix with annotations and styling
sns.heatmap(cm, annot=annot, fmt='', cmap='Blues', cbar=True, linewidths=1.5, square=True)

# Label axes
plt.xlabel('Predicted Label')
plt.ylabel('Actual Label')

# Set plot title
plt.title('Confusion Matrix with Labels')

# Customize tick labels for predicted classes
plt.xticks(ticks=[0, 1], labels=['Predicted: 0 (Stay)', 'Predicted: 1 (Leave)'])

# Customize tick labels for actual classes
plt.yticks(ticks=[0, 1], labels=['Actual: 0 (Stay)', 'Actual: 1 (Leave)'], rotation=0)

# Adjust layout for neatness
plt.tight_layout()

# Save the plot image
plt.savefig("confusion_matrix_labeled.png")

# Show the confusion matrix plot
plt.show()
