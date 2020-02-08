# Web_Scraping_HDB
Scrape HDB apartments for sales at iProperty website.

I am looking for an apartment and find that it is chore to browse through list of flats offered
by property agent. Nothing wrong with the details just that I prefer to compare all the available
flats meeting my criteria in a worksheet format.

Data analytics is not new to me but I find it particular interesting to scrap data from websites.
So I thought why not use this opportunity to practice my Python skills as well as doing analytics
on my search for a suitable apartmen.

First step is to look for available apartments for sales. I decided to look it up at iProperty
website as it allows me to put in my search criteria. This helps to narrow down data set.

I tried using Beautiful soup to parse the data initially but, I find it difficult to get to certain
data elements perhaps due to how iProperty structured their webpage. So I decided to use xpath 
which allows me to zoom in and extract each data element easily.

After extracted the data, I added the data to a list 'hdblist' temporary which was pumped into 
a dataframe 'resalehdb' which helps to make data manipulations such as column naming, sorting, etc
easier.

Finally, I export the results to a csv format file to view in Excel.

Although I have yet to find my new home but I have confidence that with the help of Python
web scraping capability, finding my new home is only a few clicks and few lines of codes away :)
