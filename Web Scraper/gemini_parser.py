import requests
import pandas as pd
from typing import List, Dict
import os
from dotenv import load_dotenv
import json
from io import StringIO
import csv

# Load environment variables
load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def clean_csv_data(csv_text: str) -> str:
    """Clean and validate CSV data to ensure consistent column counts."""
    try:
        # Read the CSV text into a list of rows
        rows = list(csv.reader(StringIO(csv_text)))
        if not rows:
            return ""
            
        # Get the number of columns from the header
        header = rows[0]
        num_columns = len(header)
        
        # Clean and validate each row
        cleaned_rows = [header]  # Start with the header
        for row in rows[1:]:
            if len(row) != num_columns:
                # If row has more columns, truncate
                if len(row) > num_columns:
                    row = row[:num_columns]
                # If row has fewer columns, pad with empty strings
                else:
                    row.extend([''] * (num_columns - len(row)))
            cleaned_rows.append(row)
        
        # Convert back to CSV string
        output = StringIO()
        writer = csv.writer(output)
        writer.writerows(cleaned_rows)
        return output.getvalue()
    except Exception as e:
        print(f"Error cleaning CSV data: {str(e)}")
        return ""

def create_csv_prompt(dom_content: str, parse_description: str) -> str:
    """Create a prompt for extracting structured data in CSV format."""
    return f"""You are a data extraction expert specialized in movie information. Your task is to analyze the website content and extract movie data in CSV format.

Website Content:
{dom_content}

Extraction Requirements:
{parse_description}

Please follow these rules strictly:
1. The output must be a valid CSV with exactly 3 columns:
   - Column 1: "Movie Name" (text)
   - Column 2: "Average Rating" (number between 0-10)
   - Column 3: "Total Ratings" (number)
2. Each row must represent one movie
3. Numbers should be plain numbers without any formatting:
   - Correct: 8.5, 1000
   - Wrong: "8.5/10", "1,000 ratings"
4. Do not include any explanations or text outside the CSV format
5. If no movie data is found, return an empty string
6. Ensure UTF-8 encoding for special characters
7. Do not include any headers or footers besides the CSV data

Example output format:
Movie Name,Average Rating,Total Ratings
The Shawshank Redemption,9.3,2500000
The Godfather,9.2,1800000
Pulp Fiction,8.9,1900000"""

def parse_with_gemini(dom_chunks: List[str], parse_description: str) -> pd.DataFrame:
    """Parse website content using Gemini API and return a pandas DataFrame."""
    all_data = []
    
    for i, chunk in enumerate(dom_chunks, start=1):
        prompt = create_csv_prompt(chunk, parse_description)
        
        # Prepare the request payload
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        # Make the API request
        try:
            response = requests.post(
                API_URL,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0'
                },
                json=payload
            )
            response.raise_for_status()
            
            # Extract the response text
            response_data = response.json()
            if 'candidates' in response_data and response_data['candidates']:
                text_response = response_data['candidates'][0]['content']['parts'][0]['text']
                
                if text_response.strip():
                    try:
                        # Clean the CSV data before processing
                        cleaned_csv = clean_csv_data(text_response)
                        if cleaned_csv:
                            # Convert CSV string to DataFrame with specific dtypes
                            df_chunk = pd.read_csv(
                                StringIO(cleaned_csv),
                                dtype={
                                    'Movie Name': str,
                                    'Average Rating': float,
                                    'Total Ratings': int
                                }
                            )
                            # Validate data types and ranges
                            if all(0 <= rating <= 10 for rating in df_chunk['Average Rating']) and \
                               all(total > 0 for total in df_chunk['Total Ratings']):
                                all_data.append(df_chunk)
                            else:
                                print(f"Invalid data in chunk {i}: Ratings out of range")
                    except Exception as e:
                        print(f"Error processing chunk {i}: {str(e)}")
                        continue
                        
        except Exception as e:
            print(f"API request failed for chunk {i}: {str(e)}")
            continue
    
    if not all_data:
        return pd.DataFrame(columns=['Movie Name', 'Average Rating', 'Total Ratings'])
    
    # Combine all chunks
    final_df = pd.concat(all_data, ignore_index=True)
    return final_df

def save_to_csv(df: pd.DataFrame, filename: str = "extracted_data.csv"):
    """Save the DataFrame to a CSV file."""
    if not df.empty:
        df.to_csv(filename, index=False)
        return True
    return False