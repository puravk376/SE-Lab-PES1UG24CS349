"""Library catalog management module."""

import hashlib
import logging
import os
import secrets

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

catalog = {
    "B01": {"title": "Clean Code", "copies": 3, "total": 3},
    "B02": {"title": "The Pragmatic Programmer", "copies": 1, "total": 1},
    "B03": {"title": "Design Patterns", "copies": 2, "total": 2},
}

DAILY_FINE_RATE = 2.0


def issue_book(book_id, patron, active_issues=None):
    """Issue a book to a patron if a copy is available.

    Returns True on success, False if the book is unknown or out of stock.
    """
    if active_issues is None:
        active_issues = []
    if book_id not in catalog or catalog[book_id]["copies"] <= 0:
        return False
    catalog[book_id]["copies"] -= 1
    active_issues.append(f"Issued book {book_id} to patron {patron}")
    return True


def return_book(book_id):
    """Return a copy of a book to the catalog.

    Returns True on success. Returns False for an unknown book id, or when
    every copy is already on the shelf (nothing was issued to return).
    """
    try:
        book = catalog[book_id]
    except KeyError:
        logger.warning("Return rejected: unknown book id %s", book_id)
        return False
    if book["copies"] >= book["total"]:
        logger.warning("Return rejected: no issued copy of %s", book_id)
        return False
    book["copies"] += 1
    return True


def check_availability(book_id):
    """Return True if at least one copy of the book is on the shelf."""
    book = catalog.get(book_id)
    if book is None:
        return False
    return book["copies"] > 0


def calculate_fine(days_overdue, rate_per_day=DAILY_FINE_RATE):
    """Return the overdue fine for the given number of days."""
    return days_overdue * rate_per_day


def generate_patron_hash(patron_id):
    """Return a SHA-256 hash of the patron id."""
    return hashlib.sha256(patron_id.encode()).hexdigest()


def generate_temp_patron_pin():
    """Return a cryptographically secure 4-digit temporary PIN."""
    return 1000 + secrets.randbelow(9000)


def export_catalog(filename="catalog_export.txt"):
    """Write the catalog to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(catalog))
    print("Catalog backup exported to:", filename)


def main():
    """Run a short demonstration of the catalog functions."""
    librarian_key = os.environ.get("LIBRARIAN_KEY")
    print("Issued B01:", issue_book("B01", "P101"))
    print("Returned B02:", return_book("B02"))
    print("Is B01 available:", check_availability("B01"))
    print("Fine accrued:", calculate_fine(4))
    print("Patron Hash:", generate_patron_hash("P101"))
    print("Temp PIN:", generate_temp_patron_pin())
    export_catalog()
    print("Librarian key configured:", librarian_key is not None)


if __name__ == "__main__":
    main()
