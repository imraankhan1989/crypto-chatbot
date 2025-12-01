# ============================================================================
# SIMPLE CRYPTO CHATBOT - SINGLE FILE
# ============================================================================

import sys
import json
import time
import random

# ============================================================================
# SIMPLE CRYPTO DATA
# ============================================================================

crypto_prices = {
    # TOP 10 FOR INDIA
    'BTC': {'price': 3842000, 'name': 'Bitcoin', 'change': 2.4},
    'ETH': {'price': 218000, 'name': 'Ethereum', 'change': 1.8},
    'USDT': {'price': 83.42, 'name': 'Tether', 'change': 0.1},
    'BNB': {'price': 31200, 'name': 'Binance Coin', 'change': 0.8},
    'SOL': {'price': 5842, 'name': 'Solana', 'change': 4.1},
    'XRP': {'price': 52.30, 'name': 'Ripple', 'change': 0.3},
    'ADA': {'price': 45.50, 'name': 'Cardano', 'change': -1.2},
    'DOGE': {'price': 12.80, 'name': 'Dogecoin', 'change': -0.5},
    
    # INDIAN FAVORITES
    'MATIC': {'price': 68.42, 'name': 'Polygon', 'change': 3.2},
    'SHIB': {'price': 0.0025, 'name': 'Shiba Inu', 'change': 5.2},
    'DOT': {'price': 620.75, 'name': 'Polkadot', 'change': -0.7},
}

# User's virtual portfolio
user_balance = 100000  # Start with ₹1,00,000
user_portfolio = {}  # Format: {'BTC': 0.5} means 0.5 BTC
trade_history = []

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def show_market():
    """Show current market prices"""
    print("\n" + "="*60)
    print("📊 CURRENT CRYPTO PRICES")
    print("="*60)
    
    for symbol, data in crypto_prices.items():
        arrow = "▲" if data['change'] >= 0 else "▼"
        print(f"{symbol} ({data['name']}):")
        print(f"  Price: ₹{data['price']:,.2f}")
        print(f"  24h Change: {arrow} {abs(data['change'])}%")
        print()

def show_portfolio():
    """Show user's portfolio"""
    print("\n" + "="*60)
    print("💰 YOUR PORTFOLIO")
    print("="*60)
    print(f"Cash Balance: ₹{user_balance:,.2f}")
    
    if not user_portfolio:
        print("\nYou don't own any cryptocurrencies yet.")
        print("Use 'buy BTC 10000' to start trading!")
        return
    
    total_value = user_balance
    
    print("\nYour Holdings:")
    print("-" * 40)
    
    for symbol, quantity in user_portfolio.items():
        if symbol in crypto_prices:
            current_price = crypto_prices[symbol]['price']
            value = quantity * current_price
            total_value += value
            
            print(f"{symbol}: {quantity:.6f} coins")
            print(f"  Current Price: ₹{current_price:,.2f}")
            print(f"  Value: ₹{value:,.2f}")
            print()
    
    print("-" * 40)
    print(f"Total Portfolio Value: ₹{total_value:,.2f}")

def buy_crypto(symbol, amount_inr):
    """Buy cryptocurrency"""
    global user_balance
    
    symbol = symbol.upper()
    
    if symbol not in crypto_prices:
        print(f"❌ {symbol} not found. Available: {', '.join(crypto_prices.keys())}")
        return
    
    if amount_inr > user_balance:
        print(f"❌ Insufficient balance. You have: ₹{user_balance:,.2f}")
        return
    
    price = crypto_prices[symbol]['price']
    quantity = amount_inr / price
    
    # Update portfolio
    user_balance -= amount_inr
    
    if symbol in user_portfolio:
        user_portfolio[symbol] += quantity
    else:
        user_portfolio[symbol] = quantity
    
    # Record trade
    trade_history.append({
        'date': time.strftime("%Y-%m-%d %H:%M"),
        'action': 'BUY',
        'symbol': symbol,
        'quantity': quantity,
        'price': price,
        'amount': amount_inr
    })
    
    print(f"\n✅ PURCHASE SUCCESSFUL!")
    print(f"Bought: {quantity:.6f} {symbol}")
    print(f"Price: ₹{price:,.2f} per coin")
    print(f"Total: ₹{amount_inr:,.2f}")
    print(f"Remaining Balance: ₹{user_balance:,.2f}")

def sell_crypto(symbol, quantity=None):
    """Sell cryptocurrency"""
    global user_balance
    
    symbol = symbol.upper()
    
    if symbol not in user_portfolio:
        print(f"❌ You don't own any {symbol}.")
        return
    
    owned_quantity = user_portfolio[symbol]
    
    # If quantity not specified, sell all
    if quantity is None or quantity > owned_quantity:
        quantity = owned_quantity
    
    price = crypto_prices[symbol]['price']
    proceeds = quantity * price
    
    # Update portfolio
    user_balance += proceeds
    
    if quantity == owned_quantity:
        # Sold all
        del user_portfolio[symbol]
    else:
        user_portfolio[symbol] -= quantity
    
    # Record trade
    trade_history.append({
        'date': time.strftime("%Y-%m-%d %H:%M"),
        'action': 'SELL',
        'symbol': symbol,
        'quantity': quantity,
        'price': price,
        'amount': proceeds
    })
    
    print(f"\n✅ SALE SUCCESSFUL!")
    print(f"Sold: {quantity:.6f} {symbol}")
    print(f"Price: ₹{price:,.2f} per coin")
    print(f"Proceeds: ₹{proceeds:,.2f}")
    print(f"New Balance: ₹{user_balance:,.2f}")

def analyze_crypto(symbol):
    """Give simple analysis of a cryptocurrency"""
    symbol = symbol.upper()
    
    if symbol not in crypto_prices:
        print(f"❌ {symbol} not found. Available: {', '.join(crypto_prices.keys())}")
        return
    
    data = crypto_prices[symbol]
    price = data['price']
    change = data['change']
    
    # Simple analysis logic
    if change > 3:
        action = "BUY"
        reason = "Strong upward momentum"
    elif change > 1:
        action = "HOLD"
        reason = "Moderate gains, watch closely"
    elif change < -2:
        action = "SELL"
        reason = "Significant downward pressure"
    else:
        action = "HOLD"
        reason = "Stable price movement"
    
    # Generate random confidence (70-95% for demo)
    confidence = random.randint(70, 95)
    
    print(f"\n🎯 ANALYSIS FOR {symbol} ({data['name']})")
    print("="*60)
    print(f"Current Price: ₹{price:,.2f}")
    print(f"24h Change: {'▲' if change >= 0 else '▼'} {abs(change)}%")
    print(f"\nRecommendation: {action}")
    print(f"Confidence: {confidence}%")
    print(f"Reason: {reason}")
    
    if action == "BUY":
        print(f"\nSuggested Entry: ₹{price * 0.995:,.2f}")
        print(f"Target: ₹{price * 1.08:,.2f} (+8%)")
        print(f"Stop Loss: ₹{price * 0.97:,.2f} (-3%)")
    elif action == "SELL":
        print(f"\nSuggested Exit: ₹{price * 1.005:,.2f}")
        print(f"Target: ₹{price * 0.92:,.2f} (-8%)")
        print(f"Stop Loss: ₹{price * 1.03:,.2f} (+3%)")

def show_help():
    """Show help menu"""
    print("""
🤖 CRYPTO CHATBOT HELP
════════════════════════════════════════════════════════════════

AVAILABLE COMMANDS:

1. market    - Show current crypto prices
2. portfolio - Show your portfolio and balance
3. buy [COIN] [AMOUNT] - Buy crypto (e.g., 'buy BTC 10000')
4. sell [COIN] [QUANTITY] - Sell crypto (e.g., 'sell BTC 0.5')
5. sell [COIN] all - Sell all of a coin
6. analyze [COIN] - Analyze a cryptocurrency
7. help      - Show this help menu
8. exit      - Exit the program

EXAMPLES:
  buy BTC 5000    - Buy ₹5,000 worth of Bitcoin
  sell ETH all    - Sell all Ethereum
  analyze MATIC   - Get analysis for Polygon

AVAILABLE COINS:
  BTC, ETH, USDT, BNB, SOL, XRP, ADA, DOGE, MATIC, SHIB, DOT
""")

# ============================================================================
# MAIN CHATBOT LOOP
# ============================================================================

def main():
    """Main chatbot function"""
    print("\n" + "="*60)
    print("🤖 WELCOME TO SIMPLE CRYPTO CHATBOT")
    print("="*60)
    print("Type 'help' to see available commands")
    print("Type 'market' to see current prices")
    print("="*60)
    
    while True:
        try:
            # Get user input
            print("\n" + "-" * 40)
            user_input = input("💬 You: ").strip()
            
            if not user_input:
                continue
            
            # Convert to lowercase for easier matching
            cmd = user_input.lower()
            
            # EXIT command
            if cmd in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye! Happy trading!")
                break
            
            # HELP command
            elif cmd in ['help', 'h']:
                show_help()
            
            # MARKET command
            elif cmd in ['market', 'm', 'prices']:
                show_market()
            
            # PORTFOLIO command
            elif cmd in ['portfolio', 'pf', 'balance']:
                show_portfolio()
            
            # ANALYZE command
            elif cmd.startswith('analyze '):
                parts = cmd.split(' ')
                if len(parts) >= 2:
                    symbol = parts[1].upper()
                    analyze_crypto(symbol)
                else:
                    print("❌ Please specify a coin. Example: 'analyze BTC'")
            
            # BUY command
            elif cmd.startswith('buy '):
                parts = cmd.split(' ')
                if len(parts) >= 3:
                    try:
                        symbol = parts[1].upper()
                        amount = float(parts[2])
                        buy_crypto(symbol, amount)
                    except ValueError:
                        print("❌ Invalid amount. Example: 'buy BTC 10000'")
                else:
                    print("❌ Format: 'buy [COIN] [AMOUNT]'. Example: 'buy BTC 10000'")
            
            # SELL command
            elif cmd.startswith('sell '):
                parts = cmd.split(' ')
                if len(parts) >= 2:
                    symbol = parts[1].upper()
                    
                    if len(parts) >= 3:
                        if parts[2].lower() == 'all':
                            # Sell all
                            if symbol in user_portfolio:
                                quantity = user_portfolio[symbol]
                                sell_crypto(symbol, quantity)
                            else:
                                print(f"❌ You don't own any {symbol}.")
                        else:
                            try:
                                quantity = float(parts[2])
                                sell_crypto(symbol, quantity)
                            except ValueError:
                                print("❌ Invalid quantity. Use a number or 'all'")
                    else:
                        print(f"❌ Specify quantity. Example: 'sell {symbol} all' or 'sell {symbol} 0.5'")
                else:
                    print("❌ Format: 'sell [COIN] [QUANTITY]' or 'sell [COIN] all'")
            
            # Unknown command
            else:
                print("❌ Unknown command. Type 'help' to see available commands.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using Crypto Chatbot!")
            break
        except Exception as e:
            print(f"\n⚠️  Error: {e}")
            print("Please try again.")

# ============================================================================
# RUN THE PROGRAM
# ============================================================================

if __name__ == "__main__":
    # Clear screen
    print("\n" * 3)
    
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPress Enter to exit...")
        input()