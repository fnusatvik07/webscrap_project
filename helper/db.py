from tinydb import TinyDB 

db=TinyDB("data.json")

#1 Create Tables 

products=db.table("products")
users=db.table("users")

#2. Insert Data 

# products.insert(
#     {
#         "id":"B001",
#         "name":"iphone",
#         "price": 9.99
#     }
# )

# products.insert_multiple(
#    [
#     {"id":"B003","name":"USB Cable","price":10},
#     {"id":"B004","name":"Power Bank","price":20},
#     {"id":"B005","name":"Player","price":30}

#    ]
# )

# users.insert(
#     {
#         "name":"John",
#         "age": 32
#     }
# )

#3. Read Data

# print(products.all())

#4. Reading by Query 

from tinydb import Query 

Product=Query() 

# a=products.get(Product.id=="B003")
# print(a)

# 5. Search

# a=products.search(Product.price>15)
# print(a)

#6. Update Data 

# products.update(
#     {"price":50},
#     Product.id=="B003"
# )

#7. Deleting a Data 

products.remove(Product.id=="B003")