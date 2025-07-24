import 'package:flutter/material.dart';
import 'dart:io';
import '../services/api_service.dart';
import '../widgets/budget_form.dart';
import '../models/budget.dart';

class BudgetsScreen extends StatefulWidget {
  const BudgetsScreen({Key? key}) : super(key: key);

  @override
  State<BudgetsScreen> createState() => _BudgetsScreenState();
}

class _BudgetsScreenState extends State<BudgetsScreen> {
  List<Budget> _budgets = [];
  Map<String, double> _totals = {};
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _fetch();
  }

  Future<void> _fetch() async {
    try {
      final budgets = await ApiService.getBudgets();
      final monthly = await ApiService.getMonthlySummary();

      final totals = <String, double>{};
      for (final item in monthly) {
        if (item['month'] != null && item['total'] != null) {
          totals[item['month']] = (item['total'] as num).toDouble().abs();
        }
      }

      setState(() {
        _budgets = budgets;
        _totals = totals;
      });
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
      appBar: AppBar(title: Text('Presupuestos', style: theme.textTheme.headline6)),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: _budgets.length,
              itemBuilder: (context, index) {
                final b = _budgets[index];
                return Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  child: Card(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    elevation: 2,
                    child: ListTile(
                      title: Text(b.month, style: theme.textTheme.bodyText1),
                      subtitle: Builder(builder: (context) {
                        final spent = _totals[b.month] ?? 0.0;
                        final limit = b.limit.toDouble();
                        final ratio = limit > 0 ? (spent / limit).clamp(0.0, 1.0) : 0.0;
                        Color barColor;
                        if (spent >= limit) {
                          barColor = Colors.red;
                        } else if (spent >= limit * 0.9) {
                          barColor = Colors.orange;
                        } else {
                          barColor = theme.colorScheme.primary;
                        }

                        return Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('L\u00edmite: ${b.limit}', style: theme.textTheme.bodyText2),
                            const SizedBox(height: 4),
                            LinearProgressIndicator(
                              value: ratio,
                              backgroundColor: barColor.withOpacity(0.2),
                              valueColor: AlwaysStoppedAnimation<Color>(barColor),
                            ),
                            const SizedBox(height: 2),
                            Text('Gastado: \$${spent.toStringAsFixed(2)}', style: theme.textTheme.caption),
                          ],
                        );
                      }),
                      trailing: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          IconButton(
                            icon: const Icon(Icons.edit),
                            onPressed: () async {
                              final result = await Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) => BudgetForm(budget: b),
                                ),
                              );
                              if (result == true) _fetch();
                            },
                          ),
                          IconButton(
                            icon: const Icon(Icons.delete),
                            onPressed: () async {
                              try {
                                await ApiService.deleteBudget(b.id);
                                _fetch();
                              } on SocketException {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(content: Text('Sin conexión a internet')),
                                );
                              } catch (e) {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  SnackBar(content: Text('Error: $e')),
                                );
                              }
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                );
              },
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          final result = await Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const BudgetForm()),
          );
          if (result == true) _fetch();
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
