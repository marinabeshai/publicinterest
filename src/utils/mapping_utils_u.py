def search_mapping(df, ticker):
    try: 
        return list(df.loc[df['ticker'] == ticker]['industry'])[0]
    except:
        return None
