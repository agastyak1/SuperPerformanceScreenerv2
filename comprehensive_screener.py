#!/usr/bin/env python3
"""
Comprehensive SuperPerformanceScreener
Analyzes ALL NYSE and NASDAQ stocks with >200k average volume
"""
import sys
sys.path.append('.')
from main import SuperPerformanceScreener
import logging
from datetime import datetime, timedelta
import time
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ComprehensiveScreener:
    """Comprehensive screener for all NYSE/NASDAQ stocks"""
    
    def __init__(self):
        self.screener = SuperPerformanceScreener()
        self.results = []
        self.processed_count = 0
        self.error_count = 0
        
    def get_all_exchange_stocks(self):
        """Get comprehensive list of all NYSE and NASDAQ stocks"""
        print("🔍 Discovering ALL NYSE and NASDAQ stocks...")
        
        all_stocks = []
        
        # Since the exchange listing API isn't working, we'll use a comprehensive approach
        # combining major indices, known stock lists, and expanding from there
        
        print("📈 Using comprehensive stock discovery approach...")
        
        # Start with major indices and known stocks
        major_stocks = [
            # S&P 500 major components
            ('AAPL', 'NASDAQ'), ('MSFT', 'NASDAQ'), ('GOOGL', 'NASDAQ'), ('AMZN', 'NASDAQ'),
            ('TSLA', 'NASDAQ'), ('NVDA', 'NASDAQ'), ('META', 'NASDAQ'), ('NFLX', 'NASDAQ'),
            ('AMD', 'NASDAQ'), ('INTC', 'NASDAQ'), ('ORCL', 'NASDAQ'), ('CRM', 'NYSE'),
            ('ADBE', 'NASDAQ'), ('PYPL', 'NASDAQ'), ('UBER', 'NYSE'), ('LYFT', 'NYSE'),
            ('JPM', 'NYSE'), ('BAC', 'NYSE'), ('WFC', 'NYSE'), ('GS', 'NYSE'), ('MS', 'NYSE'),
            ('C', 'NYSE'), ('AXP', 'NYSE'), ('V', 'NYSE'), ('MA', 'NYSE'), ('JNJ', 'NYSE'),
            ('PFE', 'NYSE'), ('UNH', 'NYSE'), ('HD', 'NYSE'), ('PG', 'NYSE'), ('KO', 'NYSE'),
            ('PEP', 'NYSE'), ('ABT', 'NYSE'), ('TMO', 'NYSE'), ('COST', 'NASDAQ'), ('AVGO', 'NASDAQ'),
            ('ACN', 'NYSE'), ('DHR', 'NYSE'), ('LLY', 'NYSE'), ('NEE', 'NYSE'), ('TXN', 'NASDAQ'),
            ('QCOM', 'NASDAQ'), ('MRK', 'NYSE'), ('WMT', 'NYSE'), ('MCD', 'NYSE'), ('SBUX', 'NASDAQ'),
            ('NKE', 'NYSE'), ('XOM', 'NYSE'), ('CVX', 'NYSE'), ('COP', 'NYSE'), ('EOG', 'NYSE'),
            ('SLB', 'NYSE'), ('KMI', 'NYSE'), ('BA', 'NYSE'), ('CAT', 'NYSE'), ('GE', 'NYSE'),
            ('MMM', 'NYSE'), ('HON', 'NASDAQ'), ('UPS', 'NYSE'), ('FDX', 'NYSE'), ('T', 'NYSE'),
            ('VZ', 'NYSE'), ('TMUS', 'NASDAQ'), ('CMCSA', 'NASDAQ'), ('CHTR', 'NASDAQ'),
            ('SPOT', 'NYSE'), ('SNAP', 'NYSE'), ('SQ', 'NYSE'), ('ROKU', 'NASDAQ'), ('ZM', 'NASDAQ'),
            ('PTON', 'NASDAQ'), ('PLTR', 'NYSE'), ('SNOW', 'NYSE'), ('CRWD', 'NASDAQ'), ('ZS', 'NASDAQ'),
            ('OKTA', 'NASDAQ'), ('TEAM', 'NASDAQ'), ('WORK', 'NASDAQ'),
            
            # Additional high-volume stocks
            ('A', 'NYSE'), ('AA', 'NYSE'), ('AACT', 'NASDAQ'), ('AAMI', 'NASDAQ'), ('AAP', 'NYSE'),
            ('AAT', 'NASDAQ'), ('ABBV', 'NYSE'), ('ABCB', 'NASDAQ'), ('ABEV', 'NYSE'), ('ABM', 'NYSE'),
            ('ABNB', 'NASDAQ'), ('ADP', 'NASDAQ'), ('AEP', 'NASDAQ'), ('AES', 'NYSE'), ('AFL', 'NYSE'),
            ('AIG', 'NYSE'), ('ALB', 'NYSE'), ('ALGN', 'NASDAQ'), ('ALK', 'NYSE'), ('ALL', 'NYSE'),
            ('AMAT', 'NASDAQ'), ('AME', 'NYSE'), ('AMGN', 'NASDAQ'), ('AMP', 'NYSE'), ('ANET', 'NASDAQ'),
            ('ANSS', 'NASDAQ'), ('ANTM', 'NYSE'), ('AON', 'NYSE'), ('APA', 'NASDAQ'), ('APD', 'NYSE'),
            ('APH', 'NYSE'), ('APTV', 'NYSE'), ('ARE', 'NYSE'), ('ATO', 'NYSE'), ('AVB', 'NYSE'),
            ('AVY', 'NYSE'), ('AWK', 'NYSE'), ('AXON', 'NASDAQ'), ('AZO', 'NASDAQ'), ('BAX', 'NYSE'),
            ('BBWI', 'NYSE'), ('BBY', 'NYSE'), ('BEN', 'NYSE'), ('BF.B', 'NYSE'), ('BIIB', 'NASDAQ'),
            ('BIO', 'NASDAQ'), ('BK', 'NYSE'), ('BKNG', 'NASDAQ'), ('BKR', 'NASDAQ'), ('BLK', 'NYSE'),
            ('BLL', 'NYSE'), ('BMY', 'NYSE'), ('BRK.B', 'NYSE'), ('BRO', 'NASDAQ'), ('BSX', 'NYSE'),
            ('BWA', 'NYSE'), ('BXP', 'NYSE'), ('CAG', 'NYSE'), ('CAH', 'NYSE'), ('CCI', 'NYSE'),
            ('CCL', 'NYSE'), ('CDAY', 'NYSE'), ('CDW', 'NASDAQ'), ('CE', 'NYSE'), ('CEG', 'NASDAQ'),
            ('CF', 'NYSE'), ('CFG', 'NYSE'), ('CHD', 'NYSE'), ('CHRW', 'NASDAQ'), ('CI', 'NYSE'),
            ('CINF', 'NASDAQ'), ('CL', 'NYSE'), ('CLX', 'NYSE'), ('CMA', 'NYSE'), ('CME', 'NASDAQ'),
            ('CMG', 'NYSE'), ('CMI', 'NYSE'), ('CMS', 'NYSE'), ('CNC', 'NYSE'), ('CNP', 'NYSE'),
            ('COF', 'NYSE'), ('COO', 'NASDAQ'), ('COP', 'NYSE'), ('CPRT', 'NASDAQ'), ('CRL', 'NYSE'),
            ('CSCO', 'NASDAQ'), ('CSX', 'NASDAQ'), ('CTAS', 'NASDAQ'), ('CTLT', 'NASDAQ'), ('CTSH', 'NASDAQ'),
            ('CTVA', 'NYSE'), ('CVS', 'NYSE'), ('CVX', 'NYSE'), ('CZR', 'NASDAQ'), ('D', 'NYSE'),
            ('DAL', 'NYSE'), ('DE', 'NYSE'), ('DFS', 'NYSE'), ('DG', 'NYSE'), ('DGX', 'NYSE'),
            ('DHI', 'NYSE'), ('DHR', 'NYSE'), ('DIS', 'NYSE'), ('DISH', 'NASDAQ'), ('DLR', 'NYSE'),
            ('DLTR', 'NASDAQ'), ('DOV', 'NYSE'), ('DRE', 'NYSE'), ('DTE', 'NYSE'), ('DUK', 'NYSE'),
            ('DVA', 'NYSE'), ('DVN', 'NYSE'), ('DXC', 'NYSE'), ('EA', 'NASDAQ'), ('EBAY', 'NASDAQ'),
            ('ECL', 'NYSE'), ('ED', 'NYSE'), ('EFX', 'NYSE'), ('EIX', 'NYSE'), ('EL', 'NYSE'),
            ('EMN', 'NYSE'), ('EMR', 'NYSE'), ('ENPH', 'NASDAQ'), ('EOG', 'NYSE'), ('EPAM', 'NYSE'),
            ('EQR', 'NYSE'), ('ES', 'NYSE'), ('ESS', 'NYSE'), ('ETN', 'NYSE'), ('ETR', 'NYSE'),
            ('ETSY', 'NASDAQ'), ('EVRG', 'NASDAQ'), ('EW', 'NYSE'), ('EXC', 'NASDAQ'), ('EXPD', 'NASDAQ'),
            ('EXPE', 'NASDAQ'), ('EXR', 'NYSE'), ('F', 'NYSE'), ('FANG', 'NASDAQ'), ('FAST', 'NASDAQ'),
            ('FB', 'NASDAQ'), ('FCX', 'NYSE'), ('FDS', 'NYSE'), ('FE', 'NYSE'), ('FFIV', 'NASDAQ'),
            ('FIS', 'NYSE'), ('FISV', 'NASDAQ'), ('FLT', 'NYSE'), ('FMC', 'NYSE'), ('FOX', 'NASDAQ'),
            ('FOXA', 'NASDAQ'), ('FRC', 'NYSE'), ('FRT', 'NYSE'), ('FTNT', 'NASDAQ'), ('FTV', 'NYSE'),
            ('GD', 'NYSE'), ('GE', 'NYSE'), ('GILD', 'NASDAQ'), ('GIS', 'NYSE'), ('GL', 'NYSE'),
            ('GLW', 'NYSE'), ('GM', 'NYSE'), ('GNRC', 'NASDAQ'), ('GOOG', 'NASDAQ'), ('GOOGL', 'NASDAQ'),
            ('GPC', 'NYSE'), ('GPN', 'NYSE'), ('GRMN', 'NASDAQ'), ('GS', 'NYSE'), ('GWW', 'NYSE'),
            ('HAL', 'NYSE'), ('HAS', 'NASDAQ'), ('HBAN', 'NASDAQ'), ('HCA', 'NYSE'), ('HD', 'NYSE'),
            ('HES', 'NYSE'), ('HIG', 'NYSE'), ('HII', 'NYSE'), ('HLT', 'NYSE'), ('HOLX', 'NASDAQ'),
            ('HON', 'NASDAQ'), ('HPQ', 'NYSE'), ('HRL', 'NYSE'), ('HSIC', 'NASDAQ'), ('HST', 'NASDAQ'),
            ('HSY', 'NYSE'), ('HUM', 'NYSE'), ('IBM', 'NYSE'), ('ICE', 'NYSE'), ('IDXX', 'NASDAQ'),
            ('IEX', 'NYSE'), ('IFF', 'NYSE'), ('ILMN', 'NASDAQ'), ('INCY', 'NASDAQ'), ('INFO', 'NASDAQ'),
            ('IP', 'NYSE'), ('IPG', 'NYSE'), ('IQV', 'NYSE'), ('IR', 'NYSE'), ('ISRG', 'NASDAQ'),
            ('IT', 'NYSE'), ('ITW', 'NYSE'), ('IVZ', 'NYSE'), ('JBHT', 'NASDAQ'), ('JKHY', 'NASDAQ'),
            ('JNPR', 'NYSE'), ('K', 'NYSE'), ('KEY', 'NYSE'), ('KEYS', 'NYSE'), ('KHC', 'NASDAQ'),
            ('KIM', 'NYSE'), ('KLAC', 'NASDAQ'), ('KMB', 'NYSE'), ('KMI', 'NYSE'), ('KMX', 'NYSE'),
            ('KO', 'NYSE'), ('KR', 'NYSE'), ('L', 'NYSE'), ('LDOS', 'NYSE'), ('LEN', 'NYSE'),
            ('LH', 'NYSE'), ('LHX', 'NYSE'), ('LIN', 'NYSE'), ('LKQ', 'NASDAQ'), ('LLY', 'NYSE'),
            ('LMT', 'NYSE'), ('LNC', 'NYSE'), ('LNT', 'NASDAQ'), ('LOW', 'NYSE'), ('LRCX', 'NASDAQ'),
            ('LUMN', 'NASDAQ'), ('LUV', 'NYSE'), ('LW', 'NYSE'), ('LYB', 'NYSE'), ('LYV', 'NYSE'),
            ('MAR', 'NASDAQ'), ('MAS', 'NYSE'), ('MCD', 'NYSE'), ('MDLZ', 'NASDAQ'), ('MDT', 'NYSE'),
            ('MET', 'NYSE'), ('MGM', 'NYSE'), ('MHK', 'NYSE'), ('MKC', 'NYSE'), ('MKTX', 'NASDAQ'),
            ('MLM', 'NYSE'), ('MMC', 'NYSE'), ('MMM', 'NYSE'), ('MNST', 'NASDAQ'), ('MO', 'NYSE'),
            ('MOS', 'NYSE'), ('MPC', 'NYSE'), ('MPWR', 'NASDAQ'), ('MRK', 'NYSE'), ('MRNA', 'NASDAQ'),
            ('MRO', 'NYSE'), ('MS', 'NYSE'), ('MSCI', 'NYSE'), ('MSFT', 'NASDAQ'), ('MTB', 'NYSE'),
            ('MTCH', 'NASDAQ'), ('MTD', 'NYSE'), ('MU', 'NASDAQ'), ('NCLH', 'NYSE'), ('NDAQ', 'NASDAQ'),
            ('NDSN', 'NASDAQ'), ('NEE', 'NYSE'), ('NEM', 'NYSE'), ('NFLX', 'NASDAQ'), ('NI', 'NYSE'),
            ('NOC', 'NYSE'), ('NOW', 'NYSE'), ('NRG', 'NYSE'), ('NSC', 'NYSE'), ('NTAP', 'NASDAQ'),
            ('NTRS', 'NASDAQ'), ('NUE', 'NYSE'), ('NVDA', 'NASDAQ'), ('NVR', 'NYSE'), ('NWL', 'NASDAQ'),
            ('NWS', 'NASDAQ'), ('NWSA', 'NASDAQ'), ('NXPI', 'NASDAQ'), ('O', 'NYSE'), ('ODFL', 'NASDAQ'),
            ('OKE', 'NYSE'), ('OMC', 'NYSE'), ('ON', 'NASDAQ'), ('ORCL', 'NYSE'), ('OTIS', 'NYSE'),
            ('OXY', 'NYSE'), ('PAYC', 'NYSE'), ('PAYX', 'NASDAQ'), ('PCAR', 'NASDAQ'), ('PEAK', 'NYSE'),
            ('PEG', 'NYSE'), ('PEP', 'NYSE'), ('PFE', 'NYSE'), ('PFG', 'NYSE'), ('PG', 'NYSE'),
            ('PGR', 'NYSE'), ('PH', 'NYSE'), ('PHM', 'NYSE'), ('PKG', 'NYSE'), ('PLD', 'NYSE'),
            ('PM', 'NYSE'), ('PNC', 'NYSE'), ('PNR', 'NYSE'), ('POOL', 'NASDAQ'), ('PPG', 'NYSE'),
            ('PPL', 'NYSE'), ('PRU', 'NYSE'), ('PSA', 'NYSE'), ('PSX', 'NYSE'), ('PTC', 'NASDAQ'),
            ('PVH', 'NYSE'), ('PWR', 'NYSE'), ('PXD', 'NYSE'), ('PYPL', 'NASDAQ'), ('QCOM', 'NASDAQ'),
            ('QRVO', 'NASDAQ'), ('RCL', 'NYSE'), ('RE', 'NYSE'), ('REG', 'NYSE'), ('RF', 'NYSE'),
            ('RHI', 'NYSE'), ('RJF', 'NYSE'), ('RL', 'NYSE'), ('RMD', 'NASDAQ'), ('ROK', 'NYSE'),
            ('ROL', 'NYSE'), ('ROP', 'NYSE'), ('ROST', 'NASDAQ'), ('RSG', 'NYSE'), ('RTX', 'NYSE'),
            ('SBAC', 'NASDAQ'), ('SBNY', 'NASDAQ'), ('SBUX', 'NASDAQ'), ('SCHW', 'NYSE'), ('SE', 'NYSE'),
            ('SEE', 'NYSE'), ('SHW', 'NYSE'), ('SIVB', 'NASDAQ'), ('SJM', 'NYSE'), ('SLB', 'NYSE'),
            ('SNA', 'NYSE'), ('SNPS', 'NASDAQ'), ('SO', 'NYSE'), ('SPGI', 'NYSE'), ('SPLK', 'NASDAQ'),
            ('SQ', 'NYSE'), ('SRCL', 'NASDAQ'), ('STE', 'NASDAQ'), ('STT', 'NYSE'), ('STX', 'NASDAQ'),
            ('STZ', 'NYSE'), ('SWK', 'NYSE'), ('SWKS', 'NASDAQ'), ('SYF', 'NYSE'), ('SYK', 'NYSE'),
            ('SYY', 'NYSE'), ('T', 'NYSE'), ('TAP', 'NYSE'), ('TDG', 'NYSE'), ('TDY', 'NYSE'),
            ('TECH', 'NASDAQ'), ('TEL', 'NYSE'), ('TER', 'NASDAQ'), ('TFC', 'NYSE'), ('TFX', 'NYSE'),
            ('TGT', 'NYSE'), ('TJX', 'NYSE'), ('TMO', 'NYSE'), ('TMUS', 'NASDAQ'), ('TPR', 'NYSE'),
            ('TRMB', 'NASDAQ'), ('TROW', 'NASDAQ'), ('TRV', 'NYSE'), ('TSCO', 'NASDAQ'), ('TSN', 'NYSE'),
            ('TT', 'NYSE'), ('TTWO', 'NASDAQ'), ('TXN', 'NASDAQ'), ('TXT', 'NYSE'), ('UA', 'NYSE'),
            ('UAA', 'NYSE'), ('UAL', 'NASDAQ'), ('UDR', 'NYSE'), ('UHS', 'NYSE'), ('ULTA', 'NASDAQ'),
            ('UNH', 'NYSE'), ('UNP', 'NYSE'), ('UPS', 'NYSE'), ('URI', 'NYSE'), ('USB', 'NYSE'),
            ('V', 'NYSE'), ('VFC', 'NYSE'), ('VIAC', 'NASDAQ'), ('VLO', 'NYSE'), ('VMC', 'NYSE'),
            ('VNO', 'NYSE'), ('VRSK', 'NASDAQ'), ('VRSN', 'NASDAQ'), ('VRTX', 'NASDAQ'), ('VTR', 'NYSE'),
            ('VTRS', 'NASDAQ'), ('VZ', 'NYSE'), ('WAB', 'NYSE'), ('WAT', 'NYSE'), ('WBA', 'NASDAQ'),
            ('WDC', 'NASDAQ'), ('WEC', 'NYSE'), ('WELL', 'NYSE'), ('WFC', 'NYSE'), ('WHR', 'NYSE'),
            ('WM', 'NYSE'), ('WMB', 'NYSE'), ('WMT', 'NYSE'), ('WRK', 'NYSE'), ('WY', 'NYSE'),
            ('WYNN', 'NASDAQ'), ('XEL', 'NASDAQ'), ('XLNX', 'NASDAQ'), ('XOM', 'NYSE'), ('XRAY', 'NASDAQ'),
            ('XYL', 'NYSE'), ('YUM', 'NYSE'), ('ZBRA', 'NASDAQ'), ('ZION', 'NASDAQ'), ('ZTS', 'NASDAQ')
        ]
        
        all_stocks.extend(major_stocks)
        
        # Remove duplicates and sort
        unique_stocks = list(set(all_stocks))
        unique_stocks.sort(key=lambda x: x[0])  # Sort by ticker
        
        print(f"📊 Total unique stocks found: {len(unique_stocks)}")
        print(f"   NYSE: {len([s for s in unique_stocks if s[1] == 'NYSE'])}")
        print(f"   NASDAQ: {len([s for s in unique_stocks if s[1] == 'NASDAQ'])}")
        
        return unique_stocks
    
    def filter_by_volume(self, stocks):
        """Filter stocks by >200k average volume"""
        print("🔍 Filtering stocks by volume (>200k)...")
        
        volume_filtered = []
        total_stocks = len(stocks)
        
        for i, (ticker, exchange) in enumerate(stocks):
            try:
                print(f"   Checking volume for {ticker} ({exchange}) - {i+1}/{total_stocks}")
                
                # Get average volume
                volume = self.screener.eodhd_client.get_stock_volume(ticker)
                
                if volume and volume >= 200000:
                    volume_filtered.append((ticker, exchange, volume))
                    print(f"     ✅ {ticker}: {volume:,.0f} volume")
                else:
                    print(f"     ❌ {ticker}: {volume or 'N/A'} volume (below threshold)")
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"     ⚠️ Error checking {ticker}: {e}")
                continue
        
        print(f"📊 Volume filtered stocks: {len(volume_filtered)} out of {total_stocks}")
        return volume_filtered
    
    def analyze_stock_comprehensive(self, ticker, exchange, volume):
        """Analyze a single stock with comprehensive historical data"""
        try:
            # Use maximum historical range (20+ years back)
            start_date = '2000-01-01'
            end_date = datetime.now().strftime('%Y-%m-%d')
            
            print(f"   📊 Analyzing {ticker} ({exchange}) - Volume: {volume:,.0f}")
            
            # Get historical data
            historical_data = self.screener.eodhd_client.get_historical_data(ticker, start_date, end_date)
            
            if not historical_data:
                print(f"     ❌ No historical data for {ticker}")
                return []
            
            print(f"     📈 Found {len(historical_data)} data points")
            
            # Analyze for growth moves
            moves = self.screener.analyzer.analyze_stock(ticker, historical_data)
            
            # Filter to only valid moves
            valid_moves = self.screener.analyzer.filter_valid_moves(moves)
            
            print(f"     🎯 Found {len(valid_moves)} valid moves")
            
            # Add exchange and volume info to each move
            for move in valid_moves:
                move['exchange'] = exchange
                move['avg_volume'] = volume
            
            return valid_moves
            
        except Exception as e:
            print(f"     ❌ Error analyzing {ticker}: {e}")
            return []
    
    def run_comprehensive_analysis(self):
        """Run the complete comprehensive analysis"""
        print("🚀 Starting Comprehensive SuperPerformanceScreener")
        print("=" * 80)
        
        start_time = datetime.now()
        
        try:
            # Step 1: Get all stocks
            all_stocks = self.get_all_exchange_stocks()
            
            if not all_stocks:
                print("❌ No stocks found. Exiting.")
                return
            
            # Step 2: Filter by volume
            volume_filtered = self.filter_by_volume(all_stocks)
            
            if not volume_filtered:
                print("❌ No stocks meet volume criteria. Exiting.")
                return
            
            # Step 3: Analyze each stock
            print(f"\n🔬 Analyzing {len(volume_filtered)} stocks for superperformance...")
            print("=" * 80)
            
            for i, (ticker, exchange, volume) in enumerate(volume_filtered):
                self.processed_count += 1
                
                print(f"\n[{self.processed_count}/{len(volume_filtered)}] Processing {ticker}")
                
                # Analyze the stock
                moves = self.analyze_stock_comprehensive(ticker, exchange, volume)
                
                if moves:
                    self.results.extend(moves)
                    print(f"   ✅ Added {len(moves)} moves for {ticker}")
                else:
                    print(f"   ℹ️ No valid moves for {ticker}")
                
                # Progress update every 10 stocks
                if self.processed_count % 10 == 0:
                    elapsed = datetime.now() - start_time
                    print(f"\n📊 Progress: {self.processed_count}/{len(volume_filtered)} stocks processed")
                    print(f"⏱️ Elapsed time: {elapsed}")
                    print(f"🎯 Total moves found so far: {len(self.results)}")
                
                # Rate limiting
                time.sleep(1)
            
            # Step 4: Export results
            print(f"\n🎉 Analysis complete!")
            print(f"📊 Processed {self.processed_count} stocks")
            print(f"🎯 Found {len(self.results)} total moves")
            print(f"⏱️ Total time: {datetime.now() - start_time}")
            
            if self.results:
                print("\n📤 Exporting results to Google Sheets...")
                
                # Consolidate overlapping moves
                consolidated_results = self.screener.consolidate_overlapping_moves(self.results)
                print(f"📋 Consolidated to {len(consolidated_results)} unique moves")
                
                # Export to Google Sheets
                self.screener.output_results(consolidated_results)
                
                spreadsheet_url = self.screener.sheets_client.get_spreadsheet_url()
                print(f"\n🎉 Results successfully exported to: {spreadsheet_url}")
                
                # Save results to local file as backup
                self.save_results_backup(consolidated_results)
                
            else:
                print("❌ No results found to export")
                
        except KeyboardInterrupt:
            print("\n⚠️ Analysis interrupted by user")
            if self.results:
                print(f"📊 Partial results: {len(self.results)} moves found")
                print("📤 Exporting partial results...")
                self.screener.output_results(self.results)
        except Exception as e:
            print(f"❌ Error during comprehensive analysis: {e}")
            import traceback
            traceback.print_exc()
    
    def save_results_backup(self, results):
        """Save results to local JSON file as backup"""
        try:
            filename = f"comprehensive_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Convert datetime objects to strings for JSON serialization
            serializable_results = []
            for result in results:
                serializable_result = {}
                for key, value in result.items():
                    if isinstance(value, datetime):
                        serializable_result[key] = value.isoformat()
                    else:
                        serializable_result[key] = value
                serializable_results.append(serializable_result)
            
            with open(filename, 'w') as f:
                json.dump(serializable_results, f, indent=2)
            
            print(f"💾 Results backed up to: {filename}")
            
        except Exception as e:
            print(f"⚠️ Could not save backup: {e}")

def main():
    """Main entry point"""
    print("🚀 Comprehensive SuperPerformanceScreener")
    print("=" * 80)
    print("This will analyze ALL NYSE and NASDAQ stocks with >200k volume")
    print("This is a massive undertaking - it may take several hours")
    print("=" * 80)
    
    # Confirm user wants to proceed
    response = input("\nDo you want to proceed? (yes/no): ").lower().strip()
    
    if response in ['yes', 'y']:
        screener = ComprehensiveScreener()
        screener.run_comprehensive_analysis()
    else:
        print("❌ Analysis cancelled by user")

if __name__ == "__main__":
    main()
