import sqlite3

def store_report(bucket_name, issues):
    conn = sqlite3.connect('compliance_reports.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports 
                 (bucket_name TEXT, issue TEXT)''')

    for issue in issues:
        c.execute("INSERT INTO reports (bucket_name, issue) VALUES (?, ?)", 
                  (bucket_name, issue))
    conn.commit()
    conn.close()

# Example usage
store_report('datavaultsecurity', ['Unencrypted file detected', 'Sensitive data found'])