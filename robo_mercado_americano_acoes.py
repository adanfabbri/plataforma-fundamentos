import time
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import datetime as dt
from scipy.signal import argrelextrema


# datas de inicio e fim Tendência de baixa nos últimos 200 dias
start = dt.datetime.now() - dt.timedelta(days=730)  # 2 anos atrás
um_ano_atras = dt.datetime.now() - dt.timedelta(days=365)
start2 = dt.datetime.now() - dt.timedelta(days=365)  # 1 ano atrás
end = datetime.now()
Lista_oficial = []
volume_minimo = 500000
preco_minimo = 5.0

Lista_backteste_inteli = []
# 🔹 1. Carregar os dados
Lista_backteste = pd.read_csv("analise_acoes.csv")
Lista_backteste_pronta = pd.read_csv("backtest_acoes.csv")

# 🔹 2. Remover colunas irrelevantes
Lista_backteste = Lista_backteste.drop(columns=[
    'Ativo Meta', 'Empresa', 'Preço atual', 'Total', 'Liquidez minima'
], errors='ignore')  # evita erro se alguma coluna não existir

print('🔹 Iniciando o backtest...')

for i, linha in Lista_backteste.iterrows():

    ativoB = linha['Ativo']
    proximo_balancoB = linha['proximo Balanco']
    proximo_balancoB = pd.to_datetime(proximo_balancoB)
    dataB = linha['proximo Balanco']
   
    
    

    if proximo_balancoB.normalize() <= pd.Timestamp.now().normalize():


        if not Lista_backteste_pronta.loc[(Lista_backteste_pronta['Ativo'] == ativoB) & (Lista_backteste_pronta["proximo Balanco"] == dataB)].empty:
            pass
        else:
            
            tendenciaB = linha['Tendencia 200 dias']
            gapB = linha['Gap Relevante 7 dias']
            rompimentoB = linha['Rompimento 20 dias']
            topoB = linha['Topos e Fundos']
            sp500B = linha['SP500 em baixa']
            balancoB = linha['3 Balanço negativo']
            setorB = linha['Setor Fragilizado']
            epsB = linha['negativas de lucro (EPS)']
            shortB = linha['Short Float 10']
            AtrB = linha['ATR acima da média 3 meses']
            historicoB = linha['Histórico com gaps relevantes']

            start = proximo_balancoB  - pd.offsets.BDay(3)

            end = proximo_balancoB + pd.offsets.BDay(1)  # Adiciona um dia para evitar o mesmo dia da entrada

            backtest = yf.download( ativoB, start=start, end=end, interval="1d", auto_adjust=True, progress=False, threads=False)

            backtest.columns = ['Close', 'High', 'Low', 'Open', 'Volume']
            # Pega a abertura do primeiro dia
            entradaB = round(backtest.iloc[0]['Open'], 2)
            # Pega o fechamento do último dia
            saidaB = round(backtest.iloc[-1]['Close'], 2)
            resultadoB = entradaB - saidaB
            resultadoB = round(resultadoB, 2)
            

            if resultadoB > 0:
                ResultadoF = 1
                #print(f"Ativo: {ativoB} deu {resultadoB} de gain")
            else:
                ResultadoF = 0
                #print(f"Ativo: {ativoB} deu {resultadoB} de loss")

        
            
            print(f"Ativo: {ativoB} add ao backtest")
            backteste_linha = {
                        'Ativo': ativoB,
                        'Tendencia 200 dias': tendenciaB,
                        'Gap Relevante 7 dias': gapB, 
                        'Rompimento 20 dias': rompimentoB, 
                        'Topos e Fundos': topoB,
                        'SP500 em baixa': sp500B,
                        '3 Balanço negativo': balancoB, 
                        'Setor Fragilizado': setorB,
                        'negativas de lucro (EPS)': epsB, 
                        'Short Float 10': shortB,
                        'ATR acima da média 3 meses': AtrB,
                        'Histórico com gaps relevantes': historicoB,
                        'proximo Balanco': proximo_balancoB,
                        'Total': ResultadoF,
                        }
            df_novoB = pd.DataFrame([backteste_linha])
            # Salva no CSV (append)
            df_novoB.to_csv("backtest_acoes.csv", mode='a', header=False, index=False, encoding='utf-8-sig')
            time.sleep(1)
print('🔹 Backtest concluído!')



exchange_map = {
    "NMS": "NAS",
    "NYQ": "NYSE",
}

# Dicionário de setores com tickers do Yahoo Finance
setores_yfinance = {
"MMM": {"Setor": "Industrials", "Empresa": "3M Company"},
"AOS": {"Setor": "Industrials", "Empresa": "A. O. Smith Corporation"},
"ABT": {"Setor": "Healthcare", "Empresa": "Abbott Laboratories"},
"ABBV": {"Setor": "Healthcare", "Empresa": "AbbVie Inc."},
"ACN": {"Setor": "Technology", "Empresa": "Accenture plc"},
"ADBE": {"Setor": "Technology", "Empresa": "Adobe Inc."},
"AMD": {"Setor": "Technology", "Empresa": "Advanced Micro Devices, Inc."},
"AES": {"Setor": "Utilities", "Empresa": "The AES Corporation"},
"AFL": {"Setor": "Financial Services", "Empresa": "Aflac Incorporated"},
"A": {"Setor": "Healthcare", "Empresa": "Agilent Technologies, Inc."},
"APD": {"Setor": "Basic Materials", "Empresa": "Air Products and Chemicals, Inc."},
"ABNB": {"Setor": "Consumer Cyclical", "Empresa": "Airbnb, Inc."},
"AKAM": {"Setor": "Technology", "Empresa": "Akamai Technologies, Inc."},
"ALB": {"Setor": "Basic Materials", "Empresa": "Albemarle Corporation"},
"ARE": {"Setor": "Real Estate", "Empresa": "Alexandria Real Estate Equities, Inc."},
"ALGN": {"Setor": "Healthcare", "Empresa": "Align Technology, Inc."},
"ALLE": {"Setor": "Industrials", "Empresa": "Allegion plc"},
"LNT": {"Setor": "Utilities", "Empresa": "Alliant Energy Corporation"},
"GOOGL": {"Setor": "Communication Services", "Empresa": "Alphabet Inc."},
"GOOG": {"Setor": "Communication Services", "Empresa": "Alphabet Inc."},
"MO": {"Setor": "Consumer Defensive", "Empresa": "Altria Group, Inc."},
"AMZN": {"Setor": "Consumer Cyclical", "Empresa": "Amazon.com, Inc."},
"AMCR": {"Setor": "Consumer Cyclical", "Empresa": "Amcor plc"},
"AEE": {"Setor": "Utilities", "Empresa": "Ameren Corporation"},
"AEP": {"Setor": "Utilities", "Empresa": "American Electric Power Company, Inc."},
"AXP": {"Setor": "Financial Services", "Empresa": "American Express Company"},
"AIG": {"Setor": "Financial Services", "Empresa": "American International Group, Inc."},
"AMT": {"Setor": "Real Estate", "Empresa": "American Tower Corporation"},
"AWK": {"Setor": "Utilities", "Empresa": "American Water Works Company, Inc."},
"AMP": {"Setor": "Financial Services", "Empresa": "Ameriprise Financial, Inc."},
"AME": {"Setor": "Industrials", "Empresa": "AMETEK, Inc."},
"AMGN": {"Setor": "Healthcare", "Empresa": "Amgen Inc."},
"APH": {"Setor": "Technology", "Empresa": "Amphenol Corporation"},
"ADI": {"Setor": "Technology", "Empresa": "Analog Devices, Inc."},
"ANSS": {"Setor": "Technology", "Empresa": "ANSYS, Inc."},
"AON": {"Setor": "Financial Services", "Empresa": "Aon plc"},
"APA": {"Setor": "Energy", "Empresa": "APA Corporation"},
"APO": {"Setor": "Financial Services", "Empresa": "Apollo Global Management, Inc."},
"AAPL": {"Setor": "Technology", "Empresa": "Apple Inc."},
"AMAT": {"Setor": "Technology", "Empresa": "Applied Materials, Inc."},
"APTV": {"Setor": "Consumer Cyclical", "Empresa": "Aptiv PLC"},
"ACGL": {"Setor": "Financial Services", "Empresa": "Arch Capital Group Ltd."},
"ADM": {"Setor": "Consumer Defensive", "Empresa": "Archer-Daniels-Midland Company"},
"ANET": {"Setor": "Technology", "Empresa": "Arista Networks Inc"},
"AJG": {"Setor": "Financial Services", "Empresa": "Arthur J. Gallagher & Co."},
"AIZ": {"Setor": "Financial Services", "Empresa": "Assurant, Inc."},
"T": {"Setor": "Communication Services", "Empresa": "AT&T Inc."},
"ATO": {"Setor": "Utilities", "Empresa": "Atmos Energy Corporation"},
"ADSK": {"Setor": "Technology", "Empresa": "Autodesk, Inc."},
"ADP": {"Setor": "Technology", "Empresa": "Automatic Data Processing, Inc."},
"AZO": {"Setor": "Consumer Cyclical", "Empresa": "AutoZone, Inc."},
"AVB": {"Setor": "Real Estate", "Empresa": "AvalonBay Communities, Inc."},
"AVY": {"Setor": "Industrials", "Empresa": "Avery Dennison Corporation"},
"AXON": {"Setor": "Industrials", "Empresa": "Axon Enterprise, Inc."},
"BKR": {"Setor": "Energy", "Empresa": "Baker Hughes Company"},
"BALL": {"Setor": "Consumer Cyclical", "Empresa": "Ball Corporation"},
"BAC": {"Setor": "Financial Services", "Empresa": "Bank of America Corporation"},
"BAX": {"Setor": "Healthcare", "Empresa": "Baxter International Inc."},
"BDX": {"Setor": "Healthcare", "Empresa": "Becton, Dickinson and Company"},
"BBY": {"Setor": "Consumer Cyclical", "Empresa": "Best Buy Co., Inc."},
"TECH": {"Setor": "Healthcare", "Empresa": "Bio-Techne Corporation"},
"BIIB": {"Setor": "Healthcare", "Empresa": "Biogen Inc."},
"BLK": {"Setor": "Financial Services", "Empresa": "BlackRock, Inc."},
"BX": {"Setor": "Financial Services", "Empresa": "Blackstone Inc."},
"BK": {"Setor": "Financial Services", "Empresa": "The Bank of New York Mellon Corporation"},
"BA": {"Setor": "Industrials", "Empresa": "The Boeing Company"},
"BKNG": {"Setor": "Consumer Cyclical", "Empresa": "Booking Holdings Inc."},
"BSX": {"Setor": "Healthcare", "Empresa": "Boston Scientific Corporation"},
"BMY": {"Setor": "Healthcare", "Empresa": "Bristol-Myers Squibb Company"},
"AVGO": {"Setor": "Technology", "Empresa": "Broadcom Inc."},
"BR": {"Setor": "Technology", "Empresa": "Broadridge Financial Solutions, Inc."},
"BRO": {"Setor": "Financial Services", "Empresa": "Brown & Brown, Inc."},
"BLDR": {"Setor": "Industrials", "Empresa": "Builders FirstSource, Inc."},
"BG": {"Setor": "Consumer Defensive", "Empresa": "Bunge Global SA"},
"BXP": {"Setor": "Real Estate", "Empresa": "BXP, Inc."},
"CHRW": {"Setor": "Industrials", "Empresa": "C.H. Robinson Worldwide, Inc."},
"CDNS": {"Setor": "Technology", "Empresa": "Cadence Design Systems, Inc."},
"CZR": {"Setor": "Consumer Cyclical", "Empresa": "Caesars Entertainment, Inc."},
"CPT": {"Setor": "Real Estate", "Empresa": "Camden Property Trust"},
"CPB": {"Setor": "Consumer Defensive", "Empresa": "The Campbell's Company"},
"COF": {"Setor": "Financial Services", "Empresa": "Capital One Financial Corporation"},
"CAH": {"Setor": "Healthcare", "Empresa": "Cardinal Health, Inc."},
"KMX": {"Setor": "Consumer Cyclical", "Empresa": "CarMax, Inc."},
"CARR": {"Setor": "Industrials", "Empresa": "Carrier Global Corporation"},
"CAT": {"Setor": "Industrials", "Empresa": "Caterpillar Inc."},
"CBOE": {"Setor": "Financial Services", "Empresa": "Cboe Global Markets, Inc."},
"CBRE": {"Setor": "Real Estate", "Empresa": "CBRE Group, Inc."},
"CDW": {"Setor": "Technology", "Empresa": "CDW Corporation"},
"COR": {"Setor": "Healthcare", "Empresa": "Cencora, Inc."},
"CNC": {"Setor": "Healthcare", "Empresa": "Centene Corporation"},
"CNP": {"Setor": "Utilities", "Empresa": "CenterPoint Energy, Inc."},
"CF": {"Setor": "Basic Materials", "Empresa": "CF Industries Holdings, Inc."},
"CRL": {"Setor": "Healthcare", "Empresa": "Charles River Laboratories International, Inc."},
"SCHW": {"Setor": "Financial Services", "Empresa": "The Charles Schwab Corporation"}, 
"CHTR": {"Setor": "Communication Services", "Empresa": "Charter Communications, Inc."},
"CVX": {"Setor": "Energy", "Empresa": "Chevron Corporation"},
"CMG": {"Setor": "Consumer Cyclical", "Empresa": "Chipotle Mexican Grill, Inc."},
"CB": {"Setor": "Financial Services", "Empresa": "Chubb Limited"},
"CHD": {"Setor": "Consumer Defensive", "Empresa": "Church & Dwight Co., Inc."},
"CI": {"Setor": "Healthcare", "Empresa": "The Cigna Group"},
"CINF": {"Setor": "Financial Services", "Empresa": "Cincinnati Financial Corporation"},
"CTAS": {"Setor": "Industrials", "Empresa": "Cintas Corporation"},
"CSCO": {"Setor": "Technology", "Empresa": "Cisco Systems, Inc."},
"C": {"Setor": "Financial Services", "Empresa": "Citigroup Inc."},
"CFG": {"Setor": "Financial Services", "Empresa": "Citizens Financial Group, Inc."},
"CLX": {"Setor": "Consumer Defensive", "Empresa": "The Clorox Company"},
"CME": {"Setor": "Financial Services", "Empresa": "CME Group Inc."},
"CMS": {"Setor": "Utilities", "Empresa": "CMS Energy Corporation"},
"KO": {"Setor": "Consumer Defensive", "Empresa": "The Coca-Cola Company"},
"CTSH": {"Setor": "Technology", "Empresa": "Cognizant Technology Solutions Corporation"},
"COIN": {"Setor": "Financial Services", "Empresa": "Coinbase Global, Inc."},
"CL": {"Setor": "Consumer Defensive", "Empresa": "Colgate-Palmolive Company"},
"CMCSA": {"Setor": "Communication Services", "Empresa": "Comcast Corporation"},
"CAG": {"Setor": "Consumer Defensive", "Empresa": "Conagra Brands, Inc."},
"COP": {"Setor": "Energy", "Empresa": "ConocoPhillips"},
"ED": {"Setor": "Utilities", "Empresa": "Consolidated Edison, Inc."},
"STZ": {"Setor": "Consumer Defensive", "Empresa": "Constellation Brands, Inc."},
"CEG": {"Setor": "Utilities", "Empresa": "Constellation Energy Corporation"},
"COO": {"Setor": "Healthcare", "Empresa": "The Cooper Companies, Inc."},
"CPRT": {"Setor": "Industrials", "Empresa": "Copart, Inc."},
"GLW": {"Setor": "Technology", "Empresa": "Corning Incorporated"},
"CPAY": {"Setor": "Technology", "Empresa": "Corpay, Inc."},
"CTVA": {"Setor": "Basic Materials", "Empresa": "Corteva, Inc."},
"CSGP": {"Setor": "Real Estate", "Empresa": "CoStar Group, Inc."},
"COST": {"Setor": "Consumer Defensive", "Empresa": "Costco Wholesale Corporation"},
"CTRA": {"Setor": "Energy", "Empresa": "Coterra Energy Inc."},
"CRWD": {"Setor": "Technology", "Empresa": "CrowdStrike Holdings, Inc."},
"CCI": {"Setor": "Real Estate", "Empresa": "Crown Castle Inc."},
"CSX": {"Setor": "Industrials", "Empresa": "CSX Corporation"},
"CMI": {"Setor": "Industrials", "Empresa": "Cummins Inc."},
"CVS": {"Setor": "Healthcare", "Empresa": "CVS Health Corporation"},
"DHR": {"Setor": "Healthcare", "Empresa": "Danaher Corporation"},
"DRI": {"Setor": "Consumer Cyclical", "Empresa": "Darden Restaurants, Inc."},
"DVA": {"Setor": "Healthcare", "Empresa": "DaVita Inc."},
"DAY": {"Setor": "Technology", "Empresa": "Dayforce Inc"},
"DECK": {"Setor": "Consumer Cyclical", "Empresa": "Deckers Outdoor Corporation"},
"DE": {"Setor": "Industrials", "Empresa": "Deere & Company"},
"DELL": {"Setor": "Technology", "Empresa": "Dell Technologies Inc."},
"DAL": {"Setor": "Industrials", "Empresa": "Delta Air Lines, Inc."},
"DVN": {"Setor": "Energy", "Empresa": "Devon Energy Corporation"},
"DXCM": {"Setor": "Healthcare", "Empresa": "DexCom, Inc."},
"FANG": {"Setor": "Energy", "Empresa": "Diamondback Energy, Inc."},
"DLR": {"Setor": "Real Estate", "Empresa": "Digital Realty Trust, Inc."},
"DG": {"Setor": "Consumer Defensive", "Empresa": "Dollar General Corporation"},
"DLTR": {"Setor": "Consumer Defensive", "Empresa": "Dollar Tree, Inc."},
"D": {"Setor": "Utilities", "Empresa": "Dominion Energy, Inc."},
"DPZ": {"Setor": "Consumer Cyclical", "Empresa": "Domino's Pizza, Inc."},
"DASH": {"Setor": "Consumer Cyclical", "Empresa": "DoorDash, Inc."},
"DOV": {"Setor": "Industrials", "Empresa": "Dover Corporation"},
"DOW": {"Setor": "Basic Materials", "Empresa": "Dow Inc."},
"DHI": {"Setor": "Consumer Cyclical", "Empresa": "D.R. Horton, Inc."},
"DTE": {"Setor": "Utilities", "Empresa": "DTE Energy Company"},
"DUK": {"Setor": "Utilities", "Empresa": "Duke Energy Corporation"},
"DD": {"Setor": "Basic Materials", "Empresa": "DuPont de Nemours, Inc."},
"EMN": {"Setor": "Basic Materials", "Empresa": "Eastman Chemical Company"},
"ETN": {"Setor": "Industrials", "Empresa": "Eaton Corporation plc"},
"EBAY": {"Setor": "Consumer Cyclical", "Empresa": "eBay Inc."},
"ECL": {"Setor": "Basic Materials", "Empresa": "Ecolab Inc."},
"EIX": {"Setor": "Utilities", "Empresa": "Edison International"},
"EW": {"Setor": "Healthcare", "Empresa": "Edwards Lifesciences Corporation"},
"EA": {"Setor": "Communication Services", "Empresa": "Electronic Arts Inc."},
"ELV": {"Setor": "Healthcare", "Empresa": "Elevance Health, Inc."},
"EMR": {"Setor": "Industrials", "Empresa": "Emerson Electric Co."},
"ENPH": {"Setor": "Technology", "Empresa": "Enphase Energy, Inc."},
"ETR": {"Setor": "Utilities", "Empresa": "Entergy Corporation"},
"EOG": {"Setor": "Energy", "Empresa": "EOG Resources, Inc."},
"EPAM": {"Setor": "Technology", "Empresa": "EPAM Systems, Inc."},
"EQT": {"Setor": "Energy", "Empresa": "EQT Corporation"},
"EFX": {"Setor": "Industrials", "Empresa": "Equifax Inc."},
"EQIX": {"Setor": "Real Estate", "Empresa": "Equinix, Inc."},
"EQR": {"Setor": "Real Estate", "Empresa": "Equity Residential"},
"ERIE": {"Setor": "Financial Services", "Empresa": "Erie Indemnity Company"},
"ESS": {"Setor": "Real Estate", "Empresa": "Essex Property Trust, Inc."},
"EL": {"Setor": "Consumer Defensive", "Empresa": "The Estée Lauder Companies Inc."},
"EG": {"Setor": "Industrials", "Empresa": "Everest Group, Ltd."},
"EVRG": {"Setor": "Utilities", "Empresa": "Evergy, Inc."},
"ES": {"Setor": "Utilities", "Empresa": "Eversource Energy"},
"EXC": {"Setor": "Utilities", "Empresa": "Exelon Corporation"},
"EXE": {"Setor": "Energy", "Empresa": "Expand Energy Corporation"},
"EXPE": {"Setor": "Consumer Cyclical", "Empresa": "Expedia Group, Inc."},
"EXPD": {"Setor": "Industrials", "Empresa": "Expeditors International of Washington, Inc."},
"EXR": {"Setor": "Real Estate", "Empresa": "Extra Space Storage Inc."},
"XOM": {"Setor": "Energy", "Empresa": "Exxon Mobil Corporation"},
"FFIV": {"Setor": "Technology", "Empresa": "F5, Inc."},
"FDS": {"Setor": "Financial Services", "Empresa": "FactSet Research Systems Inc."},
"FICO": {"Setor": "Technology", "Empresa": "Fair Isaac Corporation"},
"FAST": {"Setor": "Industrials", "Empresa": "Fastenal Company"},
"FRT": {"Setor": "Real Estate", "Empresa": "Federal Realty Investment Trust"},
"FDX": {"Setor": "Industrials", "Empresa": "FedEx Corporation"},
"FITB": {"Setor": "Financial Services", "Empresa": "Fifth Third Bancorp"},
"FSLR": {"Setor": "Technology", "Empresa": "First Solar, Inc."},
"FE": {"Setor": "Utilities", "Empresa": "FirstEnergy Corp."},
"FI": {"Setor": "Technology", "Empresa": "Fiserv, Inc."},
"F": {"Setor": "Consumer Cyclical", "Empresa": "Ford Motor Company"},
"FTNT": {"Setor": "Technology", "Empresa": "Fortinet, Inc."},
"FTV": {"Setor": "Technology", "Empresa": "Fortive Corporation"},
"FOXA": {"Setor": "Communication Services", "Empresa": "Fox Corporation"},
"FOX": {"Setor": "Communication Services", "Empresa": "Fox Corporation"},
"BEN": {"Setor": "Financial Services", "Empresa": "Franklin Resources, Inc."},
"FCX": {"Setor": "Basic Materials", "Empresa": "Freeport-McMoRan Inc."},
"GRMN": {"Setor": "Technology", "Empresa": "Garmin Ltd."},
"IT": {"Setor": "Technology", "Empresa": "Gartner, Inc."},
"GE": {"Setor": "Industrials", "Empresa": "GE Aerospace"},
"GEHC": {"Setor": "Healthcare", "Empresa": "GE HealthCare Technologies Inc."},
"GEV": {"Setor": "Industrials", "Empresa": "GE Vernova Inc."},
"GEN": {"Setor": "Technology", "Empresa": "Gen Digital Inc."},
"GNRC": {"Setor": "Industrials", "Empresa": "Generac Holdings Inc."},
"GD": {"Setor": "Industrials", "Empresa": "General Dynamics Corporation"},
"GIS": {"Setor": "Consumer Defensive", "Empresa": "General Mills, Inc."},
"GM": {"Setor": "Consumer Cyclical", "Empresa": "General Motors Company"},
"GPC": {"Setor": "Consumer Cyclical", "Empresa": "Genuine Parts Company"},
"GILD": {"Setor": "Healthcare", "Empresa": "Gilead Sciences, Inc."},
"GPN": {"Setor": "Industrials", "Empresa": "Global Payments Inc."},
"GL": {"Setor": "Financial Services", "Empresa": "Globe Life Inc."},
"GDDY": {"Setor": "Technology", "Empresa": "GoDaddy Inc."},
"GS": {"Setor": "Financial Services", "Empresa": "The Goldman Sachs Group, Inc."},
"HAL": {"Setor": "Energy", "Empresa": "Halliburton Company"},
"HIG": {"Setor": "Financial Services", "Empresa": "The Hartford Insurance Group, Inc."},
"HAS": {"Setor": "Consumer Cyclical", "Empresa": "Hasbro, Inc."},
"HCA": {"Setor": "Healthcare", "Empresa": "HCA Healthcare, Inc."},
"DOC": {"Setor": "Real Estate", "Empresa": "Healthpeak Properties, Inc."},
"HSIC": {"Setor": "Healthcare", "Empresa": "Henry Schein, Inc."},
"HSY": {"Setor": "Consumer Defensive", "Empresa": "The Hershey Company"},
"HPE": {"Setor": "Technology", "Empresa": "Hewlett Packard Enterprise Company"},
"HLT": {"Setor": "Consumer Cyclical", "Empresa": "Hilton Worldwide Holdings Inc."},
"HOLX": {"Setor": "Healthcare", "Empresa": "Hologic, Inc."},
"HD": {"Setor": "Consumer Cyclical", "Empresa": "The Home Depot, Inc."},
"HON": {"Setor": "Industrials", "Empresa": "Honeywell International Inc."},
"HRL": {"Setor": "Consumer Defensive", "Empresa": "Hormel Foods Corporation"},
"HST": {"Setor": "Real Estate", "Empresa": "Host Hotels & Resorts, Inc."},
"HWM": {"Setor": "Industrials", "Empresa": "Howmet Aerospace Inc."},
"HPQ": {"Setor": "Technology", "Empresa": "HP Inc."},
"HUBB": {"Setor": "Industrials", "Empresa": "Hubbell Incorporated"},
"HUM": {"Setor": "Healthcare", "Empresa": "Humana Inc."},
"HBAN": {"Setor": "Financial Services", "Empresa": "Huntington Bancshares Incorporated"},
"HII": {"Setor": "Industrials", "Empresa": "Huntington Ingalls Industries, Inc."},
"IBM": {"Setor": "Technology", "Empresa": "International Business Machines Corporation"},
"IEX": {"Setor": "Industrials", "Empresa": "IDEX Corporation"},
"IDXX": {"Setor": "Healthcare", "Empresa": "IDEXX Laboratories, Inc."},
"ITW": {"Setor": "Industrials", "Empresa": "Illinois Tool Works Inc."},
"INCY": {"Setor": "Healthcare", "Empresa": "Incyte Corporation"},
"IR": {"Setor": "Industrials", "Empresa": "Ingersoll Rand Inc."},
"PODD": {"Setor": "Healthcare", "Empresa": "Insulet Corporation"},
"INTC": {"Setor": "Technology", "Empresa": "Intel Corporation"},
"ICE": {"Setor": "Financial Services", "Empresa": "Intercontinental Exchange, Inc."},
"IFF": {"Setor": "Basic Materials", "Empresa": "International Flavors & Fragrances Inc."},
"IP": {"Setor": "Basic Materials", "Empresa": "International Paper Company"},
"INTU": {"Setor": "Technology", "Empresa": "Intuit Inc."},
"ISRG": {"Setor": "Healthcare", "Empresa": "Intuitive Surgical, Inc."},
"IVZ": {"Setor": "Financial Services", "Empresa": "Invesco Ltd."},
"INVH": {"Setor": "Real Estate", "Empresa": "Invitation Homes Inc."},
"IQV": {"Setor": "Healthcare", "Empresa": "IQVIA Holdings Inc."},
"IRM": {"Setor": "Real Estate", "Empresa": "Iron Mountain Incorporated"},
"JBHT": {"Setor": "Industrials", "Empresa": "J.B. Hunt Transport Services, Inc."},
"JBL": {"Setor": "Technology", "Empresa": "Jabil Inc."},
"JKHY": {"Setor": "Technology", "Empresa": "Jack Henry & Associates, Inc."},
"J": {"Setor": "Industrials", "Empresa": "Jacobs Solutions Inc."},
"JNJ": {"Setor": "Healthcare", "Empresa": "Johnson & Johnson"},
"JCI": {"Setor": "Industrials", "Empresa": "Johnson Controls International plc"},
"JPM": {"Setor": "Financial Services", "Empresa": "JPMorgan Chase & Co."},
"K": {"Setor": "Consumer Defensive", "Empresa": "Kellanova"},
"KVUE": {"Setor": "Consumer Defensive", "Empresa": "Kenvue Inc."},
"KDP": {"Setor": "Consumer Defensive", "Empresa": "Keurig Dr Pepper Inc."},
"KEY": {"Setor": "Financial Services", "Empresa": "KeyCorp"},
"KEYS": {"Setor": "Technology", "Empresa": "Keysight Technologies, Inc."},
"KMB": {"Setor": "Consumer Defensive", "Empresa": "Kimberly-Clark Corporation"},
"KIM": {"Setor": "Real Estate", "Empresa": "Kimco Realty Corporation"},
"KMI": {"Setor": "Energy", "Empresa": "Kinder Morgan, Inc."},
"KKR": {"Setor": "Financial Services", "Empresa": "KKR & Co. Inc."},
"KLAC": {"Setor": "Technology", "Empresa": "KLA Corporation"},
"KHC": {"Setor": "Consumer Defensive", "Empresa": "The Kraft Heinz Company"},
"KR": {"Setor": "Consumer Defensive", "Empresa": "The Kroger Co."},
"LHX": {"Setor": "Industrials", "Empresa": "L3Harris Technologies, Inc."},
"LH": {"Setor": "Healthcare", "Empresa": "Labcorp Holdings Inc."},
"LRCX": {"Setor": "Technology", "Empresa": "Lam Research Corporation"},
"LW": {"Setor": "Consumer Defensive", "Empresa": "Lamb Weston Holdings, Inc."},
"LVS": {"Setor": "Consumer Cyclical", "Empresa": "Las Vegas Sands Corp."},
"LDOS": {"Setor": "Technology", "Empresa": "Leidos Holdings, Inc."},
"LEN": {"Setor": "Consumer Cyclical", "Empresa": "Lennar Corporation"},
"LII": {"Setor": "Industrials", "Empresa": "Lennox International Inc."},
"LLY": {"Setor": "Healthcare", "Empresa": "Eli Lilly and Company"},
"LIN": {"Setor": "Basic Materials", "Empresa": "Linde plc"},
"LYV": {"Setor": "Communication Services", "Empresa": "Live Nation Entertainment, Inc."},
"LKQ": {"Setor": "Consumer Cyclical", "Empresa": "LKQ Corporation"},
"LMT": {"Setor": "Industrials", "Empresa": "Lockheed Martin Corporation"},
"L": {"Setor": "Financial Services", "Empresa": "Loews Corporation"},
"LOW": {"Setor": "Consumer Cyclical", "Empresa": "Lowe's Companies, Inc."},
"LULU": {"Setor": "Consumer Cyclical", "Empresa": "lululemon athletica inc."},
"LYB": {"Setor": "Basic Materials", "Empresa": "LyondellBasell Industries N.V."},
"MTB": {"Setor": "Financial Services", "Empresa": "M&T Bank Corporation"},
"MPC": {"Setor": "Energy", "Empresa": "Marathon Petroleum Corporation"},
"MKTX": {"Setor": "Financial Services", "Empresa": "MarketAxess Holdings Inc."},
"MAR": {"Setor": "Consumer Cyclical", "Empresa": "Marriott International, Inc."},
"MMC": {"Setor": "Financial Services", "Empresa": "Marsh & McLennan Companies, Inc."},
"MLM": {"Setor": "Basic Materials", "Empresa": "Martin Marietta Materials, Inc."},
"MAS": {"Setor": "Industrials", "Empresa": "Masco Corporation"},
"MA": {"Setor": "Financial Services", "Empresa": "Mastercard Incorporated"},
"MTCH": {"Setor": "Communication Services", "Empresa": "Match Group, Inc."},
"MKC": {"Setor": "Consumer Defensive", "Empresa": "McCormick & Company, Incorporated"},
"MCD": {"Setor": "Consumer Cyclical", "Empresa": "McDonald's Corporation"},
"MCK": {"Setor": "Healthcare", "Empresa": "McKesson Corporation"},
"MDT": {"Setor": "Healthcare", "Empresa": "Medtronic plc"},
"MRK": {"Setor": "Healthcare", "Empresa": "Merck & Co., Inc."},
"META": {"Setor": "Communication Services", "Empresa": "Meta Platforms, Inc."},
"MET": {"Setor": "Financial Services", "Empresa": "MetLife, Inc."},
"MTD": {"Setor": "Healthcare", "Empresa": "Mettler-Toledo International Inc."},
"MGM": {"Setor": "Consumer Cyclical", "Empresa": "MGM Resorts International"},
"MCHP": {"Setor": "Technology", "Empresa": "Microchip Technology Incorporated"},
"MU": {"Setor": "Technology", "Empresa": "Micron Technology, Inc."},
"MSFT": {"Setor": "Technology", "Empresa": "Microsoft Corporation"},
"MAA": {"Setor": "Real Estate", "Empresa": "Mid-America Apartment Communities, Inc."},
"MRNA": {"Setor": "Healthcare", "Empresa": "Moderna, Inc."},
"MHK": {"Setor": "Consumer Cyclical", "Empresa": "Mohawk Industries, Inc."},
"MOH": {"Setor": "Healthcare", "Empresa": "Molina Healthcare, Inc."},
"TAP": {"Setor": "Consumer Defensive", "Empresa": "Molson Coors Beverage Company"},
"MDLZ": {"Setor": "Consumer Defensive", "Empresa": "Mondelez International, Inc."},
"MPWR": {"Setor": "Technology", "Empresa": "Monolithic Power Systems, Inc."},
"MNST": {"Setor": "Consumer Defensive", "Empresa": "Monster Beverage Corporation"},
"MCO": {"Setor": "Financial Services", "Empresa": "Moody's Corporation"},
"MS": {"Setor": "Financial Services", "Empresa": "Morgan Stanley"},
"MOS": {"Setor": "Basic Materials", "Empresa": "The Mosaic Company"},
"MSI": {"Setor": "Technology", "Empresa": "Motorola Solutions, Inc."},
"MSCI": {"Setor": "Financial Services", "Empresa": "MSCI Inc."},
"NDAQ": {"Setor": "Financial Services", "Empresa": "Nasdaq, Inc."},
"NTAP": {"Setor": "Technology", "Empresa": "NetApp, Inc."},
"NFLX": {"Setor": "Communication Services", "Empresa": "Netflix, Inc."},
"NEM": {"Setor": "Basic Materials", "Empresa": "Newmont Corporation"},
"NWSA": {"Setor": "Communication Services", "Empresa": "News Corporation"},
"NWS": {"Setor": "Communication Services", "Empresa": "News Corporation"},
"NEE": {"Setor": "Utilities", "Empresa": "NextEra Energy, Inc."},
"NKE": {"Setor": "Consumer Cyclical", "Empresa": "NIKE, Inc."},
"NI": {"Setor": "Utilities", "Empresa": "NiSource Inc."},
"NDSN": {"Setor": "Industrials", "Empresa": "Nordson Corporation"},
"NSC": {"Setor": "Industrials", "Empresa": "Norfolk Southern Corporation"},
"NTRS": {"Setor": "Financial Services", "Empresa": "Northern Trust Corporation"},
"NOC": {"Setor": "Industrials", "Empresa": "Northrop Grumman Corporation"},
"NCLH": {"Setor": "Consumer Cyclical", "Empresa": "Norwegian Cruise Line Holdings Ltd."},
"NRG": {"Setor": "Utilities", "Empresa": "NRG Energy, Inc."},
"NUE": {"Setor": "Basic Materials", "Empresa": "Nucor Corporation"},
"NVDA": {"Setor": "Technology", "Empresa": "NVIDIA Corporation"},
"NVR": {"Setor": "Consumer Cyclical", "Empresa": "NVR, Inc."},
"NXPI": {"Setor": "Technology", "Empresa": "NXP Semiconductors N.V."},
"ORLY": {"Setor": "Consumer Cyclical", "Empresa": "O'Reilly Automotive, Inc."},
"OXY": {"Setor": "Energy", "Empresa": "Occidental Petroleum Corporation"},
"ODFL": {"Setor": "Industrials", "Empresa": "Old Dominion Freight Line, Inc."},
"OMC": {"Setor": "Communication Services", "Empresa": "Omnicom Group Inc."},
"ON": {"Setor": "Technology", "Empresa": "ON Semiconductor Corporation"},
"OKE": {"Setor": "Energy", "Empresa": "ONEOK, Inc."},
"ORCL": {"Setor": "Technology", "Empresa": "Oracle Corporation"},
"OTIS": {"Setor": "Industrials", "Empresa": "Otis Worldwide Corporation"},
"PCAR": {"Setor": "Industrials", "Empresa": "PACCAR Inc"},
"PKG": {"Setor": "Consumer Cyclical", "Empresa": "Packaging Corporation of America"},
"PLTR": {"Setor": "Technology", "Empresa": "Palantir Technologies Inc."},
"PANW": {"Setor": "Technology", "Empresa": "Palo Alto Networks, Inc."},
"PARA": {"Setor": "Communication Services", "Empresa": "Paramount Global"},
"PH": {"Setor": "Industrials", "Empresa": "Parker-Hannifin Corporation"},
"PAYX": {"Setor": "Technology", "Empresa": "Paychex, Inc."},
"PAYC": {"Setor": "Technology", "Empresa": "Paycom Software, Inc."},
"PYPL": {"Setor": "Financial Services", "Empresa": "PayPal Holdings, Inc."},
"PNR": {"Setor": "Industrials", "Empresa": "Pentair plc"},
"PEP": {"Setor": "Consumer Defensive", "Empresa": "PepsiCo, Inc."},
"PFE": {"Setor": "Healthcare", "Empresa": "Pfizer Inc."},
"PCG": {"Setor": "Utilities", "Empresa": "PG&E Corporation"},
"PM": {"Setor": "Consumer Defensive", "Empresa": "Philip Morris International Inc."},
"PSX": {"Setor": "Energy", "Empresa": "Phillips 66"},
"PNW": {"Setor": "Utilities", "Empresa": "Pinnacle West Capital Corporation"},
"PNC": {"Setor": "Financial Services", "Empresa": "The PNC Financial Services Group, Inc."},
"POOL": {"Setor": "Industrials", "Empresa": "Pool Corporation"},
"PPG": {"Setor": "Basic Materials", "Empresa": "PPG Industries, Inc."},
"PPL": {"Setor": "Utilities", "Empresa": "PPL Corporation"},
"PFG": {"Setor": "Financial Services", "Empresa": "Principal Financial Group, Inc."},
"PG": {"Setor": "Consumer Defensive", "Empresa": "The Procter & Gamble Company"},
"PGR": {"Setor": "Financial Services", "Empresa": "The Progressive Corporation"},
"PLD": {"Setor": "Real Estate", "Empresa": "Prologis, Inc."},
"PRU": {"Setor": "Financial Services", "Empresa": "Prudential Financial, Inc."},
"PEG": {"Setor": "Utilities", "Empresa": "Public Service Enterprise Group Incorporated"},
"PTC": {"Setor": "Technology", "Empresa": "PTC Inc."},
"PSA": {"Setor": "Real Estate", "Empresa": "Public Storage"},
"PHM": {"Setor": "Consumer Cyclical", "Empresa": "PulteGroup, Inc."},
"PWR": {"Setor": "Industrials", "Empresa": "Quanta Services, Inc."},
"QCOM": {"Setor": "Technology", "Empresa": "QUALCOMM Incorporated"},
"DGX": {"Setor": "Healthcare", "Empresa": "Quest Diagnostics Incorporated"},
"RL": {"Setor": "Consumer Cyclical", "Empresa": "Ralph Lauren Corporation"},
"RJF": {"Setor": "Financial Services", "Empresa": "Raymond James Financial, Inc."},
"RTX": {"Setor": "Industrials", "Empresa": "RTX Corporation"},
"O": {"Setor": "Real Estate", "Empresa": "Realty Income Corporation"},
"REG": {"Setor": "Real Estate", "Empresa": "Regency Centers Corporation"},
"REGN": {"Setor": "Healthcare", "Empresa": "Regeneron Pharmaceuticals, Inc."},
"RF": {"Setor": "Financial Services", "Empresa": "Regions Financial Corporation"},
"RSG": {"Setor": "Industrials", "Empresa": "Republic Services, Inc."},
"RMD": {"Setor": "Healthcare", "Empresa": "ResMed Inc."},
"RVTY": {"Setor": "Healthcare", "Empresa": "Revvity, Inc."},
"ROK": {"Setor": "Industrials", "Empresa": "Rockwell Automation, Inc."},
"ROL": {"Setor": "Consumer Cyclical", "Empresa": "Rollins, Inc."},
"ROP": {"Setor": "Technology", "Empresa": "Roper Technologies, Inc."},
"ROST": {"Setor": "Consumer Cyclical", "Empresa": "Ross Stores, Inc."},
"RCL": {"Setor": "Consumer Cyclical", "Empresa": "Royal Caribbean Cruises Ltd."},
"SPGI": {"Setor": "Financial Services", "Empresa": "S&P Global Inc."},
"CRM": {"Setor": "Technology", "Empresa": "Salesforce, Inc."},
"SBAC": {"Setor": "Real Estate", "Empresa": "SBA Communications Corporation"},
"SLB": {"Setor": "Energy", "Empresa": "Schlumberger Limited"},
"STX": {"Setor": "Technology", "Empresa": "Seagate Technology Holdings plc"},
"SRE": {"Setor": "Utilities", "Empresa": "Sempra"},
"NOW": {"Setor": "Technology", "Empresa": "ServiceNow, Inc."},
"SPG": {"Setor": "Real Estate", "Empresa": "Simon Property Group, Inc."},
"SWKS": {"Setor": "Technology", "Empresa": "Skyworks Solutions, Inc."},
"SJM": {"Setor": "Consumer Defensive", "Empresa": "The J. M. Smucker Company"},
"SW": {"Setor": "Consumer Cyclical", "Empresa": "Smurfit Westrock Plc"},
"SNA": {"Setor": "Industrials", "Empresa": "Snap-on Incorporated"},
"SOLV": {"Setor": "Healthcare", "Empresa": "Solventum Corporation"},
"SO": {"Setor": "Utilities", "Empresa": "The Southern Company"},
"LUV": {"Setor": "Industrials", "Empresa": "Southwest Airlines Co."},
"SWK": {"Setor": "Industrials", "Empresa": "Stanley Black & Decker, Inc."},
"SBUX": {"Setor": "Consumer Cyclical", "Empresa": "Starbucks Corporation"},
"STT": {"Setor": "Financial Services", "Empresa": "State Street Corporation"},
"STLD": {"Setor": "Basic Materials", "Empresa": "Steel Dynamics, Inc."},
"STE": {"Setor": "Healthcare", "Empresa": "STERIS plc"},
"SMCI": {"Setor": "Technology", "Empresa": "Super Micro Computer, Inc."},
"SYF": {"Setor": "Financial Services", "Empresa": "Synchrony Financial"},
"SNPS": {"Setor": "Technology", "Empresa": "Synopsys, Inc."},
"SYY": {"Setor": "Consumer Defensive", "Empresa": "Sysco Corporation"},
"TMUS": {"Setor": "Communication Services", "Empresa": "T-Mobile US, Inc."},
"TROW": {"Setor": "Financial Services", "Empresa": "T. Rowe Price Group, Inc."},
"TTWO": {"Setor": "Communication Services", "Empresa": "Take-Two Interactive Software, Inc."},
"TPR": {"Setor": "Consumer Cyclical", "Empresa": "Tapestry, Inc."},
"TRGP": {"Setor": "Energy", "Empresa": "Targa Resources Corp."},
"TGT": {"Setor": "Consumer Defensive", "Empresa": "Target Corporation"},
"TEL": {"Setor": "Industrials", "Empresa": "TE Connectivity plc"},
"TDY": {"Setor": "Technology", "Empresa": "Teledyne Technologies Incorporated"},
"TER": {"Setor": "Technology", "Empresa": "Teradyne, Inc."},
"TSLA": {"Setor": "Consumer Cyclical", "Empresa": "Tesla, Inc."},
"TXN": {"Setor": "Technology", "Empresa": "Texas Instruments Incorporated"},
"TPL": {"Setor": "Real Estate", "Empresa": "Texas Pacific Land Corporation"},
"TXT": {"Setor": "Industrials", "Empresa": "Textron Inc."},
"TMO": {"Setor": "Healthcare", "Empresa": "Thermo Fisher Scientific Inc."},
"TJX": {"Setor": "Consumer Cyclical", "Empresa": "The TJX Companies, Inc."},
"TKO": {"Setor": "Communication Services", "Empresa": "TKO Group Holdings, Inc."},
"TSCO": {"Setor": "Consumer Cyclical", "Empresa": "Tractor Supply Company"},
"TT": {"Setor": "Industrials", "Empresa": "Trane Technologies plc"},
"TDG": {"Setor": "Industrials", "Empresa": "TransDigm Group Incorporated"},
"TRV": {"Setor": "Financial Services", "Empresa": "The Travelers Companies, Inc."},
"TRMB": {"Setor": "Technology", "Empresa": "Trimble Inc."},
"TFC": {"Setor": "Financial Services", "Empresa": "Truist Financial Corporation"},
"TYL": {"Setor": "Technology", "Empresa": "Tyler Technologies, Inc."},
"TSN": {"Setor": "Consumer Defensive", "Empresa": "Tyson Foods, Inc."},
"USB": {"Setor": "Financial Services", "Empresa": "U.S. Bancorp"},
"UBER": {"Setor": "Technology", "Empresa": "Uber Technologies, Inc."},
"UDR": {"Setor": "Real Estate", "Empresa": "UDR, Inc."},
"ULTA": {"Setor": "Consumer Cyclical", "Empresa": "Ulta Beauty, Inc."},
"UNP": {"Setor": "Industrials", "Empresa": "Union Pacific Corporation"},
"UAL": {"Setor": "Industrials", "Empresa": "United Airlines Holdings, Inc."},
"UPS": {"Setor": "Industrials", "Empresa": "United Parcel Service, Inc."},
"URI": {"Setor": "Industrials", "Empresa": "United Rentals, Inc."},
"UNH": {"Setor": "Healthcare", "Empresa": "UnitedHealth Group Incorporated"},
"UHS": {"Setor": "Healthcare", "Empresa": "Universal Health Services, Inc."},
"VLO": {"Setor": "Energy", "Empresa": "Valero Energy Corporation"},
"VTR": {"Setor": "Real Estate", "Empresa": "Ventas, Inc."},
"VLTO": {"Setor": "Industrials", "Empresa": "Veralto Corporation"},
"VRSN": {"Setor": "Technology", "Empresa": "VeriSign, Inc."},
"VRSK": {"Setor": "Industrials", "Empresa": "Verisk Analytics, Inc."},
"VZ": {"Setor": "Communication Services", "Empresa": "Verizon Communications Inc."},
"VRTX": {"Setor": "Healthcare", "Empresa": "Vertex Pharmaceuticals Incorporated"},
"VTRS": {"Setor": "Healthcare", "Empresa": "Viatris Inc."},
"VICI": {"Setor": "Real Estate", "Empresa": "VICI Properties Inc."},
"V": {"Setor": "Financial Services", "Empresa": "Visa Inc."},
"VST": {"Setor": "Utilities", "Empresa": "Vistra Corp."},
"VMC": {"Setor": "Basic Materials", "Empresa": "Vulcan Materials Company"},
"WRB": {"Setor": "Financial Services", "Empresa": "W. R. Berkley Corporation"},
"GWW": {"Setor": "Industrials", "Empresa": "W.W. Grainger, Inc."},
"WAB": {"Setor": "Industrials", "Empresa": "Westinghouse Air Brake Technologies Corporation"},
"WBA": {"Setor": "Healthcare", "Empresa": "Walgreens Boots Alliance, Inc."},
"WMT": {"Setor": "Consumer Defensive", "Empresa": "Walmart Inc."},
"DIS": {"Setor": "Communication Services", "Empresa": "The Walt Disney Company"},
"WBD": {"Setor": "Communication Services", "Empresa": "Warner Bros. Discovery, Inc."},
"WM": {"Setor": "Industrials", "Empresa": "Waste Management, Inc."},
"WAT": {"Setor": "Healthcare", "Empresa": "Waters Corporation"},
"WEC": {"Setor": "Utilities", "Empresa": "WEC Energy Group, Inc."},
"WFC": {"Setor": "Financial Services", "Empresa": "Wells Fargo & Company"},
"WELL": {"Setor": "Real Estate", "Empresa": "Welltower Inc."},
"WST": {"Setor": "Healthcare", "Empresa": "West Pharmaceutical Services, Inc."},
"WDC": {"Setor": "Technology", "Empresa": "Western Digital Corporation"},
"WY": {"Setor": "Real Estate", "Empresa": "Weyerhaeuser Company"},
"WSM": {"Setor": "Consumer Cyclical", "Empresa": "Williams-Sonoma, Inc."},
"WMB": {"Setor": "Energy", "Empresa": "The Williams Companies, Inc."},
"WTW": {"Setor": "Financial Services", "Empresa": "Willis Towers Watson Public Limited Company"},
"WDAY": {"Setor": "Technology", "Empresa": "Workday, Inc."},
"WYNN": {"Setor": "Consumer Cyclical", "Empresa": "Wynn Resorts, Limited"},
"XEL": {"Setor": "Utilities", "Empresa": "Xcel Energy Inc."},
"XYL": {"Setor": "Industrials", "Empresa": "Xylem Inc."},
"YUM": {"Setor": "Consumer Cyclical", "Empresa": "Yum! Brands, Inc."},
"ZBRA": {"Setor": "Technology", "Empresa": "Zebra Technologies Corporation"},
"ZBH": {"Setor": "Healthcare", "Empresa": "Zimmer Biomet Holdings, Inc."},
"ZTS": {"Setor": "Healthcare", "Empresa": "Zoetis Inc."},


}
#########################################################################################################
# SP500 em tendência de baixa?
####################################################################################################
# Baixar dados do S&P 500 (^GSPC)
time.sleep(2)
sp500 = yf.download('^GSPC', start=start, end=end, interval="1d", auto_adjust=True, progress=False, threads=False)
sp500.columns = ['Close', 'High', 'Low', 'Open', 'Volume']

# Calcular médias móveis de 20 e 50 dias
sp500['MM20'] = sp500['Close'].rolling(window=20).mean()
sp500['MM50'] = sp500['Close'].rolling(window=50).mean()

# Remover linhas com NaN (antes do dia 50)
sp500.dropna(inplace=True)

# Verificar tendência de baixa (MM20 < MM50 na última linha)
ultima_linha = sp500.iloc[-1]
if ultima_linha['MM20'] < ultima_linha['MM50']:
    sp500_resultado = 1
    print("S&P 500 está em tendência de baixa.")
else:
    sp500_resultado = 0
    print("S&P 500 NÃO está em tendência de baixa.")

# Loop que calcula algo e guarda em 'dados'
dados_acoes = {}

for ticker, info in setores_yfinance.items():
    setor = info["Setor"]
    empresa = info["Empresa"]
    
    try:
        print(f"Baixando dados para {ticker} - Setor: {setor}")
        df = yf.download(ticker, start=start, end=end, interval="1d", auto_adjust=True, progress=False, threads=False)
        stock = yf.Ticker(ticker)
        info_yf = stock.info
        volume_medio = info_yf.get('averageVolume', 0)
        preco_atual = info_yf.get('currentPrice', 0)

        if volume_medio >= volume_minimo and preco_atual >= preco_minimo:
            #print('Seleção OK')
            # dataframe para armazenar os dados 
            df_Gap = df.copy()
            data  = df.copy()
            df_topo_Fundo = df.copy()
            df_balanco = df.copy()
            dados = df[df.index >= um_ano_atras][['Close']]
            df_atr = df.copy()
            df_relev_gap = df.copy()
            #########################################################################################################
            # Tendência de baixa nos últimos 200 dias
            ####################################################################################################
            # Exibir as primeiras linhas do DataFrame   
            df = df.drop(columns=['Volume', 'Open', 'High', 'Low'])
            # Calcula MM200
            df["MM200"] = df["Close"].rolling(window=200).mean()
            # Remove as linhas que têm NaN em 'Close' ou 'MM200'
            df_valid = df[["Close", "MM200"]].dropna()
            # Agora as duas colunas estão perfeitamente alinhadas
            dias_abaixo = ((df_valid["Close"].values.ravel()) < (df_valid["MM200"].values.ravel())).sum()
            # Calcula a porcentagem de dias abaixo da MM20
            total_dias = len(df_valid)
            porcentagem = dias_abaixo / total_dias
            # Exibe resultado
            resultado = 1 if porcentagem > 0.7 else 0
            
            #########################################################################################################
            # Verificar Sem gap relevante de alta nos últimos 7 dias
            #########################################################################################################
            # Exibir as primeiras linhas do DataFrame   
            df_Gap = df_Gap.drop(columns=['Volume', 'High', 'Low'])
            df_Gap['prev_close'] = df_Gap['Close'].shift(1)
            df_Gap = df_Gap.drop(df_Gap.index[[0]]).reset_index(drop=True)
            # Calcula MM200
            df_Gap.columns = ['Close', 'Open', 'prev_close']
            df_Gap['gap_percent'] = (df_Gap['Open'] - df_Gap['prev_close']) / df_Gap['prev_close'] * 100
            # Remove as linhas que têm NaN em 'Close' ou 'MM200'
            ultimos_7_dias = df_Gap.tail(7)
        
            # Verifica se teve gap relevante (> 2%)
            houve_gap_relevante = (ultimos_7_dias['gap_percent'] > 2).any()
            gap_resultado = 0 if houve_gap_relevante else 1

            #########################################################################################################
            # Verificar se houve rompimento de resistência nos últimos 30 dias
            #########################################################################################################
            data.columns = ['Close', 'High', 'Low', 'Open', 'Volume']
            # Criando resistência: máximo dos 20 dias anteriores (excluindo o dia atual)
            data[('resistencia_20d')] = data[('High')].shift(1).rolling(window=20).max()

            # Seleciona os últimos 20 dias do DataFrame
            ultimos_20_dias = data.tail(20)

            houve_rompimento = False

            for data_atual in ultimos_20_dias.index:
                preco_maximo = data.loc[data_atual, ('High')]
                resistencia = data.loc[data_atual, ('resistencia_20d')]

                if pd.notna(resistencia) and preco_maximo > resistencia:
                    houve_rompimento = True
                    break  # já encontrou um rompimento, pode parar

            if houve_rompimento:
                rompimento_resultado = 0
            else:
                rompimento_resultado = 1

            #########################################################################################################
            # Verificar se houve Topos e fundos descendentes visíveis nos ultimos 3 topos e fundos
            #########################################################################################################
            df_topo_Fundo.columns = ['Close', 'High', 'Low', 'Open', 'Volume']
            


            # Detectar topos e fundos locais
            n = 5  # número de candles para definir o "extremo local"
            df_topo_Fundo['topos'] = df_topo_Fundo['Close'].iloc[argrelextrema(df_topo_Fundo['Close'].values, np.greater_equal, order=n)[0]]
            df_topo_Fundo['fundos'] = df_topo_Fundo['Close'].iloc[argrelextrema(df_topo_Fundo['Close'].values, np.less_equal, order=n)[0]]

            # Remover NaNs para análise
            topos = df_topo_Fundo.dropna(subset=['topos'])
            fundos = df_topo_Fundo.dropna(subset=['fundos'])

            # Verificar se os últimos topos e fundos estão em sequência descendente
            def is_descending(series):
                return all(x > y for x, y in zip(series, series[1:]))

            # Últimos 3 topos e fundos (pode ajustar)
            ultimos_topos = topos['topos'].tail(3).values
            ultimos_fundos = fundos['fundos'].tail(3).values


            if is_descending(ultimos_topos) and is_descending(ultimos_fundos):
                topofundo_resultado = 1
                #print("O ativo está em tendência de baixa (topos e fundos descendentes).")
            else:
                topofundo_resultado = 0
                #print("O ativo não está em tendência de baixa.")

        #########################################################################################################
            # Últimos 3 balanços foram mal recebidos 
            #########################################################################################################
            
            # Obtemos as datas de earnings
            datas = stock.earnings_dates
            datas = datas.dropna()  # Remove linhas com valores ausentes
            # Pegamos as datas disponíveis (índice do DataFrame)
            datas_balanco = datas.index.to_list()
            #print("Datas de balanço disponíveis:", datas_balanco)
            # Exibindo as 5 primeiras
            balanco_datas = []
            for data in datas_balanco:
                #print(data.strftime('%d/%m/%Y'))
                
                balanco_datas.append(data.strftime('%d/%m/%Y'))
            balanco_datas = balanco_datas[:3]  # Exibe apenas as últimas 3 datas
            #print("Lista de datas formatadas:", balanco_datas)

            # Passo 3: Baixar dados de preço para +1 dia após cada balanço
            #df_balanco = yf.download(item, start=start, end=end, interval="1d", auto_adjust=True, progress=False)
            df_balanco.columns = ['Close', 'High', 'Low', 'Open', 'Volume']

            # Passo 4: Analisar impacto do balanço
            impacto_total = 0  # Pode ser um contador ou uma pontuação

            for data in balanco_datas:
                data = pd.to_datetime(data, format='%d/%m/%Y')
                
                try:
                    preco_antes = df_balanco.loc[df_balanco.index < data].iloc[-1]['Close']
                    preco_depois = df_balanco.loc[df_balanco.index > data].iloc[0]['Close']
                    retorno = (preco_depois - preco_antes) / preco_antes * 100
                    status = "NEGATIVO" if retorno < -2 else "NEUTRO/POSITIVO"
                    
                    # Incrementa a variável de acordo com o resultado
                    if status == "NEGATIVO":
                        balanco_resultado = 1  # ou impacto_total += 1, dependendo da lógica desejada
                    else:
                        balanco_resultado = 0

                    #print(f"Balanço em {data.date()}: Retorno = {retorno:.2f}% → {status}")
                except Exception as e:
                    print(f"Erro ao processar a data {data.date()}: {e}")

            #print(f"\nResultado acumulado de impacto: {balanco_resultado}")
            #########################################################################################################
            # Setor fragilizado recentemente
            #########################################################################################################
            # Etapa 1: Obter setor
        
            dados.columns = ['Close']
        

            # Etapa 3: Calcular retorno acumulado do ativo
            retorno_pct = (dados.iloc[-1, 0] / dados.iloc[0, 0] - 1) * 100 if not dados.empty else None

            # Etapa 4: Comparar com outros ativos do mesmo setor
            # Lista representativa do setor financeiro brasileiro
            df_energy =   [t for t, s in setores_yfinance.items() if s["Setor"] == setor]
            setor_financeiro = df_energy
            #print(setor_financeiro)
            try:
                
                dados_setor = yf.download(setor_financeiro, start=start2, end=end, interval="1d", auto_adjust=True, progress=False, threads=False)['Close']
                if dados_setor.empty:
                    print(f"Sem dados para {ticker}")
                    continue
                dados_acoes[ticker] = df  # guarda o dataframe no dicionário
            except Exception as e:
                msg = str(e)
                if "timezone" in msg.lower() or "delisted" in msg.lower():
                    print(f"Erro conhecido para {ticker}: possivelmente deslistada ou problema de timezone.")
                else:
                    print(f"Erro inesperado para {ticker}: {e}")
            #dados_setor = yf.download(setor_financeiro, start=start2, end=end, interval="1d", auto_adjust=True, progress=False)['Close']

            #print(dados_setor)

            if dados_setor.empty:
                print(f"Dados do setor '{setor}' estão vazios.")
            else:
                retornos_setor = (dados_setor.iloc[-1] / dados_setor.iloc[0] - 1) * 100

                retorno_medio_setor = retornos_setor.mean(axis=0)

            # Etapa 5: Avaliar fragilidade
            setor_fragilizado = retorno_medio_setor < 0
            nota_setor = 1 if setor_fragilizado else 0

            #########################################################################################################
            # adciona os resultados na lista
            #########################################################################################################
            # Inicializa a variável
            eps_resultado = 0

            # Obter datas de earnings
            df_eps = stock.earnings_dates

            # Filtrar apenas colunas relevantes e remover valores ausentes
            df_eps = df_eps[['EPS Estimate', 'Reported EPS']].dropna()
        

            # Calcular a surpresa (diferença entre o reportado e o estimado)
            df_eps['Surpresa'] = df_eps['Reported EPS'] - df_eps['EPS Estimate']
        

            # Verificar se houve revisão negativa
            df_eps['Revisao_Negativa'] = df_eps['Surpresa'] < 0

            # Verificar se as 3 últimas revisões foram negativas
            if df_eps['Revisao_Negativa'].head(3).all():
                eps_resultado = 1
                
            else:
                eps_resultado = 0
                
            #########################################################################################################
            # Short float acima de 10%
            #########################################################################################################

            # Tenta pegar diretamente
            info = stock.info
            short_float =  info.get("shortPercentFloat", None)

            # Se não vier, tenta estimar
            if short_float is None:
                short_shares = info.get("sharesShort", None)
                float_shares = info.get("floatShares", None)
                if short_shares and float_shares:
                    short_float = short_shares / float_shares

            if short_float is not None:
                short_pct = short_float * 100
                #print(f"Short float de {ticker}: {short_pct:.2f}%")
                nota_short = 1 if short_pct > 10 else 0
            else:
                print(f"Short float de {ticker} não disponível.")
                nota_short = 0

            #print(f"Nota short: {nota_short}")
            #########################################################################################################
            # ATR atual acima da média dos 3 últimos meses
            #########################################################################################################
            # Calcular True Range (TR)
            df_atr['H-L'] = df_atr['High'] - df_atr['Low']
            df_atr['H-PC'] = abs(df_atr['High'] - df_atr['Close'].shift(1))
            df_atr['L-PC'] = abs(df_atr['Low'] - df_atr['Close'].shift(1))
            df_atr['TR'] = df_atr[['H-L', 'H-PC', 'L-PC']].max(axis=1)

            # Calcular ATR padrão (14 dias)
            df_atr['ATR14'] = df_atr['TR'].rolling(window=14).mean()

            # Ponto atual (último valor conhecido)
            atr_atual = df_atr['ATR14'].iloc[-1]

            # Média dos últimos 3 meses (~63 pregões)
            media_3m = df_atr['ATR14'].tail(63).mean()

            #print(f"ATR atual: {atr_atual:.2f}")
            #print(f"Média dos últimos 3 meses: {media_3m:.2f}")

            # Avaliação
            nota_volatilidade = 0 if atr_atual > media_3m else 1
            #print(f"Nota volatilidade: {nota_volatilidade}")

            #########################################################################################################
            # Histórico mostra gaps relevantes
            #########################################################################################################
            df_relev_gap = df_relev_gap.tail(365)  # Considera o histórico dos últimos 365 dias
            # Corrigir MultiIndex: remover o segundo nível 
            df_relev_gap.columns = df_relev_gap.columns.droplevel(1)

            # Calcular 'Close_prev' corretamente
            df_relev_gap['Close_prev'] = df_relev_gap['Close'].shift(1)

            # Calcular o gap percentual
            df_relev_gap['gap_perc'] = (df_relev_gap['Open'] - df_relev_gap['Close_prev']) / df_relev_gap['Close_prev'] * 100

            # Remover NaNs
            df_relev_gap = df_relev_gap.dropna(subset=['gap_perc'])

            # Filtrar gaps relevantes (> 10% para cima ou para baixo)
            limiar_gap = 10

            houve_gap_relevante = (abs(df_relev_gap['gap_perc']) > limiar_gap).any()

            # gap_resultado = 0 se teve gap relevante, 2 se não teve
            gap_resultado = 1 if houve_gap_relevante else 0

            #print(f"Houve gap relevante: {houve_gap_relevante}")
            # print(f"Resultado do gap: {gap_resultado}")
            #########################################################################################################
            # data do  Proximo balanço
            #########################################################################################################
            calendar = stock.calendar

            # Captura a próxima data de earnings
            earnings_date = calendar.get("Earnings Date", None)
            if isinstance(earnings_date, (list, tuple)):
                earnings_date = earnings_date[0]

            # Converte para datetime
            earnings_date = pd.to_datetime(earnings_date)
            data_entrada = earnings_date - pd.offsets.BDay(3)

            

    
           
            #print("📅 Próxima data de balanço:", earnings_date.date())
            #print("📆 4 dias úteis antes:", data_entrada.date())

             #########################################################################################################
            # Ativo Metatrader 5
            #########################################################################################################
            
            exchange_code = stock.info.get("exchange")
            exchange_name = exchange_map.get(exchange_code, None)
            metatrader = f"{ticker}.{exchange_name}"
           
            #print(f"MetaTrader: {metatrader}")
        
            #########################################################################################################
            # adciona os resultados na lista
            #########################################################################################################
            liquidez=1
            preco_acao = 1
            Lista_oficial.append({
                'Ativo': ticker,
                'Ativo Meta': metatrader,
                'Empresa': empresa,
                'Tendencia 200 dias': resultado,
                'Gap Relevante 7 dias': gap_resultado , 
                'Rompimento 20 dias': rompimento_resultado, 
                'Topos e Fundos': topofundo_resultado,
                'SP500 em baixa': sp500_resultado,
                '3 Balanço negativo': balanco_resultado, 
                'Setor Fragilizado': nota_setor,
                'negativas de lucro (EPS)': eps_resultado, 
                'Short Float 10': nota_short,
                'Liquidez minima': liquidez,
                'Preço atual': preco_acao,
                'ATR acima da média 3 meses': nota_volatilidade,
                'Histórico com gaps relevantes': gap_resultado,
                'próxima entrada':  data_entrada.date(),
                'proximo Balanco':  earnings_date.date(),
                })
            
    
    except Exception as e:
        print(f"Erro ao processar {ticker}: {e}")
 
# Criar o DataFrame
Lista_oficial = pd.DataFrame(Lista_oficial)
#tirar linhas none e nan
Lista_oficial = Lista_oficial.dropna()

Lista_ordenada = Lista_oficial
print(Lista_ordenada)

Lista_ordenada.to_csv("analise_acoes.csv", index=False, encoding='utf-8-sig')


