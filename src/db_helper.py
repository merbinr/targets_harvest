import sqlite3



class DBHelper:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
    
    def __drop_table(self, table_name):
        cursor = self.conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.conn.commit()
    
    def __create_programs_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE programs (
                id INTEGER PRIMARY KEY,
                platform TEXT,
                program_id TEXT,
                name TEXT,
                currency TEXT,
                state TEXT,
                triage_active TEXT,
                visibility TEXT,
                created_at TEXT,
                offers_bounties TEXT
            )
        """)
        self.conn.commit()
    
    def __create_scopes_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE scopes (
                id INTEGER PRIMARY KEY,
                platform TEXT,
                program_id TEXT,
                asset TEXT,
                asset_type TEXT,
                eligible_for_bounty TEXT,
                eligible_for_submission TEXT,
                max_severity TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        self.conn.commit()
    def insert_scope(self, scope_data):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO scopes (
                platform,
                program_id,
                asset,
                asset_type,
                eligible_for_bounty,
                eligible_for_submission,
                max_severity,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            scope_data.get("platform"),
            scope_data.get("program_id"),
            scope_data.get("asset"),
            scope_data.get("asset_type"),
            scope_data.get("eligible_for_bounty"),
            scope_data.get("eligible_for_submission"),
            scope_data.get("max_severity"),
            scope_data.get("created_at"),
            scope_data.get("updated_at")
        ))
        self.conn.commit()

    def insert_program(self, program_data):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO programs (
                platform,
                program_id,
                name,
                currency,
                state,
                triage_active,
                visibility,
                created_at,
                offers_bounties
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            program_data.get("platform"),
            program_data.get("program_id"),
            program_data.get("name"),
            program_data.get("currency"),
            program_data.get("state"),
            program_data.get("triage_active"),
            program_data.get("visibility"),
            program_data.get("created_at"),
            program_data.get("offers_bounties")
        ))
        self.conn.commit()

    def initialize_db(self):
        self.__drop_table("programs")
        self.__drop_table("scopes")
        self.__create_programs_table()
        self.__create_scopes_table()
