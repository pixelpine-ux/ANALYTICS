from typing import List, Dict, Tuple, Optional
import json
from sqlalchemy.orm import Session
from .data_processor import DataProcessor


class GoogleSheetsConnector:
    """
    Google Sheets integration with robust error handling
    Senior Engineer Principle: Fail gracefully, provide clear error messages
    """
    
    def __init__(self, db: Session, credentials_file: Optional[str] = None):
        self.db = db
        self.credentials_file = credentials_file
        self.service = None
        
    def _initialize_service(self):
        """
        Lazy initialization of Google Sheets service
        Algorithm: Initialize only when needed to save resources
        """
        if self.service is not None:
            return True
            
        try:
            # Import here to make it optional
            from google.oauth2.service_account import Credentials
            from googleapiclient.discovery import build
            
            if not self.credentials_file:
                raise ValueError("Google credentials file not configured")
            
            # Define required scopes
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            
            # Load credentials
            credentials = Credentials.from_service_account_file(
                self.credentials_file, 
                scopes=SCOPES
            )
            
            # Build service
            self.service = build('sheets', 'v4', credentials=credentials)
            return True
            
        except ImportError:
            raise ImportError("Google API libraries not installed. Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        except Exception as e:
            raise ConnectionError(f"Failed to initialize Google Sheets service: {str(e)}")
    
    def extract_sheet_data(self, spreadsheet_id: str, range_name: str = "Sheet1") -> Tuple[int, List[str]]:
        """
        Extract data from Google Sheets and process it
        
        Args:
            spreadsheet_id: The ID from the Google Sheets URL
            range_name: Sheet name and optional range (e.g., "Sheet1!A1:D100")
        
        Returns:
            Tuple of (records_processed, errors_list)
        """
        try:
            # Initialize service if needed
            if not self._initialize_service():
                return 0, ["Failed to initialize Google Sheets connection"]
            
            # Fetch data from sheet
            sheet_data = self._fetch_sheet_data(spreadsheet_id, range_name)
            
            if not sheet_data:
                return 0, ["No data found in the specified range"]
            
            # Convert to CSV format for processing
            csv_content = self._convert_to_csv(sheet_data)
            
            # Use existing CSV processor
            processor = DataProcessor(self.db)
            records_processed, errors = processor.process_csv_content(csv_content)
            
            return records_processed, errors
            
        except Exception as e:
            return 0, [f"Google Sheets extraction error: {str(e)}"]
    
    def _fetch_sheet_data(self, spreadsheet_id: str, range_name: str) -> List[List[str]]:
        """
        Fetch raw data from Google Sheets
        Algorithm: Single API call with error handling
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                raise ValueError("No data found in spreadsheet")
            
            return values
            
        except Exception as e:
            if "not found" in str(e).lower():
                raise ValueError(f"Spreadsheet not found or not accessible: {spreadsheet_id}")
            elif "permission" in str(e).lower():
                raise PermissionError("Insufficient permissions to access spreadsheet")
            else:
                raise ConnectionError(f"Failed to fetch data: {str(e)}")
    
    def _convert_to_csv(self, sheet_data: List[List[str]]) -> str:
        """
        Convert Google Sheets data to CSV format
        Algorithm: Join with commas, handle empty cells
        """
        csv_lines = []
        
        for row in sheet_data:
            # Pad row with empty strings if needed
            padded_row = row + [''] * (len(sheet_data[0]) - len(row))
            # Escape commas and quotes in cell values
            escaped_row = [self._escape_csv_value(cell) for cell in padded_row]
            csv_lines.append(','.join(escaped_row))
        
        return '\n'.join(csv_lines)
    
    def _escape_csv_value(self, value: str) -> str:
        """
        Escape CSV special characters
        Algorithm: Quote values containing commas or quotes
        """
        value = str(value).strip()
        
        if ',' in value or '"' in value or '\n' in value:
            # Escape quotes by doubling them
            escaped_value = value.replace('"', '""')
            return f'"{escaped_value}"'
        
        return value
    
    def validate_sheet_access(self, spreadsheet_id: str) -> Dict[str, any]:
        """
        Test connection and validate sheet structure
        Returns metadata about the sheet for validation
        """
        try:
            if not self._initialize_service():
                return {"valid": False, "error": "Failed to initialize connection"}
            
            # Get spreadsheet metadata
            metadata = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id
            ).execute()
            
            sheets = metadata.get('sheets', [])
            sheet_names = [sheet['properties']['title'] for sheet in sheets]
            
            # Get sample data from first sheet
            if sheet_names:
                sample_data = self._fetch_sheet_data(spreadsheet_id, f"{sheet_names[0]}!1:5")
                
                return {
                    "valid": True,
                    "title": metadata.get('properties', {}).get('title', 'Unknown'),
                    "sheet_names": sheet_names,
                    "sample_headers": sample_data[0] if sample_data else [],
                    "sample_rows": len(sample_data) - 1 if sample_data else 0
                }
            else:
                return {"valid": False, "error": "No sheets found in spreadsheet"}
                
        except Exception as e:
            return {"valid": False, "error": str(e)}


class SheetsURLParser:
    """
    Utility class to extract spreadsheet ID from Google Sheets URLs
    """
    
    @staticmethod
    def extract_spreadsheet_id(url: str) -> Optional[str]:
        """
        Extract spreadsheet ID from various Google Sheets URL formats
        
        Supported formats:
        - https://docs.google.com/spreadsheets/d/{ID}/edit#gid=0
        - https://docs.google.com/spreadsheets/d/{ID}/
        """
        import re
        
        # Pattern to match Google Sheets URLs
        pattern = r'/spreadsheets/d/([a-zA-Z0-9-_]+)'
        match = re.search(pattern, url)
        
        if match:
            return match.group(1)
        
        # If it's already just an ID (no URL), return as-is
        if re.match(r'^[a-zA-Z0-9-_]+$', url.strip()):
            return url.strip()
        
        return None
    
    @staticmethod
    def validate_url_format(url: str) -> bool:
        """Check if URL looks like a valid Google Sheets URL"""
        return 'docs.google.com/spreadsheets' in url or SheetsURLParser.extract_spreadsheet_id(url) is not None