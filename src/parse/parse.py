import pandas as pd
import csv 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import plotly.express as px

# def graph(filename):
    
#     x = [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in date.keys()]

#     plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
#     plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=12))
#     fig, ax = plt.subplots()
#     ax.plot(x, date.values())
#     plt.gcf().autofmt_xdate()
#     plt.savefig('myfig')



if __name__ == '__main__':
    with open('../download/senate-09252021.csv') as senate_data:
        with open('./senate_skipped.txt', 'a') as errors:
            with open('./senate-09252021-output.csv', 'a') as output:

                date = {}
                
                csvreader = pd.read_csv(senate_data)

                for i in csvreader.amount:
                    # i = "{}-{}-{}".format( i[6:10], i[0:2], i[3:5])
                    if i in date:
                        date[i] = date[i] + 1;
                    else:
                        date[i] = 1 
                        
                writer = csv.writer(output)
                writer.writerow(['amount', 'amount_count'])
                for i in date:
                    writer.writerow([i, date[i]])
                    
            df = pd.read_csv('./senate-09252021-output.csv')
            # df1 = df.sort_values("date").reset_index(drop=True)
            # df.sort_values(by="date", key=pd.to_datetime)
            # df['date'] =pd.to_datetime(df.date)

            fig = px.line(df, x='amount', y = 'amount_count', title='date and time count for senate')
            
            fig.update_layout(autotypenumbers='convert types')
            fig.write_html("amount_Act.html")

                # fig.show()
