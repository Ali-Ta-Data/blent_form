def try_except(func):
    """
    Produit automatiquement une erreur 500 si une exception est levée
    """
    def wrapper(**kwargs):
        try:
            return func(**kwargs)
        except Exception as e:
            return {'error': str(e)}, 500
    return wrapper

@try_except
def with_error():
    raise Exception("Produit volontairement une erreur")

@try_except
def without_error():
    return "Ne produit pas d'erreur"
    
print(with_error())
print(without_error())