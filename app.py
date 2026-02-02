"""
Sample application with multiple functions - some tested, some not.
This demonstrates a codebase with partial test coverage (~40-50%).
"""

import json
import os
from typing import List, Dict, Optional

print("hellooooooo0000 jiiiii")
# ============ TESTED FUNCTIONS (will have coverage) ============

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b


def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# ============ UNTESTED FUNCTIONS (no coverage) ============

def divide(a: int, b: int) -> float:
    """Divide a by b with error handling."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base: int, exponent: int) -> int:
    """Calculate base raised to exponent."""
    if exponent < 0:
        raise ValueError("Negative exponents not supported")
    result = 1
    for _ in range(exponent):
        result *= base
    return result


def factorial(n: int) -> int:
    """Calculate factorial of n."""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fibonacci(n: int) -> List[int]:
    """Generate first n Fibonacci numbers."""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib


def is_prime(n: int) -> bool:
    """Check if n is a prime number."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def find_primes(limit: int) -> List[int]:
    """Find all prime numbers up to limit."""
    primes = []
    for num in range(2, limit + 1):
        if is_prime(num):
            primes.append(num)
    return primes


# ============ STRING FUNCTIONS (untested) ============

def reverse_string(s: str) -> str:
    """Reverse a string."""
    return s[::-1]


def is_palindrome(s: str) -> bool:
    """Check if string is a palindrome."""
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def count_vowels(s: str) -> int:
    """Count vowels in a string."""
    vowels = "aeiouAEIOU"
    return sum(1 for char in s if char in vowels)


def word_frequency(text: str) -> Dict[str, int]:
    """Calculate word frequency in text."""
    words = text.lower().split()
    frequency = {}
    for word in words:
        word = word.strip(".,!?;:")
        if word:
            frequency[word] = frequency.get(word, 0) + 1
    return frequency


# ============ DATA FUNCTIONS (untested) ============

def filter_even(numbers: List[int]) -> List[int]:
    """Filter even numbers from list."""
    return [n for n in numbers if n % 2 == 0]


def filter_odd(numbers: List[int]) -> List[int]:
    """Filter odd numbers from list."""
    return [n for n in numbers if n % 2 != 0]


def calculate_average(numbers: List[int]) -> float:
    """Calculate average of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


def find_max(numbers: List[int]) -> Optional[int]:
    """Find maximum value in list."""
    if not numbers:
        return None
    return max(numbers)


def find_min(numbers: List[int]) -> Optional[int]:
    """Find minimum value in list."""
    if not numbers:
        return None
    return min(numbers)


def sort_descending(numbers: List[int]) -> List[int]:
    """Sort numbers in descending order."""
    return sorted(numbers, reverse=True)


# ============ VALIDATION FUNCTIONS (untested) ============

def validate_email(email: str) -> bool:
    """Simple email validation."""
    if not email or '@' not in email:
        return False
    parts = email.split('@')
    if len(parts) != 2:
        return False
    local, domain = parts
    if not local or not domain:
        return False
    if '.' not in domain:
        return False
    return True


def validate_phone(phone: str) -> bool:
    """Validate phone number (10 digits)."""
    digits = ''.join(c for c in phone if c.isdigit())
    return len(digits) == 10


def validate_age(age: int) -> bool:
    """Validate age is reasonable."""
    return 0 <= age <= 150


# ============ NEW FUNCTIONS (to be tested) ============

def calculate_circle_area(radius: float) -> float:
    """Calculate area of a circle given its radius."""
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    import math
    return math.pi * (radius ** 2)


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format a number as a currency string."""
    return f"{currency} {amount:,.2f}"

