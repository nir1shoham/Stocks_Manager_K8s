class Error(Exception):
    """Base class for other exceptions"""
    pass
class ExternalAPIServiceError(Error):
    """Occurs due to an issue with an external API"""
    pass

class StockNotExists(Error):
    """Occurs when a stock's symbol is not found in the API"""
    pass

class StockNotFoundError(Error):
    """Not found"""
    pass

class DuplicateStockError(Error):
    """Occurs when the stock is already present in the collection"""
    pass

class RequiredFieldMissingError(Error):
    """Occurs when a necessary field is absent"""
    pass

class EmptyPortfolioError(Error):
    """Occurs when the portfolio is empty"""
    pass

class UnsupportedContentType(Error):
    """Occurs when the content type is not supported"""
    pass

# In Exceptions.py
class DatabaseError(Exception):
    """Raised for errors related to database operations."""
    pass

class InvalidFieldError(Exception):
    """Raised when a field is invalid."""
    pass

class InvalidQueryParameterError(Exception):
    """Raised when a query parameter is invalid."""
    pass