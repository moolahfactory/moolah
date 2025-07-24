class Reward {
  final int id;
  final String level;
  final int points;
  final DateTime timestamp;
  final int ownerId;

  Reward({
    required this.id,
    required this.level,
    required this.points,
    required this.timestamp,
    required this.ownerId,
  });

  factory Reward.fromJson(Map<String, dynamic> json) {
    return Reward(
      id: json['id'] as int,
      level: json['level'] as String,
      points: json['points'] as int,
      timestamp: DateTime.parse(json['timestamp']),
      ownerId: json['owner_id'] as int,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'level': level,
      'points': points,
      'timestamp': timestamp.toIso8601String(),
      'owner_id': ownerId,
    };
  }
}
