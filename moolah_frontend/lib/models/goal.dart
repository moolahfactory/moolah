class Goal {
  final int id;
  final String description;
  final double targetAmount;
  final bool achieved;
  final int ownerId;

  Goal({
    required this.id,
    required this.description,
    required this.targetAmount,
    required this.achieved,
    required this.ownerId,
  });

  factory Goal.fromJson(Map<String, dynamic> json) {
    return Goal(
      id: json['id'] as int,
      description: json['description'] as String,
      targetAmount: (json['target_amount'] as num).toDouble(),
      achieved: json['achieved'] as bool,
      ownerId: json['owner_id'] as int,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'description': description,
      'target_amount': targetAmount,
      'achieved': achieved,
      'owner_id': ownerId,
    };
  }
}
