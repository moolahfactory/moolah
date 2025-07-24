class Transaction {
  final int id;
  final double amount;
  final DateTime timestamp;
  final int ownerId;
  final int? categoryId;
  final String? description;

  Transaction({
    required this.id,
    required this.amount,
    required this.timestamp,
    required this.ownerId,
    this.categoryId,
    this.description,
  });

  factory Transaction.fromJson(Map<String, dynamic> json) {
    return Transaction(
      id: json['id'] as int,
      amount: (json['amount'] as num).toDouble(),
      timestamp: DateTime.parse(json['timestamp']),
      ownerId: json['owner_id'] as int,
      categoryId: json['category_id'] as int?,
      description: json['description'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'amount': amount,
      'timestamp': timestamp.toIso8601String(),
      'owner_id': ownerId,
      'category_id': categoryId,
      if (description != null) 'description': description,
    };
  }
}
