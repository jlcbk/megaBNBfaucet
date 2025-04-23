import sqlite3

def view_wallets():
    conn = sqlite3.connect('/Users/fomostorm/Documents/megaBNB/wallets.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM wallets")
    for row in c.fetchall():
        print(row)
    
    conn.close()

if __name__ == "__main__":
    view_wallets()