from itertools import product
import re
from flask import Flask,render_template , request , url_for ,redirect
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from flask_migrate import Migrate, migrate

import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
import models


@app.route('/')
#home Page 
def index():
    return render_template('home.html')

@app.route('/Product')
#Product List Page
def Product():
    entries=models.Product.query.all()
    return render_template('Product.html'  , entries=entries)

@app.route('/AddProduct')
#add ProductPage
def AddProduct():
    return render_template('AddProduct.html')

@app.route('/submitAddProduct' ,methods=['POSt','GET'])
#Submit Product
def submitAddProduct():
    u = models.Product(name=request.form["name"])
    db.session.add(u)
    if(db.session.commit):
        db.session.commit()
        return  redirect(url_for('Product'))
    else :
        return 'Error'

@app.route('/editProduct/<int:id>', methods=['POSt','GET'])
#edit Product Page 
def editProduct(id):
    try:
        sqliteConnection = sqlite3.connect('app.db')
        cursor = sqliteConnection.cursor()
        sql_delete_query = """SELECT name from Product where id = ?"""
        cursor.execute(sql_delete_query ,(id,))
        records = cursor.fetchall()
        cursor.close()
        for row in records:
            name=row[0]
        return render_template('editProduct.html',name=name , id=id)

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
    return redirect(url_for('Product'))

@app.route('/submitUpdateProduct',methods=['POST','GET'])
#submit Edit Product
def submitUpdateProduct():
    name = request.form["name"]
    id = request.form["id"]
    try:
        sqliteConnection = sqlite3.connect('app.db')
        cursor = sqliteConnection.cursor()
        sql_delete_query = """Update Product set name = ? where id = ?"""
        data = (name, id)
        cursor.execute(sql_delete_query ,data)
        sqliteConnection.commit()
        

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
    return redirect(url_for('Product'))

@app.route('/viewProduct/<int:id>' ,methods=['POSt','GET'])
#View Product
def viewProduct(id):
    try:
        sqliteConnection = sqlite3.connect('app.db')
        cursor = sqliteConnection.cursor()
        sql_delete_query = """SELECT name from Product where id = ?"""
        cursor.execute(sql_delete_query ,(id,))
        records = cursor.fetchall()
        cursor.close()
        for row in records:
            name=row[0]
        cursor.close()
        return render_template('viewProduct.html',name=name)

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
    return redirect(url_for('Product'))

     
@app.route('/Location')
#Location Page 
def Location():
    entries=models.Location.query.all()
    return render_template('Location.html' ,entries=entries)

@app.route('/AddLocation',methods=['POST','GET'])
#add Location Page 
def AddLocation():
    return render_template('addLocation.html')


@app.route('/submitLocation' ,methods=['POSt','GET'])
#submit Location
def submitLocation():
    u = models.Location(name=request.form["name"])
    db.session.add(u)
    if(db.session.commit):
        db.session.commit()
        return redirect(url_for("Location"))
    else:
        return render_template('error.html',title="Error")

@app.route('/editLocation/<int:id>', methods=['POSt','GET'])
#edit Location Page 
def editLocation(id):
    try:
        sqliteConnection = sqlite3.connect('app.db')
        cursor = sqliteConnection.cursor()
        sql_delete_query = """SELECT name from Location where id = ?"""
        cursor.execute(sql_delete_query ,(id,))
        records = cursor.fetchall()
        cursor.close()
        for row in records:
            name=row[0]
        return render_template('editLocation.html',name=name , id=id)

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
    return redirect(url_for('Product'))

@app.route('/submitUpdateLocation',methods=['POST','GET'])
#submit Edit Location
def submitUpdateLocation():
    name = request.form["name"]
    id = request.form["id"]
    try:
        sqliteConnection = sqlite3.connect('app.db')
        cursor = sqliteConnection.cursor()
        sql_delete_query = """Update Location set name = ? where id = ?"""
        data = (name, id)
        cursor.execute(sql_delete_query ,data)
        sqliteConnection.commit()
        

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
    return redirect(url_for('Location'))

@app.route('/viewLocation/<int:id>' ,methods=['POSt','GET'])
#View Location
def viewLocation(id):
    try:
        sqliteConnection = sqlite3.connect('app.db')
        cursor = sqliteConnection.cursor()
        sql_delete_query = """SELECT name from Location where id = ?"""
        cursor.execute(sql_delete_query ,(id,))
        records = cursor.fetchall()
        cursor.close()
        for row in records:
            name=row[0]
        cursor.close()
        return render_template('viewLocation.html',name=name)

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
    return redirect(url_for('Location'))

@app.route('/ProductMovement')
#Product Movement Page
def ProductMovement():
    entries=models.ProductMovement.query.all()
    return render_template('ProductMovement.html',entries=entries)

@app.route('/AddMovement')
#Add Movement 
def AddMovement():
    location=models.Location.query.all()
    product=models.Product.query.all()
    return render_template('AddMovement.html',location=location , product = product)

@app.route('/submitMovement' , methods=['POST','GET'])
#submit Movement
def submitMovement():
    fromLocation = request.form["fromLocation"]
    toLocation=request.form['toLocation']
    quantity = request.form['quantity']
    productId = request.form['product']
    if(productId == "0"):
        return render_template("error.html",title="You can't send Undefined Product")
    if(fromLocation == '0' and toLocation =='0'):
        return render_template("error.html" , title="The place of exit or entry of the goods must be specified")
    if(quantity == ''):
        return render_template("error.html",title="You can't send empty Quantity of Product")
    if(quantity == 0):
        return render_template("error.html",title="You can't send Zero Quantity of Product")
    u = models.ProductMovement(fromLocation=fromLocation,toLocation=toLocation,productId=productId,quantity=quantity)
    db.session.add(u)
    if(db.session.commit):
        db.session.commit()
        return redirect(url_for("ProductMovement"))
    else:
        return  render_template('error.html',title="Error")

#product_movement
@app.route('/editProductMovement/<int:id>', methods=['POSt','GET'])
#edit Product Movement Page 
def editProductMovement(id):
    try:
        sqliteConnection = sqlite3.connect('app.db')
        cursor = sqliteConnection.cursor()
        sql_delete_query = """SELECT * from product_movement where id = ?"""
        cursor.execute(sql_delete_query ,(id,))
        records = cursor.fetchall()
        cursor.close()
        for row in records:
            fromLocation=row[1]
            toLocation=row[2]
            Product=row[3]
            quantity=row[4]
        all_Location=models.Location.query.all()
        all_Product=models.Product.query.all()
        return render_template('editMovement.html',fromLocation=fromLocation,toLocation=toLocation,Product=Product,quantity=quantity,all_Location=all_Location,all_Product=all_Product, id=id)

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
    return redirect(url_for('ProductMovement'))
@app.route('/submitEditMovement',methods=['POST','GET'])
#submit Edit Product Movement
def submitEditMovement():
    fromLocation = request.form["fromLocation"]
    toLocation=request.form['toLocation']
    quantity = request.form['quantity']
    id = request.form["id"]
    Product = request.form['product']
    if(Product == "0"):
        return render_template("error.html",title="You can't send Undefined Product")
    if(fromLocation == '0' and toLocation =='0'):
        return render_template("error.html" , title="The place of exit or entry of the goods must be specified")
    if(quantity == ''):
        return render_template("error.html",title="You can't send empty Quantity of Product")
    if(quantity == 0):
        return render_template("error.html",title="You can't send Zero Quantity of Product")
    try:
        sqliteConnection = sqlite3.connect('app.db')
        cursor = sqliteConnection.cursor()
        sql_delete_query = """Update product_movement set fromLocation = ? , toLocation = ? ,productId = ? , quantity = ? where id = ?"""
        data = (fromLocation , toLocation , Product ,quantity, id)
        cursor.execute(sql_delete_query ,data)
        sqliteConnection.commit()
        

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
    return redirect(url_for('ProductMovement'))

@app.route('/viewProductMovement/<int:id>' ,methods=['POSt','GET'])
#View Producct Movement
def viewProductMovement(id):
    try:
        sqliteConnection = sqlite3.connect('app.db')
        cursor = sqliteConnection.cursor()
        sql_delete_query = """SELECT * from product_movement where id = ?"""
        cursor.execute(sql_delete_query ,(id,))
        records = cursor.fetchall()
        cursor.close()
        for row in records:
            fromLocation=row[1]
            toLocation=row[2]
            Product=row[3]
            quantity=row[4]
        all_Location=models.Location.query.all()
        all_Product=models.Product.query.all()
        return render_template('viewProductMovement.html',fromLocation=fromLocation,toLocation=toLocation,Product=Product,quantity=quantity,all_Location=all_Location,all_Product=all_Product)

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
    return redirect(url_for('ProductMovement'))

@app.route('/ProductBalance')
def ProductBalance():
    all_Location=models.Location.query.all()
    all_Product=models.Product.query.all()
    all_Movement = models.ProductMovement.query.all()
    arr = []
    sum =0
    for product in all_Product:
        for store in all_Location:
            sum =0
            for movement in all_Movement:
                if ((movement.fromLocation == store.id) and (movement.productId == product.id)):
                    sum = sum - movement.quantity
                elif ((movement.toLocation == store.id) and (movement.productId == product.id)):
                    sum = sum + movement.quantity
            arr.append(sum)
            
    new_data = []
    r_data = []
    lnth = 0
    for i in range(len(arr)):
        if i % len(all_Product) == 0 and i != 0:
            new_data.append(r_data)
            r_data = [arr[i]]
            lnth += 1
        else:
            r_data.append(arr[i])
    new_data.append(r_data)
    lnth += 1

    return render_template('ProductBalance.html' , Lenght = lnth, data=new_data ,all_Location = all_Location , all_Product=all_Product)

@app.route('/deleteAllMovement')
def deleteAllMovement():
    try:
        sqliteConnection = sqlite3.connect('app.db')
        cursor = sqliteConnection.cursor()
        sql_delete_query = """DELETE from product_movement where id=4"""
        cursor.execute(sql_delete_query)
        sqliteConnection.commit()
        cursor.close()

        return redirect(url_for('ProductMovement'))


    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
    return redirect(url_for('ProductMovement'))

if __name__ =='__main__': 
    app.run(debug=True)


