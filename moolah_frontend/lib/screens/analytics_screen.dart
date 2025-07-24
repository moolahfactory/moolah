import 'package:flutter/material.dart';
import 'dart:io';
import '../services/api_service.dart';

class AnalyticsScreen extends StatefulWidget {
  const AnalyticsScreen({Key? key}) : super(key: key);

  @override
  State<AnalyticsScreen> createState() => _AnalyticsScreenState();
}

class _AnalyticsScreenState extends State<AnalyticsScreen> {
  List<dynamic> _monthly = [];
  List<dynamic> _categories = [];
  bool _showCategories = false;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _fetch();
  }

  Future<void> _fetch() async {
    try {
      final monthly = await ApiService.getMonthlySummary();
      final byCategory = await ApiService.getCategorySummary();
      setState(() {
        _monthly = monthly;
        _categories = byCategory;
      });
    } on SocketException {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Sin conexión a internet')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: Text('Analíticas', style: theme.textTheme.headline6)),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _monthly.isEmpty
              ? const Center(child: Text('Sin datos'))
              : ListView(
                  padding: const EdgeInsets.all(16.0),
                  children: [
                    const Text('Totales por mes:'),
                    ..._monthly.map(
                      (m) => Padding(
                        padding: const EdgeInsets.symmetric(vertical: 4),
                        child: Card(
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                          elevation: 2,
                          child: ListTile(
                            title: Text(m['month'], style: theme.textTheme.bodyText1),
                            trailing: Text('${m['total']}', style: theme.textTheme.bodyText1),
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),
                    SwitchListTile(
                      title: const Text('Mostrar por categoría'),
                      value: _showCategories,
                      onChanged: (v) => setState(() => _showCategories = v),
                    ),
                    if (_showCategories) ...[
                      const SizedBox(height: 10),
                      const Text('Totales por categoría:'),
                      ..._categories.map(
                        (c) => Padding(
                          padding: const EdgeInsets.symmetric(vertical: 4),
                          child: Card(
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                            elevation: 2,
                            child: ListTile(
                              title: Text(c['category'], style: theme.textTheme.bodyText1),
                              trailing: Text('${c['total']}', style: theme.textTheme.bodyText1),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ],
                ),
    );
  }
}
