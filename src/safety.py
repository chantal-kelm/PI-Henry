def is_adversarial_query(query: str) -> bool:
    """
    Analiza de forma heurística la consulta entrante para mitigar inyecciones de prompt.
    Retorna True si detecta intenciones maliciosas, False si la consulta es segura.
    """
    if not query:
        return False
        
    query_clean = query.strip().lower()
    
    # Palabras clave y heurísticas típicas de ataques adversariales de inyección
    adversarial_patterns = [
        "ignora las instrucciones",
        "olvida lo anterior",
        "ignore previous",
        "ignore instructions",
        "system prompt",
        "revela tus instrucciones",
        "revela tu prompt",
        "actúa como un modo",
        "you are now a",
        "bypass rules"
    ]
    
    return any(pattern in query_clean for pattern in adversarial_patterns)