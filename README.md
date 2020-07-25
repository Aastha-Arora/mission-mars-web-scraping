## Web Scraping Homework - Mission to Mars

### Objective

Build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

### Step 1 - Scraping
Web scraping using BeautifulSoup, Pandas, and Requests/Splinter.

Python script `scrape_mars.py` constains the code to scrape the code from the following websites 
and returns one Python dictionary containing all of the scraped data.

[NASA Mars News](https://mars.nasa.gov/news/)
Extract the latest News Title and Paragraph Text

[JPL Mars Space Images](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)
Extract the image url for the current Featured Mars Image

[Mars Weather Twitter Account](https://twitter.com/marswxreport?lang=en)
Scrape the latest Mars weather tweet from the page

[Mars Facts](https://space-facts.com/mars/)
Scrape the table containing facts about the planet including Diameter, Mass, etc.

[Mars Hemispheres](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)
Extract the high resolution images for each of Mar's hemispheres


### Step 2 - MongoDB and Flask Application
MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped.
PyMongo is used for CRUD applications for the database. 

**Flask App `app.py`**

Routes
* root route `/`: This route will query the MongoDB and pass the mars data into an HTML template to display the data.
* `/scrape`: This route imports the `scrape_mars.py` script and calls the function to scrape data. Scaped data is saved in MongoDB

**Template HTML file `index.html`**

This file takes the mars data dictionary and displays all of the data in the appropriate HTML elements.


![](https://github.com/Aastha-Arora/web-scraping-challenge/blob/master/Missions_to_Mars/Screenshots/Screenshot%201.png)
