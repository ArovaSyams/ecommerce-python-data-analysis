# Stackware E-commerce Data Analysis
I try to analysis data at Stackware E-commerce, focusing on gaining deep insights into customer and seller demographics, seller profitability, top-selling product categories, and seller revenue performance. By implementing a structured and measurable workflow, including data wrangling, cleaning, exploratory analysis, data visualization, and the creation of interactive dashboards, I successfully delivered valuable and easily understandable insights to stakeholders. This analysis not only identified growth opportunities but also investigated the drivers of seller revenue fluctuations, aiding the platform in making smarter decisions to optimize its business performance. 

## Define Business Questions
- What is the demographic of customers and sellers on our E-Commerce platform?
- Which sellers generate the highest and lowest profits?
- Which product categories sell the most and the least?
- How is the revenue performance of sellers in the past few months?
- What are the causes of increasing and decreasing seller revenue?

## Conclusion From Business Questions
Conclusion question 1:
The majority of customers reside in the state of SP (Sao Paulo).
The majority of sellers also reside in the state of SP (Sao Paulo).

Conclusion question 2:
Based on the visual data above, the seller generating the highest profit has the first 3 digits of ID 532,
while the seller generating the lowest profit has the first 3 digits of ID cf6.

Conclusion question 3:
Bed bath table is the category with the highest sales,
while security and service is the category with the lowest sales volume.

Conclusion question 4:
It can be observed that from October 2016 to April 2018, the sales trend continuously increased.
After April 2018 until October 2018, the trend reversed and declined, with the most significant decline occurring from August 2018 to October 2018.

Conclusion question 5:
After conducting several tests to find the relationship between revenue, order count, and rating, it can be concluded that the fluctuation in revenue is primarily influenced by the number of orders.
Moreover, the increase or decrease in order count is not affected by the rating of order reviews. 

## Stackware E-Commerce Dashboard
I also make the website-based dashboard powered by Streamlit to summarize all the analysis result on visualization and make stakeholder to do desirable range of date on data.
### Setup Environment
```
pipenv install 
pipenv shell
pipenv install numpy pandas matplotlib seaborn streamlit babel
```

### Run Streamlit
```
streamlit run dashboard.py
```
### Link Streamlit Cloud
https://ecommerce-python-data-analysis.streamlit.app/

![dashboard e-commerce](image.png)

### Cluster Analisis
This method is used to seek insights into the causes of increases and decreases in seller revenue.

Seller revenue is analyzed using cluster analysis conducted per seller and per month, with the following three identified relationships:
1. Identifying the relationship between seller revenue and order count.
2. Identifying the relationship between order count and order review.
3. Identifying the relationship between seller revenue and order review.

