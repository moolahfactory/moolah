class Budget {
  final int id;
  final String month;
  final double limit;
  final int ownerId;

  Budget({
    required this.id,
    required this.month,
    required this.limit,
    required this.ownerId,
  });

  factory Budget.fromJson(Map<String, dynamic> json) {
    return Budget(
      id: json['id'] as int,
      month: json['month'] as String,
      limit: (json['limit'] as num).toDouble(),
      ownerId: json['owner_id'] as int,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'month': month,
      'limit': limit,
      'owner_id': ownerId,
    };
  }
}
