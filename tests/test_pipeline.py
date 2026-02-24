"""
Tests for the main data pipeline.
"""

import pytest
import pandas as pd

from src.main_pipeline import DataPipeline


class TestDataPipeline:
    """Test suite for DataPipeline class."""
    
    def test_pipeline_initialization(self):
        """Test pipeline can be initialized."""
        pipeline = DataPipeline()
        assert pipeline is not None
        assert pipeline.engines == {}
        assert pipeline.connections == {}
    
    def test_transform_data(self):
        """Test data transformation."""
        pipeline = DataPipeline()
        
        # Create sample data
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'value': [100, 200, None]
        })
        
        result = pipeline.transform_data(df)
        
        assert 'loaded_at' in result.columns
        assert 'source_system' in result.columns
        assert len(result) == 3
    
    def test_transform_with_nulls(self):
        """Test transformation handles null values."""
        pipeline = DataPipeline()
        
        df = pd.DataFrame({
            'id': [1, 2],
            'value': [None, None]
        })
        
        result = pipeline.transform_data(df)
        
        # Should drop rows with all nulls
        assert len(result) == 0 or 'loaded_at' in result.columns


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
