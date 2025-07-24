import 'reward.dart';

class User {
  final int id;
  final String email;
  final bool isActive;
  final bool isAdmin;
  final int points;
  final List<Reward> rewards;

  User({
    required this.id,
    required this.email,
    required this.isActive,
    required this.isAdmin,
    required this.points,
    required this.rewards,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    final rewardsJson = json['rewards'] as List<dynamic>? ?? [];
    final rewards = rewardsJson.map((e) => Reward.fromJson(e)).toList();
    return User(
      id: json['id'] as int,
      email: json['email'] as String,
      isActive: json['is_active'] as bool? ?? true,
      isAdmin: json['is_admin'] as bool? ?? false,
      points: json['points'] as int? ?? 0,
      rewards: rewards,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'is_active': isActive,
      'is_admin': isAdmin,
      'points': points,
      'rewards': rewards.map((e) => e.toJson()).toList(),
    };
  }
}
