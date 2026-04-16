# Error handling utilities

import logging
import time
from typing import Optional, Callable, Any
from functools import wraps
from openai import RateLimitError as OpenAIRateLimitError, APIError as OpenAIAPIError, Timeout as OpenAITimeout, InternalServerError as OpenAIInternalServerError


class SupportAutomationError(Exception):
    """Base exception for support automation"""
    pass


class APIError(SupportAutomationError):
    """API-related errors"""
    pass


class ClassificationError(SupportAutomationError):
    """Classification-specific errors"""
    pass


class ResponseGenerationError(SupportAutomationError):
    """Response generation errors"""
    pass


def retry_on_rate_limit(max_retries: int = 3, base_delay: float = 1.0):
    """Decorator to retry on rate limit errors"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except OpenAIRateLimitError as e:
                    if attempt == max_retries - 1:
                        raise APIError(f"Rate limit exceeded after {max_retries} attempts")
                    
                    wait_time = base_delay * (2 ** attempt)  # Exponential backoff
                    logging.warning(f"Rate limit hit, retrying in {wait_time}s (attempt {attempt + 1})")
                    time.sleep(wait_time)
                except (OpenAITimeout, OpenAIInternalServerError) as e:
                    if attempt == max_retries - 1:
                        raise APIError(f"API error after {max_retries} attempts")
                    
                    wait_time = base_delay * (2 ** attempt)
                    logging.warning(f"API error, retrying in {wait_time}s (attempt {attempt + 1})")
                    time.sleep(wait_time)
            return None  # Should not reach here
        return wrapper
    return decorator


def fallback_to_keyword(fallback_func: Callable) -> Callable:
    """Decorator to fallback to keyword-based classifier on LLM failure"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.warning(f"LLM failed, falling back to keyword classifier: {e}")
                return fallback_func(*args, **kwargs)
        return wrapper
    return decorator


def monitor_performance(func: Callable) -> Callable:
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logging.info(f"{func.__name__} completed in {elapsed_time:.3f}s")
            return result
        except Exception as e:
            elapsed_time = time.time() - start_time
            logging.error(f"{func.__name__} failed after {elapsed_time:.3f}s: {e}")
            raise
    return wrapper
