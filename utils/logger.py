import sys
from pathlib import Path
from loguru import logger
from datetime import datetime


def setup_logger(log_dir: str = "logs"):
    """
    Configure loguru logger for the test framework
    This should be called once at the start of test execution
    """
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Remove default logger
    logger.remove()
    
    # Console handler - INFO level and above with colors
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    # File handler - DEBUG level (detailed logs)
    debug_log = log_path / f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger.add(
        debug_log,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        enqueue=True
    )
    
    # File handler - INFO level (execution logs)
    info_log = log_path / f"execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger.add(
        info_log,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        level="INFO",
        rotation="5 MB",
        retention="30 days",
        compression="zip",
        enqueue=True
    )
    
    # File handler - ERROR level only
    error_log = log_path / f"errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger.add(
        error_log,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}",
        level="ERROR",
        rotation="5 MB",
        retention="90 days",
        compression="zip",
        enqueue=True,
        backtrace=True,
        diagnose=True
    )
    
    logger.info("Logger initialized successfully")
    return logger


# ✅ FIXED: Double underscores
__all__ = ['logger', 'setup_logger']