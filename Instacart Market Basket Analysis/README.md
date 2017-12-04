# Instacart Market Basket Analysis  
## Objectives  
Instacart is a national-wide company that provides same-day grocery delivery services. Last year, over 3 million orders were placed on Instacart from over 206 thousands of users on 50 thousands of products.  

When a customer dose grocery shopping online, it's inconvenient for him/her to look though thousands of products to find out what he/she wants to buy. In addition, not everyone has a to-buy-list. Sometimes people would just decide to purchase the products when they actually see them. A “buy-it-again” section on Instacart website will greatly help with this situation. Accurately predicting the products that a customer want to buy will both save time for customers and increase the revenue for Instacart.  

The objective of this project was using XGBoost model to predict what products will be repurchased in a customer's next order based on last years’ orders on Instacart.  

## Performance metric  
F1 score was chosen as the performance metric. Accurately predicting the re-purchased products has two meanings. First, we want to make sure that we select all the products the customer will buy. Otherwise, customers have to spend time searching for them or Instacart may lose the revenue of the missing products. Second, among all the products that we select, all of them should be repurchased by the customer. Otherwise we will waste a valuable space in the buy-it-again window. F1 score takes both these two conditions into account.  

## Feature Engineering  
Three types of features were generated for each user-product combination.   
1) User-related features: such as user total order number, user average order interval, time since user's last order  
2) Product-related features: such as product average reorder ratio, product average order interval  
3) User-product-related features: such as time since user's last purchase of this product, average user product order interval, average user product reorder ratio  


## Model  
### Baseline model  
A baseline model was build by predicting all the products that a customer purchased last time will be repurchased in the new order. The baseline model had a F1 score of 0.336  

### Xgboost model  
Xgboost model was developed based on the features. After parameter optimization, it improved the F1 score to 0.376.


