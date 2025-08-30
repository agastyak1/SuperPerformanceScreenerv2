"""
Stock Analysis Engine for SuperPerformanceScreener
Implements the core logic for detecting growth moves, superperformance, and drawdowns
"""
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import logging

from config import (
    MIN_GROWTH_PERCENTAGE,
    MAX_DRAWDOWN_PERCENTAGE,
    MIN_DRAWDOWN_PERCENTAGE,
    GROWTH_MOVE_DAYS,
    MAX_DAYS_WITHOUT_HIGH,
    MAX_TOTAL_DAYS,
    CONTINUATION_WINDOW_DAYS,
    GROWTH_THRESHOLDS
)

logger = logging.getLogger(__name__)

class StockAnalyzer:
    """Core stock analysis engine"""
    
    def __init__(self):
        self.data_cache = {}
        # Set up debug logging for this class
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
    
    def format_date(self, date_str: str) -> str:
        """Format date as 'Month D, YYYY'"""
        try:
            if isinstance(date_str, str):
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            else:
                date_obj = date_str
            
            return date_obj.strftime('%b %d, %Y')
        except:
            return str(date_str)
    
    def calculate_percentage_change(self, start_price: float, end_price: float) -> float:
        """Calculate percentage change between two prices"""
        if start_price == 0:
            return 0.0
        return ((end_price - start_price) / start_price) * 100
    
    def find_lowest_of_day_candidates(self, data: List[Dict]) -> List[Dict]:
        """Find potential LOD (Lowest of Day) candidates"""
        candidates = []
        
        for i, day in enumerate(data):
            if i < len(data) - GROWTH_MOVE_DAYS:
                # Check if this day's low is the lowest in the next 5 days
                current_low = day['low']
                future_highs = [d['high'] for d in data[i+1:i+GROWTH_MOVE_DAYS+1]]
                
                # Check if we get 5% growth within 5 days
                max_future_price = max(future_highs)
                growth = self.calculate_percentage_change(current_low, max_future_price)
                
                if growth >= MIN_GROWTH_PERCENTAGE:
                    candidates.append({
                        'date': day['date'],
                        'low': current_low,
                        'growth': growth,
                        'index': i
                    })
        
        return candidates
    
    def detect_growth_move(self, data: List[Dict], start_index: int) -> Optional[Dict]:
        """
        Detect a growth move starting from a given LOD candidate
        
        Returns:
            Dict with move details or None if no valid move
        """
        if start_index >= len(data) - 1:
            return None
        
        start_data = data[start_index]
        start_date = start_data['date']
        lod_price = start_data['low']
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        
        peak_price = lod_price
        peak_date = start_date
        peak_index = start_index
        days_without_high = 0
        drawdowns = []
        continuation_occurred = False
        new_lod_after_drawdown = None
        
        # Track the move with improved logic
        move_terminated = False
        termination_reason = None
        
        self.logger.debug(f"Starting move analysis for {start_date} at LOD price {lod_price}")
        
        for i in range(start_index + 1, len(data)):
            current_data = data[i]
            current_date = current_data['date']
            current_high = current_data['high']
            current_low = current_data['low']
            current_close = current_data['close']
            
            current_datetime = datetime.strptime(current_date, '%Y-%m-%d')
            days_since_start = (current_datetime - start_datetime).days
            
            # Check if we've exceeded time limits
            if days_since_start > MAX_TOTAL_DAYS:
                move_terminated = True
                termination_reason = "Max total days exceeded"
                self.logger.debug(f"Move terminated: {termination_reason} at {current_date}")
                break
            
            # Update peak if we have a new high
            if current_high > peak_price:
                peak_price = current_high
                peak_date = current_date
                peak_index = i
                days_without_high = 0
                self.logger.debug(f"New peak: {peak_price} at {peak_date}")
            else:
                days_without_high += 1
            
            # Calculate current drawdown from peak
            current_drawdown = self.calculate_percentage_change(peak_price, current_close)
            
            # Check if price drops below LOD (this should terminate the move)
            if current_low < lod_price:
                move_terminated = True
                termination_reason = "Price dropped below LOD"
                self.logger.debug(f"Move terminated: {termination_reason} at {current_date} (low: {current_low}, LOD: {lod_price})")
                break
            
            # Check for drawdowns (15-29.9%) - FIX 2: Separate drawdown detection
            if MIN_DRAWDOWN_PERCENTAGE <= current_drawdown < MAX_DRAWDOWN_PERCENTAGE:
                # Check if this is a new drawdown or continuation of existing one
                if not drawdowns or (current_datetime - datetime.strptime(drawdowns[-1]['date'], '%Y-%m-%d')).days > 1:
                    drawdowns.append({
                        'date': current_date,
                        'drawdown': current_drawdown,
                        'price': current_close
                    })
                    self.logger.debug(f"Drawdown detected: {current_drawdown:.1f}% at {current_date}")
            
            # Check for continuation (recovery to new high within 90 days of peak) - FIX 3: Proper continuation detection
            if drawdowns and not continuation_occurred:
                peak_datetime = datetime.strptime(peak_date, '%Y-%m-%d')
                days_since_peak = (current_datetime - peak_datetime).days
                
                # Allow continuation if we recover to a new high within the continuation window
                if days_since_peak <= CONTINUATION_WINDOW_DAYS and current_high > peak_price:
                    continuation_occurred = True
                    # Find the lowest point during the drawdown
                    drawdown_prices = [d['price'] for d in drawdowns]
                    if drawdown_prices:
                        new_lod_after_drawdown = min(drawdown_prices)
                    self.logger.debug(f"Continuation detected: new high {current_high} > peak {peak_price} at {current_date}")
                
                # Also check for continuation if we're still within the window and showing recovery signs
                elif days_since_peak <= CONTINUATION_WINDOW_DAYS and current_drawdown < MIN_DRAWDOWN_PERCENTAGE:
                    # If we're recovering from a drawdown and still within the window, mark as potential continuation
                    if len(drawdowns) > 0:
                        last_drawdown = drawdowns[-1]
                        last_drawdown_datetime = datetime.strptime(last_drawdown['date'], '%Y-%m-%d')
                        days_since_last_drawdown = (current_datetime - last_drawdown_datetime).days
                        
                        # If we're showing recovery within 30 days of the last drawdown, consider it a continuation
                        if days_since_last_drawdown <= 30 and current_close > last_drawdown['price']:
                            continuation_occurred = True
                            self.logger.debug(f"Continuation detected: recovery from drawdown at {current_date}")
            
            # FIX 1: Restructure termination logic - don't terminate immediately on 30%+ drawdown
            # Instead, continue tracking to capture the full drawdown and potential recovery
            if current_drawdown >= MAX_DRAWDOWN_PERCENTAGE:
                # Record this as a significant drawdown but don't terminate yet
                if not any(d['date'] == current_date for d in drawdowns):
                    drawdowns.append({
                        'date': current_date,
                        'drawdown': current_drawdown,
                        'price': current_close
                    })
                    self.logger.debug(f"Major drawdown recorded: {current_drawdown:.1f}% at {current_date}")
                
                # Only terminate if we've gone too long without recovery
                if days_without_high >= MAX_DAYS_WITHOUT_HIGH:
                    move_terminated = True
                    termination_reason = f"30+ days without new high after {current_drawdown:.1f}% drawdown"
                    self.logger.debug(f"Move terminated: {termination_reason} at {current_date}")
                    break
            
            # Check if we've gone too long without a new high (but allow for drawdown recovery)
            if days_without_high >= MAX_DAYS_WITHOUT_HIGH:
                # Only terminate if we're not in a significant drawdown recovery period
                if current_drawdown < MIN_DRAWDOWN_PERCENTAGE:
                    move_terminated = True
                    termination_reason = f"30+ days without new high (drawdown: {current_drawdown:.1f}%)"
                    self.logger.debug(f"Move terminated: {termination_reason} at {current_date}")
                    break
        
        # Calculate final metrics
        if peak_price > lod_price:
            growth_percentage = self.calculate_percentage_change(lod_price, peak_price)
            duration_days = (datetime.strptime(peak_date, '%Y-%m-%d') - start_datetime).days
            
            # Determine superperformance status
            superperformance_status = self.classify_superperformance(growth_percentage, duration_days)
            
            self.logger.debug(f"Move completed: {growth_percentage:.1f}% growth over {duration_days} days")
            self.logger.debug(f"Drawdowns found: {len(drawdowns)}")
            self.logger.debug(f"Continuation: {continuation_occurred}")
            
            return {
                'start_date': start_date,
                'end_date': peak_date,
                'start_price': lod_price,
                'peak_price': peak_price,
                'growth_percentage': growth_percentage,
                'duration_days': duration_days,
                'drawdowns': [d['date'] for d in drawdowns],
                'continuation': continuation_occurred,
                'superperformance': superperformance_status,
                'new_lod_after_drawdown': new_lod_after_drawdown,
                'termination_reason': termination_reason if move_terminated else None
            }
        
        return None
    
    def classify_superperformance(self, growth_percentage: float, duration_days: int) -> str:
        """Classify the move as Growth, Superperformance, or None"""
        if 64 <= duration_days <= 252:
            if growth_percentage >= GROWTH_THRESHOLDS['super_64_252']:
                return 'Superperformance'
            elif growth_percentage >= GROWTH_THRESHOLDS['growth_64_252']:
                return 'Growth'
        elif 252 < duration_days <= 504:
            if growth_percentage >= GROWTH_THRESHOLDS['super_252_504']:
                return 'Superperformance'
            elif growth_percentage >= GROWTH_THRESHOLDS['growth_252_504']:
                return 'Growth'
        
        return 'None'
    
    def analyze_stock(self, ticker: str, data: List[Dict]) -> List[Dict]:
        """
        Analyze a stock for all growth moves
        
        Args:
            ticker: Stock ticker symbol
            data: Historical OHLC data
            
        Returns:
            List of growth move results
        """
        if not data or len(data) < GROWTH_MOVE_DAYS + 1:
            return []
        
        # Sort data by date
        data = sorted(data, key=lambda x: x['date'])
        
        # Find LOD candidates
        lod_candidates = self.find_lowest_of_day_candidates(data)
        
        moves = []
        processed_indices = set()
        
        for candidate in lod_candidates:
            start_index = candidate['index']
            
            # Skip if we've already processed this area
            if any(abs(start_index - idx) < 5 for idx in processed_indices):
                continue
            
            # Detect growth move
            move = self.detect_growth_move(data, start_index)
            
            if move:
                # Format dates for output
                move['ticker'] = ticker
                move['start_date_formatted'] = self.format_date(move['start_date'])
                move['end_date_formatted'] = self.format_date(move['end_date'])
                move['drawdowns_formatted'] = [self.format_date(d) for d in move['drawdowns']]
                move['continuation_formatted'] = 'Yes' if move['continuation'] else 'No'
                move['superperformance_formatted'] = 'Yes' if move['superperformance'] in ['Growth', 'Superperformance'] else 'No'
                
                moves.append(move)
                processed_indices.add(start_index)
        
        return moves
    
    def filter_valid_moves(self, moves: List[Dict]) -> List[Dict]:
        """Filter moves to only include those that meet criteria"""
        valid_moves = []
        
        for move in moves:
            # Only include moves that are Growth or Superperformance
            if move['superperformance'] in ['Growth', 'Superperformance']:
                valid_moves.append(move)
        
        return valid_moves
    
    def format_output_row(self, move: Dict) -> List[str]:
        """Format a move for Google Sheets output"""
        drawdowns_str = ', '.join(move['drawdowns_formatted']) if move['drawdowns_formatted'] else 'none'
        
        return [
            move['ticker'],
            move['start_date_formatted'],
            move['end_date_formatted'],
            move['superperformance_formatted'],
            drawdowns_str,
            move['continuation_formatted']
        ] 

    def debug_move_analysis(self, ticker: str, data: List[Dict], start_index: int) -> Dict:
        """
        Debug method to analyze a single move with detailed logging
        
        Args:
            ticker: Stock ticker symbol
            data: Historical OHLC data
            start_index: Starting index for the move
            
        Returns:
            Dict with detailed analysis information
        """
        self.logger.info(f"🔍 DEBUG: Analyzing move for {ticker} starting at index {start_index}")
        
        if start_index >= len(data) - 1:
            self.logger.warning(f"❌ DEBUG: Invalid start index {start_index} for data length {len(data)}")
            return {}
        
        start_data = data[start_index]
        start_date = start_data['date']
        lod_price = start_data['low']
        
        self.logger.info(f"📊 DEBUG: LOD Date: {start_date}, LOD Price: {lod_price}")
        
        # Run the normal analysis
        result = self.detect_growth_move(data, start_index)
        
        if result:
            self.logger.info(f"✅ DEBUG: Move found for {ticker}")
            self.logger.info(f"   📈 Growth: {result['growth_percentage']:.1f}%")
            self.logger.info(f"   📅 Duration: {result['duration_days']} days")
            self.logger.info(f"   📉 Drawdowns: {len(result['drawdowns'])}")
            self.logger.info(f"   🔄 Continuation: {result['continuation']}")
            self.logger.info(f"   🏷️ Classification: {result['superperformance']}")
            
            if result['drawdowns']:
                self.logger.info(f"   📊 Drawdown dates: {result['drawdowns']}")
            
            if result.get('termination_reason'):
                self.logger.info(f"   ⏹️ Termination: {result['termination_reason']}")
        else:
            self.logger.warning(f"❌ DEBUG: No valid move found for {ticker}")
        
        return result or {} 