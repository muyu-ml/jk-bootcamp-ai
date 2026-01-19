#!/usr/bin/env python3
"""Script to execute seed.sql file."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Get database URL from environment
database_url = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ticket_db"
)

# Get the directory where this script is located
script_dir = Path(__file__).parent
seed_file = script_dir / "seed.sql"

def execute_seed():
    """Execute the seed.sql file."""
    try:
        # Create database engine
        engine = create_engine(database_url)
        
        # Read seed.sql file
        if not seed_file.exists():
            print(f"Error: {seed_file} not found!")
            sys.exit(1)
        
        print(f"Reading {seed_file}...")
        with open(seed_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Execute the entire SQL file
        # Use a transaction to ensure all-or-nothing execution
        with engine.begin() as connection:
            print("Executing seed.sql...")
            # Execute the entire SQL content
            connection.execute(text(sql_content))
        
        print("Successfully executed seed.sql!")
        print("Seed data has been loaded into the database.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    execute_seed()
