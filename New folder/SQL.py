import pypyodbc as obdc
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup


# Kết nối đến cơ sở dữ liệu SQL Server sử dụng Windows Authentication
DRIVER_NAME='SQL SERVER'
SERVER__NAME = 'DESKTOP-O4719F3'
DATABASE_NAME = 'EcormerceTechnology'
connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER__NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""
conn = obdc.connect(connection_string)
#print(conn)
sql_query1= "SELECT CustomerID,CustomerName,Address,City,CustomerPreferences FROM Customer"
sql_query2="SELECT ProductID,ProductName,Category,UnitPrice FROM Products"
sql_query3 ="SELECT TransactionID,CustomerID,ProductID,Quantity,TransactionTime,UnitPrice FROM SalesTransations"
sql_query4 ="SELECT AccessID,TransactionID,AvgTimeOnPage,VisitedPage,CustomerID FROM WebsiteAccess"
df1 = pd.read_sql(sql_query1, conn)
df2 = pd.read_sql(sql_query2, conn)
df3 = pd.read_sql(sql_query3, conn)
df4 = pd.read_sql(sql_query4, conn)

# Close the connection
conn.close()

# Display the DataFrame
df2_cleaned = df2.dropna()
df4_cleaned = df4.dropna()
#print(df2_cleaned.isnull().sum())
# Loại bỏ các hàng chứa giá trị NaN
df3_cleaned = df3.dropna()

# Tính tổng số lượng giá trị trùng lặp
total_duplicates = df4_cleaned.duplicated().sum()

#print("All Duplicates:", total_duplicates)

# Loại bỏ các hàng chứa giá trị trùng lặp từ DataFrame df3
df4_unique = df4_cleaned.drop_duplicates()

# Hiển thị DataFrame sau khi loại bỏ giá trị trùng lặp
#print(df4_unique.duplicated().sum())
df1['customername'] = df1['customername'].str.upper()
df1['address'] = df1['address'].str.replace(' Street', '')
df1['city'] = df1['city'].str.replace(' City', '')
df3_cleaned['transactiontime'] = pd.to_datetime(df3_cleaned['transactiontime'])

#print(df1)
#print(df3_cleaned.dtypes)

#print(df3_cleaned)

# Xem một số mẫu dữ liệu đầu tiên của DataFrame df3_cleaned
print("First few rows of df3_cleaned:")
print(df3_cleaned.head())

print("\nBasic info of df3_cleaned:")
print(df3_cleaned.info())

print("\nDescriptive statistics of numeric variables in df3_cleaned:")
print(df3_cleaned.describe())

plt.figure(figsize=(8, 6))
sns.histplot(df3_cleaned['quantity'], kde=True)
plt.title('Histogram of Quantity')
plt.xlabel('Quantity')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(data=df3_cleaned, x='transactiontime', y='unitprice')
plt.title('Boxplot of UnitPrice by TransactionTime')
plt.xlabel('TransactionTime')
plt.ylabel('UnitPrice')
plt.xticks(rotation=45)
plt.show()

correlation_matrix = df3_cleaned.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap of Variables in df3_cleaned')
plt.show()
