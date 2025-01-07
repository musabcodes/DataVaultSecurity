import sqlite3

class ReportManager:
    def __init__(self, db_name="compliance_reports.db"):
        self.db_name = db_name
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS reports 
                     (bucket_name TEXT, issue TEXT)''')
        conn.commit()
        conn.close()

    def store_report(self, bucket_name, issues):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        for issue in issues:
            c.execute("INSERT INTO reports (bucket_name, issue) VALUES (?, ?)", 
                      (bucket_name, issue))
        conn.commit()
        conn.close()
