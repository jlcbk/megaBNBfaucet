import sqlite3

def init_database():
    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS wallets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  address TEXT UNIQUE NOT NULL,
                  private_key TEXT NOT NULL,
                  claimed INTEGER DEFAULT 0)''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()