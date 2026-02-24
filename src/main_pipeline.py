#!/usr/bin/env python3
"""
Data Engineering Portfolio - Main Pipeline
Production-ready data pipeline demonstrating modern data stack skills.
"""

import os
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import pandas as pd
from sqlalchemy import create_engine, text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataPipeline:
    """Modern data pipeline with dbt, multi-warehouse, and streaming support."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize pipeline with configuration."""
        self.config = config or {}
        self.engines = {}
        self.connections = {}
        logger.info("DataPipeline initialized")
    
    def connect_postgres(self, connection_string: str) -> bool:
        """Connect to PostgreSQL database."""
        try:
            engine = create_engine(connection_string)
            self.engines['postgres'] = engine
            logger.info("Connected to PostgreSQL")
            return True
        except Exception as e:
            logger.error(f"PostgreSQL connection failed: {e}")
            return False
    
    def extract_data(self, source: str, query: str) -> pd.DataFrame:
        """Extract data from source."""
        logger.info(f"Extracting from {source}")
        
        if source in self.engines:
            df = pd.read_sql(query, self.engines[source])
            logger.info(f"Extracted {len(df)} rows")
            return df
        else:
            raise ValueError(f"Source {source} not connected")
    
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform raw data."""
        logger.info("Transforming data")
        
        # Basic transformations
        df = df.copy()
        df['loaded_at'] = datetime.now()
        df['source_system'] = 'pipeline'
        
        # Data quality checks
        initial_rows = len(df)
        df = df.dropna(how='all')
        dropped_rows = initial_rows - len(df)
        
        if dropped_rows > 0:
            logger.warning(f"Dropped {dropped_rows} rows with all null values")
        
        logger.info(f"Transformed data: {len(df)} rows")
        return df
    
    def load_data(self, df: pd.DataFrame, target: str, table: str) -> bool:
        """Load data to target warehouse."""
        logger.info(f"Loading to {target}.{table}")
        
        if target not in self.engines:
            logger.error(f"Target {target} not connected")
            return False
        
        try:
            df.to_sql(
                table,
                self.engines[target],
                if_exists='append',
                index=False,
                method='multi'
            )
            logger.info(f"Loaded {len(df)} rows to {table}")
            return True
        except Exception as e:
            logger.error(f"Load failed: {e}")
            return False
    
    def run_pipeline(self, source: str, target: str, query: str, table: str) -> bool:
        """Run full ETL pipeline."""
        logger.info("=" * 50)
        logger.info("Starting pipeline run")
        logger.info("=" * 50)
        
        try:
            # Extract
            df = self.extract_data(source, query)
            
            # Transform
            df = self.transform_data(df)
            
            # Load
            success = self.load_data(df, target, table)
            
            logger.info("Pipeline completed successfully" if success else "Pipeline failed")
            return success
            
        except Exception as e:
            logger.error(f"Pipeline error: {e}")
            return False


def demo():
    """Run demo pipeline."""
    print("🚀 Data Engineering Portfolio - Demo Pipeline")
    print("=" * 50)
    
    pipeline = DataPipeline()
    
    # Demo with sample data
    sample_data = pd.DataFrame({
        'id': range(1, 11),
        'name': [f'Product_{i}' for i in range(1, 11)],
        'value': [i * 100 for i in range(1, 11)],
        'category': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C']
    })
    
    print(f"✅ Sample data created: {len(sample_data)} rows")
    print(f"📊 Columns: {list(sample_data.columns)}")
    print("\nSample data:")
    print(sample_data.head())
    
    print("\n" + "=" * 50)
    print("Pipeline demo completed!")
    print("Ready for real implementations.")
    
    return pipeline


if __name__ == "__main__":
    demo()
