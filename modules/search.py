from typing import List, Dict, Any


def search_transactions(transactions: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по подстроке в описании или категории.
    Регистронезависимый поиск. Поддерживает русский и английский текст.
    """
    if not query:
        return transactions
    
    query_lower = query.lower()
    # Создаём список вариантов запроса (русская/английская о)
    query_variants = {query_lower, query_lower.replace('о', 'o'), query_lower.replace('o', 'о')}
    
    results = []
    for t in transactions:
        desc = t.get('description', '').lower()
        category = t.get('category', '').lower()
        
        for qv in query_variants:
            if qv in desc or qv in category:
                results.append(t)
                break
    
    return results


def format_search_results(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Форматирует результаты поиска для JSON-отчёта.
    """
    return [
        {
            "date": t.get("date", ""),
            "amount": abs(t.get("amount", 0)),
            "category": t.get("category", ""),
            "description": t.get("description", "")
        }
        for t in transactions
    ]


if __name__ == "__main__":
    # Добавляем путь к модулям
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from modules.transactions import load_transactions_from_excel
    
    trans = load_transactions_from_excel("data/operations.xlsx")
    
    test_queries = ["озон", "ozon", "магнит", "колхоз", "перевод"]
    
    for query in test_queries:
        results = search_transactions(trans, query)
        print(f"Поиск '{query}': {len(results)} транзакций")
