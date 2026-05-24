"""
وحدة الطباعة الافتراضية
"""

class Printer:
    @staticmethod
    def print_text(text):
        print(text)

    @staticmethod
    def print_document(file_path):
        print(f"Printing document: {file_path}")
