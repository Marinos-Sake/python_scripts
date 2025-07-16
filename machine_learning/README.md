# Customer Churn Prediction

## Data Source  
The data used comes from the [Iranian Churn Dataset](https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset)

---

## Project Objective  
Develop a prediction model to accurately identify customer churn, performing well on both training and unseen data.

---

## Methodology

### Data Exploration & Preprocessing  
- Loaded and inspected dataset (missing values, data types).  
- Calculated feature correlations with target (Churn).  
- Dropped less relevant features: 'Call Failure', 'Age', 'Age Group'.  

### Model Training  
- Split data into training (85%) and testing (15%) sets.  
- Used Random Forest Classifier with 500 trees and balanced class weights.  

---

## Results  
- Achieved ~93.7% accuracy on test data.  
- High precision & recall on both classes, slightly lower on churn prediction.  
- Generated confusion matrix with labeled cells for better interpretability.  
- Confusion matrix saved as `confusion_matrix_labeled.png`.

---

## Conclusion  
Random Forest with 500 estimators and balanced classes gave strong predictive performance, useful for customer retention efforts.

---

## Dependencies  
- Python 3.x  
- numpy  
- pandas  
- matplotlib  
- seaborn  
- scikit-learn
