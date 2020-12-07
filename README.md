# Supermarket Scraping Project
This project helps people to shop for certain product faster, because it scapes products from supermarkets, puts them in a database and then displays it through a flask web app.
From every product being scraped, it stores the supermarket from where it came from, name, prices and discounts, image, link and quantity.
It uses Selenium and BeautifulSoup libraries for the scraping part, which makes the process really slow, but it can load all the javascript within webpages, which is necessary, otherwise we couldn't get the data.
There is some specific properties for every supermarket website, because they all have different HTML, CSS and Javascript usage. Therefore one program was made for each.
In the end of every scrape, it loads the info to a database with sqlite3. For the python environment and therefore all the scraping side of the project, Spider from Anaconda is being used.
When the database is fully loaded with the info, it's loaded to the CS50 IDE. For a better User Experience, the data is being displayed in different categories, otherwise there will be too many products in one page.
The data is just being displayed in the form of bootstrap cards, with the number of the supermarket for each product. They are all ordered by price, or savings in the offer parts of the website.
This gives the user the ability to see side by side the products each supermarket offers, which leads them to know which prices are lower in a minimum amount of time.
Every page is being showed with a pagination macro, which gives the user a better experience by having just 21 products per page.
Through a navbar fixed on top of the page, the user can navigate through the website and also search for some query.
Note that this project was just used to check the prices and data from alcohols in 2 supermarkets. It can be easily escalade to show all the products each supermarket has.
On the home page it has the best offers available and you can go to each category or search for a query from each one of the pages.
All the website was built with flask and jinja, for a faster and better design of the code.
Through all these features, the user can compare the prices from supermarkets easily, through the COMPARA2(name) web app in a short amount of time, check for each category and check for different offers.
Which leads to a better experience when buying something that the user wants to get the best price for.
