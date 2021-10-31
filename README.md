# publicinterest
- "Taste, however, is a field of cultural inquuiry that is much more amenable to quantiative analysis and has veen recently traversed by cultural sociologists." -- K.Leview et al. 2008 
- OLS regression coefficients 
- Lewis, Kevin, et al. “Tastes, Ties, and Time: A New Social Network Dataset Using Facebook.Com.” Social Networks, vol. 30, no. 4, Oct. 2008, pp. 330–42. ScienceDirect ONLINE https://doi.org/10.1016/j.socnet.2008.07.002

- One could imagine looking at the timing of buy and sell (of the same
asset) for him, or several.
- Need to look at what other people have done. 
- Need to research types of graphs particularly for the csv_breakdowns and what should be in the graphs. 
    - See what people have made (NYT and WSJ).
    - Distribution over time of transactions?
    - Distribution plot? NCTK.
    - Pick 5-10 of the most active trades. 
    - For each ticker, market cap and Volatility. 
    - Scatter plot matrix. 
- Looking at people specifically. 
- Correlation between high runners and those who did not provide data. 
- pip install  (later)
- https://bigcharts.marketwatch.com/
- Bhatt's recs
    - https://link.springer.com/article/10.1007%2Fs12197-017-9384-z
    - https://www.opensecrets.org/ 
    - https://www.opensecrets.org/personal-finances/
    - https://therevolvingdoorproject.org/


- 

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
            - Canes-Wrone  
            - Mian 
            - Shafir 
        - Finance
            - Matray (N)
            - Cox 
            - Blinder 
# Notes
    - How many people are we talking about, how often do they do things, how big are the transactions, where do they take place, etc.  
    - Need to walk through wiki.txt. Am I skipping anything important? (publicinterest/src/py/wiki.txt)
    - Bug with 'RDSA' ticker. 
        -https://efdsearch.senate.gov/search/view/ptr/045f76aa-7ae2-4040-a603-67b5ebc3b271/
    - Need to talk about frequency_of_shares.csv. 
    - Skipping: transaction['disclosure_date'], transaction['ptr_link'], transaction['asset_description'], transaction['comment']
```

@HERE
```diff
@@ Week 10 [Monday, November 1] @@
- Deadlines: 
    - Frequency of shares (sort of it, exponential scale, sort by high runners?, non-linear graphing)
    - Need to deal with stock options better. 
    - Need to research regarding notice dates. How early?
    - Dividend reinvestment @ at end of the quarter. 
    - Email people back.
        - Update list from last week. 
        - Meet with Blinder (around Thanksgiving b/c of OH) with results. 
    - Need to find out who is in congress and who is not (basically difference between those reporting and those not reporting) (are there official records?)
    - Group tickers by type (tech, oil, medicine, etc.).
    - Need to be able to search https://www.congress.gov/congressional-record/2020/04/14
    - Need to add birthday to Rep.py 
    - Need to control for number of years in congress. 
    - Need to deal with Nans better. 
    - Maybe explore matplotlib or seaborn, along with Pandas.
+ Done:
    - Moved over to Jupyter notebook.
    - Compared transaction date to tax deadlines. 
# Notes
```

```diff
@@ Week 11 [Monday, November 8] @@
- Deadlines: 
+ Done:
# Notes
```

```diff
@@ Week 12 [Monday, November 15] @@
- Deadlines: 
    - Can we get more data? 
+ Done:
# Notes
```

```diff
@@ Week 13 [Monday, November 22] @@
- Deadlines: 
+ Done:
# Notes
```

```diff
@@ Week 14 [Monday, November 29] @@
- Deadlines: 
    - Attend "How to Write an IW Paper"
+ Done:
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
    -  Analyze their buying trends 
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

