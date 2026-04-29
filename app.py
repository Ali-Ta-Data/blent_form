from flask import Flask, request, jsonify
from models import db, Product, Cart, CartItem

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de l'extension SQLAlchemy avec notre application
db.init_app(app)

# Création des tables au démarrage de l'application
@app.before_request
def create_tables():
    app.before_request_funcs[None].remove(create_tables)
    
    db.create_all()

# Ajout de quelques produits pour tester
@app.before_request
def add_sample_data():
    app.before_request_funcs[None].remove(add_sample_data)
    
    # Vérifier si des produits existent déjà
    if Product.query.count() == 0:
        products = [
            Product(id='je8zng', name='Smartphone Ultra', description='Smartphone pliable', price=799.99, stock=50),
            Product(id='ab9h2p', name='Casque Bluetooth', description='Audio haute qualité', price=129.99, stock=30),
            Product(id='cd5j7k', name='Livre Python', description='Apprendre Python en profondeur', price=39.99, stock=100)
        ]
        db.session.add_all(products)
        
        # Créer un panier vide
        cart = Cart()
        db.session.add(cart)
        
        db.session.commit()

# Récupérer le contenu du panier
@app.route('/cart', methods=['GET'])
def list_cart():
    # On récupère le premier panier (dans une vraie application, on identifierait le panier par utilisateur)
    cart = Cart.query.first()
    if not cart:
        # Si aucun panier n'existe, on en crée un
        cart = Cart()
        db.session.add(cart)
        db.session.commit()
    
    # On prépare la liste des produits dans le panier
    items = []
    for item in cart.items:
        product = Product.query.get(item.product_id)
        items.append({
            'id': item.product_id,
            'name': product.name,
            'price': product.price,
            'quantity': item.quantity
        })
    
    return jsonify(items), 200

# Ajouter un produit au panier
@app.route('/cart', methods=['POST'])
def add_to_cart():
    try:
        body = request.get_json()
        
        # Vérifier les champs requis
        if 'id' not in body or 'quantity' not in body:
            return jsonify({'error': 'Champs manquants (id ou quantity)'}), 400
        
        # Vérifier si le produit existe
        product = Product.query.get(body['id'])
        if not product:
            return jsonify({'error': 'Produit non trouvé'}), 404
        
        # Récupérer le panier actuel ou en créer un nouveau
        cart = Cart.query.first()
        if not cart:
            cart = Cart()
            db.session.add(cart)
            db.session.commit()
        
        # Vérifier si le produit est déjà dans le panier
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=body['id']).first()
        
        if cart_item:
            # Mettre à jour la quantité
            cart_item.quantity += int(body['quantity'])
        else:
            # Ajouter un nouvel élément au panier
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=body['id'],
                quantity=int(body['quantity'])
            )
            db.session.add(cart_item)
        
        db.session.commit()
        return jsonify({}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Modifier la quantité d'un produit dans le panier
@app.route('/cart', methods=['PATCH'])
def edit_cart():
    try:
        body = request.get_json()
        
        # Vérifier les champs requis
        if 'id' not in body or 'quantity' not in body:
            return jsonify({'error': 'Champs manquants (id ou quantity)'}), 400
        
        # Récupérer le panier actuel
        cart = Cart.query.first()
        if not cart:
            return jsonify({'error': 'Panier non trouvé'}), 404
        
        # Trouver l'élément dans le panier
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=body['id']).first()
        if not cart_item:
            return jsonify({'error': 'Produit non trouvé dans le panier'}), 404
        
        # Mettre à jour la quantité
        cart_item.quantity = int(body['quantity'])
        db.session.commit()
        
        return jsonify({}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Supprimer un produit du panier
@app.route('/cart', methods=['DELETE'])
def remove_from_cart():
    try:
        body = request.get_json()
        
        # Vérifier les champs requis
        if 'id' not in body:
            return jsonify({'error': 'Champ id manquant'}), 400
        
        # Récupérer le panier actuel
        cart = Cart.query.first()
        if not cart:
            return jsonify({'error': 'Panier non trouvé'}), 404
        
        # Trouver l'élément dans le panier
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=body['id']).first()
        if not cart_item:
            return jsonify({'error': 'Produit non trouvé dans le panier'}), 404
        
        # Supprimer l'élément du panier
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500