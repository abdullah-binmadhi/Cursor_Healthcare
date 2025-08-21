#!/usr/bin/env python3
"""
Healthcare Analytics Query Runner
Executes essential healthcare analytics queries and displays results
"""

import sqlite3
import pandas as pd
from datetime import datetime
import sys
import re

def parse_queries_from_file(filename):
    """Parse queries from SQL file"""
    with open(filename, 'r') as f:
        content = f.read()
    
    # Split by query headers
    query_sections = re.split(r'-- =+\s*\n-- \d+\.\s*([^\n]+)\s*\n-- =+\s*', content)
    
    queries = []
    query_names = []
    
    for i in range(1, len(query_sections), 2):
        if i + 1 < len(query_sections):
            query_name = query_sections[i].strip()
            query_sql = query_sections[i + 1].strip()
            
            # Clean up the SQL
            query_sql = re.sub(r'^\s*--.*$', '', query_sql, flags=re.MULTILINE)
            query_sql = query_sql.strip()
            
            if query_sql:
                queries.append(query_sql)
                query_names.append(query_name)
    
    return queries, query_names

def run_analytics_queries():
    """Run all essential healthcare analytics queries"""
    
    try:
        # Connect to database
        conn = sqlite3.connect('healthcare_analytics.db')
        print("=" * 80)
        print("HEALTHCARE ANALYTICS DASHBOARD")
        print("=" * 80)
        print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Parse queries
        queries, query_names = parse_queries_from_file('essential_analytics_queries.sql')
        
        for i, (query, query_name) in enumerate(zip(queries, query_names), 1):
            try:
                print(f"\n{'='*60}")
                print(f"QUERY {i}: {query_name}")
                print(f"{'='*60}")
                
                # Execute query
                df = pd.read_sql_query(query, conn)
                
                if not df.empty:
                    print(f"Results: {len(df)} rows")
                    print("-" * 60)
                    print(df.to_string(index=False))
                else:
                    print("No results found")
                    
            except Exception as e:
                print(f"Error executing query {i}: {str(e)}")
                continue
        
        conn.close()
        print(f"\n{'='*80}")
        print("ANALYTICS COMPLETED SUCCESSFULLY")
        print(f"{'='*80}")
        
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        sys.exit(1)

def run_specific_query(query_number):
    """Run a specific query by number"""
    
    try:
        conn = sqlite3.connect('healthcare_analytics.db')
        
        # Parse queries
        queries, query_names = parse_queries_from_file('essential_analytics_queries.sql')
        
        if 1 <= query_number <= len(queries):
            query = queries[query_number - 1]
            query_name = query_names[query_number - 1]
            
            print(f"\n{'='*60}")
            print(f"EXECUTING: {query_name}")
            print(f"{'='*60}")
            print(f"SQL Query:\n{query}")
            print(f"\n{'='*60}")
            print("RESULTS:")
            print(f"{'='*60}")
            
            df = pd.read_sql_query(query, conn)
            
            if not df.empty:
                print(f"Results: {len(df)} rows")
                print("-" * 60)
                print(df.to_string(index=False))
            else:
                print("No results found")
        else:
            print(f"Query number {query_number} not found. Available queries: 1-{len(queries)}")
            
        conn.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")

def list_available_queries():
    """List all available queries"""
    
    try:
        queries, query_names = parse_queries_from_file('essential_analytics_queries.sql')
        
        print("AVAILABLE ANALYTICS QUERIES:")
        print("=" * 50)
        
        for i, query_name in enumerate(query_names, 1):
            print(f"{i:2d}. {query_name}")
            
    except Exception as e:
        print(f"Error reading queries: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            list_available_queries()
        elif sys.argv[1].isdigit():
            run_specific_query(int(sys.argv[1]))
        else:
            print("Usage:")
            print("  python run_analytics_queries.py          # Run all queries")
            print("  python run_analytics_queries.py --list   # List available queries")
            print("  python run_analytics_queries.py <number> # Run specific query")
    else:
        run_analytics_queries()
