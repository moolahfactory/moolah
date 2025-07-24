import 'reward.dart';

class RewardsData {
  final int points;
  final List<Reward> rewards;
  final List<String> available;

  RewardsData({required this.points, required this.rewards, required this.available});

  factory RewardsData.fromJson(Map<String, dynamic> json) {
    final rewardsList = (json['rewards'] as List<dynamic>? ?? [])
        .map((e) => Reward.fromJson(e))
        .toList();
    final availableList = (json['available'] as List<dynamic>? ?? [])
        .map((e) => e.toString())
        .toList();
    return RewardsData(
      points: json['points'] as int? ?? 0,
      rewards: rewardsList,
      available: availableList,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'points': points,
      'rewards': rewards.map((e) => e.toJson()).toList(),
      'available': available,
    };
  }
}
