from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data_db = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_data_db=mars_data_db)

# Route that will call the scrape function (get Mars data) 
@app.route("/scrape")  
def scrape():
    
    # Run the scrape function
    scrape_one = scrape_mars.scrape1()
    scrape_two = scrape_mars.scrape2()
    scrape_three = scrape_mars.scrape3() 
    scrape_four = scrape_mars.scrape4()
    
    mars_data_db = {
        "title" : scrape_one[0],
        "paragraph" : scrape_one[1],
        "featured_photo" : scrape_two,
        "Mars_facts_table" : scrape_three,
        "Mars_Hemispheres" : scrape_four
        }

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data_db, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)