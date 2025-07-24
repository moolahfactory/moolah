import 'package:flutter/material.dart';
import 'dart:io';
import '../services/api_service.dart';
import '../models/rewards_data.dart';
import '../models/reward.dart';

class RewardsScreen extends StatefulWidget {
  const RewardsScreen({Key? key}) : super(key: key);

  @override
  State<RewardsScreen> createState() => _RewardsScreenState();
}

class _RewardsScreenState extends State<RewardsScreen> {
  RewardsData? _rewards;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _fetch();
  }

  Future<void> _fetch() async {
    try {
      final data = await ApiService.getRewards();
      setState(() => _rewards = data);
    } on SocketException {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Sin conexión a internet')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: Text('Recompensas', style: theme.textTheme.headline6)),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _rewards == null
              ? const Center(child: Text('Sin datos'))
              : Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Puntos: ${_rewards!.points}', style: theme.textTheme.headline6),
                      const SizedBox(height: 20),
                      const Text('Recompensas desbloqueadas:'),
                      ..._rewards!.rewards.map(
                        (Reward r) => Padding(
                          padding: const EdgeInsets.symmetric(vertical: 4),
                          child: Card(
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                            elevation: 2,
                            child: ListTile(
                              title: Text(r.level.toString(),
                                  style: theme.textTheme.bodyText1),
                              subtitle: Text(
                                'Puntos: ${r.points} - ${r.timestamp.toIso8601String().split('T').first}',
                                style: theme.textTheme.bodyText2,
                              ),
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 20),
                      const Text('Recompensas disponibles:'),
                      ..._rewards!.available.map(
                        (String r) => Padding(
                          padding: const EdgeInsets.symmetric(vertical: 4),
                          child: Card(
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                            elevation: 2,
                            child: ListTile(
                              title: Text(r,
                                  style: theme.textTheme.bodyText1),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
    );
  }
}
