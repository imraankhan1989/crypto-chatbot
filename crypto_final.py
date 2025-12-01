import time
import random
import requests

# Global variables
user_balance = 100000
user_portfolio = {}
trade_history = []

def get_prices():
    """Get crypto prices - tries live API first, falls back to sample data"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum,matic-network,solana,binancecoin,cardano',
            'vs_currencies': 'inr',
            'include_24hr_change': 'true'
        }
        
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            prices = {
                'BTC': {'price': data['bitcoin']['inr'], 'name': 'Bitcoin', 'change': data['bitcoin']['inr_24h_change']},
                'ETH': {'price': data['ethereum']['inr'], 'name': 'Ethereum', 'change': data['ethereum']['inr_24h_change']},
                'MATIC': {'price': data['matic-network']['inr'], 'name': 'Polygon', 'change': data['matic-network']['inr_24h_change']},
                'SOL': {'price': data['solana']['inr'], 'name': 'Solana', 'change': data['solana']['inr_24h_change']},
                'BNB': {'price': data['binancecoin']['inr'], 'name': 'Binance Coin', 'change': data['binancecoin']['inr_24h_change']},
                'ADA': {'price': data['cardano']['inr'], 'name': 'Cardano', 'change': data['cardano']['inr_24h_change']},
            }
            print("✅ Live prices loaded")
            return prices
    except:
        pass
    
    # Fallback data
    return {
        'BTC': {'price': 3842000, 'name': 'Bitcoin', 'change': 2.4},
        'ETH': {'price': 218000, 'name': 'Ethereum', 'change': 1.8},
        'MATIC': {'price': 68.42, 'name': 'Polygon', 'change': 3.2},
        'SOL': {'price': 5842, 'name': 'Solana', 'change': 4.1},
        'BNB': {'price': 31200, 'name': 'Binance Coin', 'change': 0.8},
        'ADA': {'price': 45.50, 'name': 'Cardano', 'change': -1.2},
    }

# Initialize prices
prices = get_prices()

def show_market():
    print("\n" + "="*60)
    print("📊 CRYPTO PRICES IN ₹")
    print("="*60)
    
    for symbol, data in prices.items():
        arrow = "▲" if data['change'] >= 0 else "▼"
        print(f"{symbol} ({data['name']}):")
        print(f"  Price: ₹{data['price']:,.2f}")
        print(f"  Change: {arrow} {abs(data['change']):.1f}%")
        print()

def show_portfolio():
    print("\n" + "="*60)
    print("💰 YOUR PORTFOLIO")
    print("="*60)
    print(f"Cash: ₹{user_balance:,.2f}")
    
    if not user_portfolio:
        print("\nNo holdings. Use 'buy BTC 10000' to start.")
        return
    
    total = user_balance
    print("\nHoldings:")
    for symbol, qty in user_portfolio.items():
        if symbol in prices:
            value = qty * prices[symbol]['price']
            total += value
            print(f"{symbol}: {qty:.6f} = ₹{value:,.2f}")
    
    print(f"\nTotal: ₹{total:,.2f}")

def buy(symbol, amount):
    global user_balance
    
    symbol = symbol.upper()
    if symbol not in prices:
        print(f"❌ {symbol} not available")
        return
    
    if amount > user_balance:
        print(f"❌ Need ₹{amount}, have ₹{user_balance}")
        return
    
    price = prices[symbol]['price']
    qty = amount / price
    
    user_balance -= amount
    if symbol in user_portfolio:
        user_portfolio[symbol] += qty
    else:
        user_portfolio[symbol] = qty
    
    trade_history.append({
        'time': time.strftime("%H:%M:%S"),
        'action': 'BUY',
        'symbol': symbol,
        'qty': qty,
        'price': price,
        'amount': amount
    })
    
    print(f"\n✅ Bought {qty:.6f} {symbol} for ₹{amount:,.2f}")
    print(f"Balance: ₹{user_balance:,.2f}")

def sell(symbol, qty=None):
    global user_balance
    
    symbol = symbol.upper()
    if symbol not in user_portfolio:
        print(f"❌ Don't own {symbol}")
        return
    
    owned = user_portfolio[symbol]
    if qty is None or qty > owned:
        qty = owned
    
    price = prices[symbol]['price']
    amount = qty * price
    
    user_balance += amount
    
    if qty == owned:
        del user_portfolio[symbol]
    else:
        user_portfolio[symbol] -= qty
    
    trade_history.append({
        'time': time.strftime("%H:%M:%S"),
        'action': 'SELL',
        'symbol': symbol,
        'qty': qty,
        'price': price,
        'amount': amount
    })
    
    print(f"\n✅ Sold {qty:.6f} {symbol} for ₹{amount:,.2f}")
    print(f"Balance: ₹{user_balance:,.2f}")

def analyze(symbol):
    symbol = symbol.upper()
    if symbol not in prices:
        print(f"❌ {symbol} not found")
        return
    
    data = prices[symbol]
    change = data['change']
    
    if change > 3:
        rec = "BUY"
        reason = "Strong momentum"
    elif change > 0:
        rec = "HOLD"
        reason = "Moderate growth"
    else:
        rec = "SELL"
        reason = "Downward trend"
    
    print(f"\n🎯 {symbol} ANALYSIS")
    print("="*60)
    print(f"Price: ₹{data['price']:,.2f}")
    print(f"24h: {'▲' if change >= 0 else '▼'} {abs(change):.1f}%")
    print(f"\nRecommend: {rec}")
    print(f"Reason: {reason}")
    
    if rec == "BUY":
        print(f"\nTarget: ₹{data['price'] * 1.08:,.2f} (+8%)")
        print(f"Stop: ₹{data['price'] * 0.96:,.2f} (-4%)")

def refresh():
    global prices
    print("\n🔄 Refreshing prices...")
    prices = get_prices()
    print("✅ Updated")

def help_menu():
    print("""
🤖 COMMANDS:
market    - Show prices
portfolio - Show holdings
buy SYM AMT  - Buy crypto (buy BTC 10000)
sell SYM QTY - Sell crypto (sell BTC 0.5)
analyze SYM  - Analyze coin
refresh   - Update prices
help      - This menu
exit      - Quit

COINS: BTC, ETH, MATIC, SOL, BNB, ADA
""")

def main():
    print("\n" + "="*60)
    print("🤖 CRYPTO CHATBOT")
    print("="*60)
    print("Type 'help' for commands")
    
    while True:
        try:
            cmd = input("\n💬 You: ").strip().lower()
            
            if not cmd:
                continue
            
            if cmd == 'exit':
                print("\n👋 Goodbye!")
                break
            elif cmd == 'help':
                help_menu()
            elif cmd == 'market':
                show_market()
            elif cmd == 'portfolio':
                show_portfolio()
            elif cmd.startswith('buy '):
                parts = cmd.split()
                if len(parts) == 3:
                    try:
                        buy(parts[1], float(parts[2]))
                    except:
                        print("❌ Use: buy BTC 10000")
                else:
                    print("❌ Use: buy BTC 10000")
            elif cmd.startswith('sell '):
                parts = cmd.split()
                if len(parts) == 3:
                    try:
                        sell(parts[1], float(parts[2]))
                    except:
                        print("❌ Use: sell BTC 0.5")
                else:
                    print("❌ Use: sell BTC 0.5")
            elif cmd.startswith('analyze '):
                parts = cmd.split()
                if len(parts) == 2:
                    analyze(parts[1])
                else:
                    print("❌ Use: analyze BTC")
            elif cmd == 'refresh':
                refresh()
            else:
                print("❌ Unknown command. Type 'help'")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()