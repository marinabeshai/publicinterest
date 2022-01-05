# publicinterest
- looking into the outliers 
- research the tax thing. 
- who is trading in cryptocurrency?
- fund error :) w/ticker to industry mappying 
- frequency of difference --> list top 3 people. 

    # <!-- state and industry? -->

    
- i have to test all the code. especially utils!!!
    2. add assertions
    3. run then
    4.comments
    
- most popular td fe official 
    - break down into purchase and sell
        - are they selling to pay for taxes?
            - are they buying a house?
                - integrated value 

- tax returns public? 

- sales and purchases next up. 
- most_popular_td_fe_sector --> purchase only. 

- timing of purchases.  

ml - prediction or classification [?] --> labeled data? 

- estimate size [confidence interval]

= DEBUG SECTOR AND INDUSTRY@!!!!!!

- traded on industries where they sit on committee!!!!
- dates and size of amount!!!!
    - geomtric mean; sort it; find which days are the most monetarily popular 

- One could imagine looking at the timing of buy and sell (of the same
asset) for him, or several.
- Need to look at what other people have done. 
- Looking at people specifically. 
- Correlation between high runners and those who did not provide data. 
- pip install  (later)


- futures on the commodities market (?)
- mutual funds -- benign (????)
- buy and hold vs. buy and sell ?
- group by age, and find an investment strategy (buy-and-hold vs. buy-and-sell)
- look for consistency of sotcks per year (like appl, msft)

- need to figure out "pdf disclosed filling" in frequency_of_asset_type 
- average return 
- track buys and sells per person using geometric mean of "amount"
- systematic similarities and differences between house and senate
- who was trading the no longer existing stocks? 



- box and whisker (?) plot 
- elements of graphing data. 
- https://bigcharts.marketwatch.com/
- https://www.mckinsey.com/business-functions/strategy-and-corporate-finance/our-insights/the-impact-of-covid-19-on-capital-markets-one-year-in

```diff
@@ Week 1 [Monday, August 30] @@
- Deadlines: 
+ Done:
    - Meeting w/PEMM Group (9/2)
    - Independent Work Getting Started Meeting (9/2-3)
    - Meeting w/Brian (9/3)
# Notes
```


```diff
@@ Week 2 [Monday, September 6] @@
- Deadlines: 
+ Done:
    - Meeting w/Jack (9/6)
    - Meeting w/AnneMarie (9/8)
    - Emailed:
        - Matt D.
        - Eric G. 
# Notes
```

```diff
@@ Week 3 [Monday, September 13] @@
- Deadlines: 
+ Done:
    - Emailed:
        - Arvind
# Notes
```

```diff
@@ Week 4 [Monday, September 20] @@
- Deadlines: 
    - Submit a Written Project Proposal by 11:59pm EDT, in the IW portal.
+ Done:
    - Got an Idea
# Notes
```


```diff
@@ Week 5 [Monday, September 27] @@
- Deadlines: 
+ Done:
    - Automatic download of data.
# Notes
```

```diff
@@ Week 6 [Monday, October 4] @@
- Deadlines: 
+ Done:
    - Emailed: 
        - Tim of House and Senate StockWatcher.com
        - info.clerkweb@
    - Tried to read and scrap PDFs using Python to get the gap between the ones that are decent but not on Tim's site. 
# Notes
    - Congressional data is on the GitHub Bulk data repository https://github.com/usgpo which is made available by GPO.
```

```diff
@@ Week 7 [Monday, October 11] @@
- Deadlines: 
    - Submit the Checkpoint Form by 11:59pm EDT, in the IW portal
+ Done:
# Notes
```

```diff
@@ Week 8 [Monday, October 18] @@
- Deadlines: 
+ Done:
# Notes
```

```diff
@@ Week 9 [Monday, October 25] @@
- Deadlines: 
+ Done:
    - Finished basic parsing, csving, and graphing of senate data (dates.py, costs.py, person.py, ticker.py, parse.py, utils.py)
    - Wikipedia scraping work. 
    - Emailed:
        - SPIA
            - Bénabou 
            - Canes-Wrone (Next Semester)
            - Mian 
            - Shafir 
        - Finance
            - Matray (N)
            - Cox 
            - Blinder (Meeting)
        - Econ
            - de Swaan
# Notes
    - How many people are we talking about, how often do they do things, how big are the transactions, where do they take place, etc.  
    - Need to walk through wiki.txt. Am I skipping anything important? (publicinterest/src/py/wiki.txt)
    - Bug with 'RDSA' ticker. 
        -https://efdsearch.senate.gov/search/view/ptr/045f76aa-7ae2-4040-a603-67b5ebc3b271/
    - Need to talk about frequency_of_shares.csv. 
    - Skipping: transaction['disclosure_date'], transaction['ptr_link'], transaction['asset_description'], transaction['comment']
```

```diff
@@ Week 10 [Monday, November 1] @@
- Deadlines: 
    - Need to research types of graphs particularly for the csv_breakdowns and what should be in the graphs. 
        - See what people have made (NYT and WSJ).
        - Distribution over time of transactions?
        - Distribution plot? NCTK.
        - Pick 5-10 of the most active trades. 
        - For each ticker, market cap and Volatility. 
        - Scatter plot matrix. 
    - Need to deal with stock options better. 
    - Need to research regarding notice dates. How early?
    - Dividend reinvestment @ at end of the quarter. 
    - Email people back.
        - Update list from last week. 
    - Need to find out who is in congress and who is not (basically difference between those reporting and those not reporting) (are there official records?)
    - Need to be able to search https://www.congress.gov/congressional-record/2020/04/14
    - Maybe explore matplotlib or seaborn, along with Pandas.
+ Done:
    - Sort data (made sort_keys, methods in utils.py, etc.). 
    - Need to deal with Nans better. 
    - Need to control for number of years in congress. 
    - Moved over to Jupyter notebook.
    - Compared transaction date to tax deadlines. 
    - Need to add birthday to Rep.py (now Official in wiki.py)
# Notes
```

```diff
@@ Week 11 [Monday, November 8] @@
- Deadlines: 
    - Frequency of industry by year. 
    - Add a mapping between ticker and industry.
+ Done:
    - Group tickers by type (tech, oil, medicine, etc.).
    - Need to clean all code. 
    - Breakdown of tax date code. 
    - Can get congress. 
# Notes
    - Lukas recommended that I reach out to de Swaan in the Econ department (emailed). 
    - If I can get congress ---> that means i can figure out who is and who is not there. https://en.wikipedia.org/wiki/List_of_United_States_senators_in_the_105th_Congress
```

```diff
@@ Week 12 [Monday, November 15] @@
- Deadlines: 
    - Can we get more data? 
        - There is a pdf to text parser in my email from Brian (subject line is "pdftotext"
    - Have to write method that translate date to a congress number so we can see who is trading and who is not.
+ Done:
    - Types of transactions per person. 
    - Fixed bug with go_shopping() (in wiki.py).
    - Fixed/finished get_congress() (in wiki.py).
    - Fixed education in Official so as to collect all of them. 
# Notes
    - Need to figure out what I should do with "ticker_to_industry_mapping_ERRORS"
    - Need more clean up of education. Some corner cases exist. It is possible to do a degree_count like BS, MBA, JD,...
```

```diff
@@ Week 13 [Monday, November 22] @@
- Deadlines: 
    - Need to figure out what I'm doing with errors. 
    -  type of degree per official. 
+ Done:
    - Number of degrees.
    - Get sector data.
    - Canonical names. 
# Notes
```

```diff
@@ Week 14 [Monday, November 29] @@
- Deadlines: 
    - Meet with Blinder (around Thanksgiving b/c of OH) with results. 
+ Done:
    - Average size of amount per person. 
# Notes
```

```diff
@@ Week 15 [Monday, December 6] @@
- Deadlines: 
    - Submit Progress Report for Thesis/Two-Term Projects by 11:59pm EST, in the IW portal
+ Done:
# Notes
```

```diff
@@ Week 16 [Monday, December 13] @@
- Deadlines: 
    - Make an outline for Chapter 2.
    - Make an outline for Chapter 3.
+ Done:
# Notes
```

```diff
@@ Week 17 [Monday, December 20] @@
- Deadlines: 
    - Make an outline for Chapter 1.
    - Chapter 2 (Background) Due.
    - Submit Chapter 2 for Review.
    - Chapter 3 (Related Work) Due
    - Submit Chapter 3 for Review.
+ Done:
# Notes
```

```diff
@@ Week 18 [Monday, December 27] @@
- Deadlines: 
    - Make an outline for Chapter 4.
    - Chapter 1 (Introduction) Due.
    - Submit Chapter 1 for Review.
+ Done:
# Notes
```

```diff
@@ Week 19 [Monday, January 3] @@
- Deadlines: 
    - Make an outline for Chapter 5. 
    - Chapter 4 (Approach) Due.
    - Submit Chapter 4 for Review.
+ Done:
# Notes
    Meeting Notes [1/3]:
        - Fraction of the whole of the ticker symbols. [How could we make this better?]
```

```diff
@@ Week 20 [Monday, January 10] @@
- Deadlines: 
    - Chapter 5 (Methodology) Due.
    - Submit Chapter 5 for Review.
+ Done:
# Notes
```

```diff
@@ Week 21 [Monday, January 17] @@
- Deadlines: 
    - Need all the data in a table.
        - Multiple tables seems most likely.  For now, maybe just think of clean flat files, with an eye to an SQL or other formal database in the (near?) future.
	- Need to figure out how to store the table
        - Knowing what it is, how big, etc., will help answer this.
    - Need to figure out how to make API accessible. 
	    - I think API design and making it available come later on, though you should keep them in mind as you go along.  But you can's make an API if you don't know what you have and if you haven't thought about what kinds of use you and others might make of it.

+ Done:
# Notes
```

```diff
@@ Week 22 [Monday, January 24] @@
- Deadlines: 
+ Done:
# Notes
```	
	
```diff
@@ Week 23 [Monday, January 31] @@
- Deadlines: 
    - Analyze their buying trends 
    - Reach out to Professor who returned from sabbatical (Canes-Wrone). 
+ Done:
# Notes
```
    
```diff
@@ Week 24 [Monday, February 7] @@
- Deadlines: 
+ Done:
# Notes
```
	
```diff
@@ Week 25 [Monday, February 14] @@
- Deadlines: 
	- Compare their trends with market performance Here's another place where you have to figure out what data you want and how to get it easily.  Stock prices from the NYSE, etc., are easy; not so clear about pork belly futures, though probably they too are around somewhere.
+ Done:
# Notes
```

```diff
@@ Week 26 [Monday, February 21] @@
- Deadlines: 
    - Need a thesis second reader. 
    - Submit a Draft Paper by 11:59pm EST, in the IW portal
+ Done:
# Notes
```

```diff
@@ Week 27 [Monday, February 28] @@
- Deadlines: 
    - Last grab of data (cut off at EOY'22).
    - Make an outline for Chapter 6
    - Make an outline for Chapter 7.
    - Write an algorithm that takes their data into consideration and buys with latency and calculates return in investment.
+ Done:
# Notes
```

```diff
@@ Week 28 [Monday, March 7] @@
- Deadlines: 
    - Make an outline for Chapter 8.
    - Chapter 6 (Results) Due
    - Chapter 7 (Evaluation) Due.
    - Submit Chapter 6&7 for Review.
+ Done:
# Notes
```

```diff
@@ Week 29 [Monday, March 14] @@
- Deadlines: 
    - Make an outline for Chapter 9.
    - Chapter 8 (Discussion) Due
    - Submit Chapter 8 for Review.
    - Evaluation algorithm.
+ Done:
# Notes
```

```diff
@@ Week 30 [Monday, March 21] @@
- Deadlines: 
    - Chapter 9 (Conclusion) Due.
    - Submit Chapter 9 for Review.
    - WANT FULL DRAFT BY THIS DATE.
    - Select a second reader by 11:59pm EST, in the IW portal (required for thesis, only)
+ Done:
# Notes
```

```diff
@@ Week 31 [Monday, March 28] @@
- Deadlines: 
+ Done:
# Notes
```

```diff
@@ Week 32 [Monday, April 4] @@
- Deadlines: 
+ Done:
# Notes
```

```diff
@@ Week 33 [Monday, April 11] @@
- Deadlines: 
    - Submit a Written Final Report by 11:59pm EST, in the IW portal
+ Done:
# Notes
```

```diff
@@ Week 34 [Monday, April 18] @@
- Deadlines: 
    - Submit Slides for Oral Presentation by 11:59pm in IW portal
    - Oral presentation week
+ Done:
# Notes
```

