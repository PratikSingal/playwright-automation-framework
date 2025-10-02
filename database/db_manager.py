import oracledb
from typing import List, Dict, Any, Optional
from config.config_manager import config
from loguru import logger
import allure


class DatabaseManager:
    """Database manager for Oracle database operations"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.db_config = config.db_config
    
    @allure.step("Connect to Oracle database")
    def connect(self) -> None:
        """Establish connection to Oracle database"""
        try:
            logger.info("Connecting to Oracle database")
            
            connection_string = f"{self.db_config['username']}/{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['service_name']}"
            
            self.connection = oracledb.connect(
                user=self.db_config['username'],
                password=self.db_config['password'],
                dsn=f"{self.db_config['host']}:{self.db_config['port']}/{self.db_config['service_name']}"
            )
            
            self.cursor = self.connection.cursor()
            logger.success("Successfully connected to Oracle database")
            
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise
    
    @allure.step("Execute query: {query}")
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute SELECT query and return results
        
        Args:
            query: SQL query to execute
            params: Optional query parameters
            
        Returns:
            List of dictionaries containing query results
        """
        try:
            logger.info(f"Executing query: {query}")
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            # Get column names
            columns = [desc[0] for desc in self.cursor.description]
            
            # Fetch all results
            rows = self.cursor.fetchall()
            
            # Convert to list of dictionaries
            results = [dict(zip(columns, row)) for row in rows]
            
            logger.success(f"Query executed successfully. Rows returned: {len(results)}")
            return results
            
        except Exception as e:
            logger.error(f"Failed to execute query: {str(e)}")
            raise
    
    @allure.step("Execute non-query: {query}")
    def execute_non_query(self, query: str, params: Optional[tuple] = None) -> int:
        """
        Execute INSERT, UPDATE, DELETE queries
        
        Args:
            query: SQL query to execute
            params: Optional query parameters
            
        Returns:
            Number of rows affected
        """
        try:
            logger.info(f"Executing non-query: {query}")
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            self.connection.commit()
            rows_affected = self.cursor.rowcount
            
            logger.success(f"Non-query executed successfully. Rows affected: {rows_affected}")
            return rows_affected
            
        except Exception as e:
            logger.error(f"Failed to execute non-query: {str(e)}")
            self.connection.rollback()
            raise
    
    @allure.step("Execute stored procedure: {proc_name}")
    def execute_procedure(self, proc_name: str, params: Optional[List] = None) -> Any:
        """
        Execute stored procedure
        
        Args:
            proc_name: Name of stored procedure
            params: List of parameters
            
        Returns:
            Result from stored procedure
        """
        try:
            logger.info(f"Executing stored procedure: {proc_name}")
            
            if params:
                result = self.cursor.callproc(proc_name, params)
            else:
                result = self.cursor.callproc(proc_name)
            
            self.connection.commit()
            logger.success(f"Stored procedure {proc_name} executed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Failed to execute stored procedure: {str(e)}")
            self.connection.rollback()
            raise
    
    @allure.step("Fetch single row")
    def fetch_one(self, query: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        """
        Fetch single row from query result
        
        Args:
            query: SQL query
            params: Optional query parameters
            
        Returns:
            Dictionary containing single row or None
        """
        try:
            logger.info(f"Fetching single row: {query}")
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            columns = [desc[0] for desc in self.cursor.description]
            row = self.cursor.fetchone()
            
            if row:
                result = dict(zip(columns, row))
                logger.success("Single row fetched successfully")
                return result
            
            logger.info("No row found")
            return None
            
        except Exception as e:
            logger.error(f"Failed to fetch single row: {str(e)}")
            raise
    
    @allure.step("Close database connection")
    def disconnect(self) -> None:
        """Close database connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            
            logger.success("Database connection closed successfully")
            
        except Exception as e:
            logger.error(f"Error closing database connection: {str(e)}")
            raise
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()


# Example usage:
# with DatabaseManager() as db:
#     results = db.execute_query("SELECT * FROM users WHERE id = :id", (1,))
#     print(results)