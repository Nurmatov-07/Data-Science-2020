import pyodbc

server = 'mysqlserver8112.database.windows.net'
database = 'mySampleDatabase'
username = 'azureuser'
password = 'Parol-123'
driver = '{ODBC Driver 17 for SQL Server}'

connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
cursor = connection.cursor()
#SELECT SalesPerson,
#          ISNULL(CAST(FirstName AS VARCHAR(30)), 
#                 CASE WHEN GROUPING(FirstName)=1 AND GROUPING(SalesPerson)=0 
#                      THEN 'Subtotal' 
#                      ELSE 'GrandTotal' END) AS FirstName,
#          ISNULL(cast(Name AS VARCHAR(30)),
#                CASE 
#                    WHEN GROUPING(Name) = 1
#                    THEN 'None' end)
#        AS Name,
#          SUM(ListPrice) AS itog,
#          GROUPING(SalesPerson) AS grouping_salesperson,
#          GROUPING(Name) AS grouping_name
#   FROM [SalesLT].[Customer]
#    JOIN [SalesLT].[SalesOrderHeader]
#    ON [SalesLT].[Customer].CustomerID = [SalesLT].[SalesOrderHeader].CustomerID
#    JOIN [SalesLT].[SalesOrderDetail]
#    ON [SalesLT].[SalesOrderHeader].SalesOrderID = [SalesLT].[SalesOrderDetail].SalesOrderID
#    JOIN [SalesLT].[Product] 
#    ON [SalesLT].[SalesOrderDetail].ProductID = [SalesLT].[Product].ProductID
#    GROUP BY 
#    ROLLUP (SalesPerson, FirstName, Name)
while(True):
    response = int(input('Выберите запрос от 1 до 6: \n'))
    if response == 1: #два варианта
        cursor.execute("""SELECT SalesPerson,
          ISNULL(CAST(FirstName AS VARCHAR(30)), 
                 CASE WHEN GROUPING(FirstName)=1 AND GROUPING(SalesPerson)=0 
                      THEN 'Subtotal' 
                      ELSE 'GrandTotal' END) AS FirstName,
          ISNULL(cast(Name AS VARCHAR(30)),
                CASE 
                    WHEN GROUPING(Name) = 1
                    THEN 'None' end)
        AS Name,
          SUM(ListPrice - UnitPriceDiscount) AS itog,
          GROUPING(SalesPerson) AS grouping_salesperson,
          GROUPING(Name) AS grouping_name
   FROM [SalesLT].[Customer]
    JOIN [SalesLT].[SalesOrderHeader]
    ON [SalesLT].[Customer].CustomerID = [SalesLT].[SalesOrderHeader].CustomerID
    JOIN [SalesLT].[SalesOrderDetail]
    ON [SalesLT].[SalesOrderHeader].SalesOrderID = [SalesLT].[SalesOrderDetail].SalesOrderID
    JOIN [SalesLT].[Product] 
    ON [SalesLT].[SalesOrderDetail].ProductID = [SalesLT].[Product].ProductID
    GROUP BY 
    ROLLUP (SalesPerson, FirstName, Name)""")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    elif response == 2:
            cursor.execute("""SELECT CountryRegion, AddressLine1, [SalesLT].[SalesOrderHeader].CustomerID, Name, ShipToAddressID, BillToAddressID, SUM(TotalDue) AS itog
            FROM [SalesLT].[Product]
            JOIN [SalesLT].[SalesOrderDetail]
            ON [SalesLT].[Product].ProductID = [SalesLT].[SalesOrderDetail].ProductID
            JOIN [SalesLT].[SalesOrderHeader]
            ON [SalesLT].[SalesOrderDetail].SalesOrderID = [SalesLT].[SalesOrderHeader].SalesOrderID
            JOIN [SalesLT].[Customer] 
            ON [SalesLT].[SalesOrderHeader].CustomerID = [SalesLT].[Customer].CustomerID
            JOIN [SalesLT].[CustomerAddress]
            ON [SalesLT].[Customer].CustomerID = [SalesLT].[CustomerAddress].CustomerID
            JOIN [SalesLT].[Address]
            ON [SalesLT].[CustomerAddress].AddressID = [SalesLT].[Address].AddressID
            GROUP BY
            Grouping SETS (CountryRegion, AddressLine1, [SalesLT].[SalesOrderHeader].CustomerID, Name, ShipToAddressID, BillToAddressID)""")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
                #ROLLUP (CountryRegion, StateProvince, City), OrderQty, UnitPrice, UnitPriceDiscount, Comment;
            #SELECT CountryRegion, AddressLine1, [SalesLT].[SalesOrderHeader].CustomerID, Name, ShipToAddressID, BillToAddressID, SUM(TotalDue) AS itog
            #FROM [SalesLT].[Product]
            #JOIN [SalesLT].[SalesOrderDetail]
            #ON [SalesLT].[Product].ProductID = [SalesLT].[SalesOrderDetail].ProductID
            #JOIN [SalesLT].[SalesOrderHeader]
            #ON [SalesLT].[SalesOrderDetail].SalesOrderID = [SalesLT].[SalesOrderHeader].SalesOrderID
            #JOIN [SalesLT].[Customer] 
            #ON [SalesLT].[SalesOrderHeader].CustomerID = [SalesLT].[Customer].CustomerID
            #JOIN [SalesLT].[CustomerAddress]
            #ON [SalesLT].[Customer].CustomerID = [SalesLT].[CustomerAddress].CustomerID
            #JOIN [SalesLT].[Address]
            #ON [SalesLT].[CustomerAddress].AddressID = [SalesLT].[Address].AddressID
            #GROUP BY
            #Grouping SETS ((AddressLine1), (ShipToAddressID), (BillToAddressID)), [SalesLT].[SalesOrderHeader].CustomerID, name, CountryRegion ;

    
    elif response == 3:
        cursor.execute("""SELECT City, CountryRegion, StateProvince, SUM(LineTotal - (OrderQty * UnitPrice * UnitPriceDiscount)), (OrderQty * UnitPrice * UnitPriceDiscount) ,
                ISNULL(CAST(Comment AS VARCHAR(30)), 
                    CASE 
                        WHEN GROUPING(City)=1 AND GROUPING(CountryRegion)=1 AND Grouping(StateProvince)=0
                            THEN 'Summary of  StateProvince' 
                        WHEN GROUPING(City)=1 AND Grouping(CountryRegion)=0
                            THEN 'Summary of CoutryRegion'
                        WHEN GROUPING(CountryRegion)=1 AND GROUPING(City)=1 AND Grouping(StateProvince)=1
                            THEN 'GrandTotal' 
                        END) AS Comment 
            FROM [SalesLT].[Customer] 
            JOIN [SalesLT].[SalesOrderHeader]
            ON [SalesLT].[Customer].CustomerID = [SalesLT].[SalesOrderHeader].CustomerID
            JOIN [SalesLT].[SalesOrderDetail]
            ON [SalesLT].[SalesOrderHeader].SalesOrderID = [SalesLT].[SalesOrderDetail].SalesOrderID
            JOIN [SalesLT].[Product] 
            ON [SalesLT].[SalesOrderDetail].ProductID = [SalesLT].[Product].ProductID
            JOIN [SalesLT].[Address]
            ON [SalesLT].[Address].AddressID = [SalesLT].[SalesOrderHeader].ShipToAddressID
            GROUP BY 
            Grouping SETS((City, StateProvince, CountryRegion, OrderQty, UnitPrice, UnitPriceDiscount, Comment), (City, CountryRegion, StateProvince, Comment), (CountryRegion, StateProvince, Comment), (CountryRegion, Comment), (Comment))""")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
            #SELECT  CountryRegion, StateProvince, City, SUM(LineTotal - (OrderQty * UnitPrice * UnitPriceDiscount)), (OrderQty * UnitPrice * UnitPriceDiscount) ,
            #    ISNULL(CAST(Comment AS VARCHAR(30)), 
            #        CASE 
            #            WHEN GROUPING(City)=1 AND GROUPING(CountryRegion)=1 AND Grouping(StateProvince)=0
            #                THEN 'Summary of  StateProvince' 
            #            WHEN GROUPING(City)=1 AND Grouping(CountryRegion)=0
            #                THEN 'Summary of CoutryRegion'
            #            WHEN GROUPING(CountryRegion)=1 AND GROUPING(City)=1 AND Grouping(StateProvince)=1
            #                THEN 'GrandTotal' 
            #            END) AS Comment 
            #FROM [SalesLT].[Customer] 
            #JOIN [SalesLT].[SalesOrderHeader]
            #ON [SalesLT].[Customer].CustomerID = [SalesLT].[SalesOrderHeader].CustomerID
            #JOIN [SalesLT].[SalesOrderDetail]
            #ON [SalesLT].[SalesOrderHeader].SalesOrderID = [SalesLT].[SalesOrderDetail].SalesOrderID
            #JOIN [SalesLT].[Product] 
            #ON [SalesLT].[SalesOrderDetail].ProductID = [SalesLT].[Product].ProductID
            #JOIN [SalesLT].[Address]
            #ON [SalesLT].[Address].AddressID = [SalesLT].[SalesOrderHeader].ShipToAddressID
            #GROUP BY 
            
    elif response == 4:
        cursor.execute("""Select HighCategory.Name as HighCategory, LowCategory.Name As LowCategory, [SalesLT].[Product].Name, SUM(ListPrice - UnitPriceDiscount) AS ITOG
            FROM [SalesLT].[SalesOrderDetail]
            JOIN [SalesLT].[Product]
            ON [SalesLT].[SalesOrderDetail].productID = [SalesLT].[Product].ProductID
        JOIN [SalesLT].[ProductCategory] as LowCategory
        ON [SalesLT].[Product].ProductCategoryID = LowCategory.ProductCategoryID
        JOIN [SalesLT].[ProductCategory] as HighCategory
        ON HighCategory.ProductCategoryID = LowCategory.ParentProductCategoryID
        GROUP BY GROUPING SETS((HighCategory.Name, LowCategory.Name, [SalesLT].[Product].Name, ListPrice), (HighCategory.Name))""")
  
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        
    elif response == 5: #два варианта
        cursor.execute("""SELECT Name, SalesPerson, FirstName, CountryRegion, StateProvince, City, SUM(LineTotal) AS 'Summary'
        FROM [SalesLT].[Product]
        JOIN [SalesLT].[SalesOrderDetail]
        ON [SalesLT].[Product].ProductID = [SalesLT].[SalesOrderDetail].ProductID
        JOIN [SalesLT].[SalesOrderHeader]
        ON [SalesLT].[SalesOrderDetail].SalesOrderID = [SalesLT].[SalesOrderHeader].SalesOrderID
        JOIN [SalesLT].[Customer] 
        ON [SalesLT].[SalesOrderHeader].CustomerID = [SalesLT].[Customer].CustomerID
        JOIN [SalesLT].[CustomerAddress]
        ON [SalesLT].[Customer].CustomerID = [SalesLT].[CustomerAddress].CustomerID
        JOIN [SalesLT].[Address]
        ON [SalesLT].[CustomerAddress].AddressID = [SalesLT].[Address].AddressID
        GROUP BY 
        CUBE (Name, SalesPerson, FirstName), ROLLUP ((CountryRegion, StateProvince, City), (CountryRegion, StateProvince), (CountryRegion));""")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    elif response == 6:
        cursor.execute("""SELECT [SalesLT].[Customer].SalesPerson, COUNT(customerID) AS Amount_Customers, RANK() OVER (order by COUNT(customerID) DESC) AS RANK
FROM [SalesLT].[Customer]
GROUP BY  [SalesLT].[Customer].SalesPerson;""")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    elif response == 7:
        cursor.execute("""SELECT [SalesLT].[Customer].SalesPerson, COUNT([SalesLT].[SalesOrderHeader].customerID) AS Number_of_Sales, DENSE_RANK() OVER (ORDER BY COUNT([SalesLT].[SalesOrderHeader].CustomerID) DESC) AS DENSE_RANK
FROM [SalesLT].[Customer]
Left Join [SalesLT].[SalesOrderHeader]
ON [SalesLT].[SalesOrderHeader].CustomerId = [SalesLT].[Customer].CustomerId
Group by [SalesLT].[Customer].SalesPerson""")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
#SELECT Distinct salesPerson, Count([SalesLT].[SalesOrderHeader].CustomerID), dense_rank() over ( Order By Count([SalesLT].[SalesOrderHeader].CustomerID) DESC)
#From [SalesLT].[Customer]
#Left Join [SalesLT].[SalesOrderHeader]
#ON [SalesLT].[SalesOrderHeader].CustomerId = [SalesLT].[Customer].CustomerId
#Group by salesPerson
    elif response == 8:
        cursor.execute("""SELECT [SalesLT].[Customer].SalesPerson, ISNULL(SUM(LineTotal - (OrderQty * UnitPrice * UnitPriceDiscount)), 0), RANK() OVER (ORDER BY COUNT([SalesLT].[SalesOrderHeader].customerID) DESC) AS RANK
From [SalesLT].[Customer]
LEFT JOIN [SalesLT].[SalesOrderHeader]
    ON [SalesLT].[Customer].CustomerID = [SalesLT].[SalesOrderHeader].CustomerID
    LEFT JOIN [SalesLT].[SalesOrderDetail]
    ON [SalesLT].[SalesOrderHeader].SalesOrderID = [SalesLT].[SalesOrderDetail].SalesOrderID
GROUP BY [SalesLT].[Customer].SalesPerson""")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    elif response == 9:
        cursor.execute("""SELECT CountryRegion, StateProvince, COUNT(FirstName) AS CNT, PERCENT_RANK() OVER (PARTITION BY CountryRegion ORDER BY COUNT(StateProvince) ASC) AS "Percent Rank"
FROM [SalesLT].[Customer] 
        JOIN [SalesLT].[CustomerAddress]
        ON [SalesLT].[Customer].CustomerID = [SalesLT].[CustomerAddress].CustomerID
        JOIN [SalesLT].[Address]
        ON [SalesLT].[CustomerAddress].AddressID = [SalesLT].[Address].AddressID
        WHERE AddressType = 'Main Office'
        GROUP BY CountryRegion, StateProvince""")
        
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    elif response == 10:
        cursor.execute("""SELECT CountryRegion, StateProvince, COUNT(FirstName) AS CNT, DENSE_RANK() OVER (PARTITION BY CountryRegion ORDER BY COUNT(FirstName) DESC) AS DENSE_RANK
        FROM [SalesLT].[Customer] 
        LEFT JOIN [SalesLT].[CustomerAddress]
        ON [SalesLT].[Customer].CustomerID = [SalesLT].[CustomerAddress].CustomerID
        LEFT JOIN [SalesLT].[Address]
        ON [SalesLT].[CustomerAddress].AddressID = [SalesLT].[Address].AddressID
        AND AddressType = 'Main Office'
        GROUP BY CountryRegion, StateProvince""")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    elif response == 11:
        cursor.execute("""SELECT CountryRegion, StateProvince, City, COUNT(CustomerID) AS CNT,
LAG(COUNT(CustomerID),1) OVER (partition by CountryRegion ORDER BY COUNT(CustomerID) DESC) - COUNT(CustomerID) AS dif,
RANK() over (partition by CountryRegion order by COUNT(CustomerID) desc) AS rank
FROM [SalesLT].[Address]
JOIN [SalesLT].[CustomerAddress]
ON [SalesLT].[Address].AddressID = [SalesLT].[CustomerAddress].AddressID
WHERE AddressType = 'Main Office'
GROUP BY CountryRegion, StateProvince, City""")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
connection.close()

#SELECT FirstName,
#                ISNULL(cast(Name AS VARCHAR(30)),
#                    CASE WHEN GROUPING(Name) = 1 AND GROUPING(FirstName) = 1 AND GROUPING(ShipMethod) = 1 AND GROUPING(CountryRegion) = 1 AND GROUPING(AddressLine1) = 1
#                        THEN 'GrandTotal' end)
#                    AS Name, ShipMethod, CountryRegion, AddressLine1,
#                    SUM(ListPrice - UnitPriceDiscount) AS itogFROM [SalesLT].[Product]
#                JOIN [SalesLT].[SalesOrderDetail]
#                ON [SalesLT].[Product].ProductID = [SalesLT].[SalesOrderDetail].ProductID
#                JOIN [SalesLT].[SalesOrderHeader]
#                ON [SalesLT].[SalesOrderDetail].SalesOrderID = [SalesLT].[SalesOrderHeader].SalesOrderID
#                JOIN [SalesLT].[Customer] 
#                ON [SalesLT].[SalesOrderHeader].CustomerID = [SalesLT].[Customer].CustomerID
#                JOIN [SalesLT].[CustomerAddress]
#                ON [SalesLT].[Customer].CustomerID = [SalesLT].[CustomerAddress].CustomerID
#                JOIN [SalesLT].[Address]
#                ON [SalesLT].[CustomerAddress].AddressID = [SalesLT].[Address].AddressID
#            GROUP BY
#            ROLLUP ((FirstName, Name, ShipMethod, CountryRegion, AddressLine1));