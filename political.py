class Political:
  def internationalTradePartners(self,Country,Tradeflow):
    import pandas as pd
    df=pd.read_excel('https://asiliventures.com/wp-content/uploads/2023/07/InternationalTradeVolumes_withPartners.xlsx')
    Country=str(Country)
    Tradeflow=str(Tradeflow)
    tradePartners=[]
    years=[]
    for index, row in df.iterrows():
      if (row['Reporter country'] == Country) and (row['Flow'] == Tradeflow):
            tradePartners.append(df.at[index,'Partner country'])
      
