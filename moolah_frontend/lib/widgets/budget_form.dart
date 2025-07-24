import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/budget.dart';

class BudgetForm extends StatefulWidget {
  final Budget? budget;
  const BudgetForm({Key? key, this.budget}) : super(key: key);

  @override
  State<BudgetForm> createState() => _BudgetFormState();
}

class _BudgetFormState extends State<BudgetForm> {
  final _formKey = GlobalKey<FormState>();
  final _monthController = TextEditingController();
  final _limitController = TextEditingController();
  bool _loading = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    if (widget.budget != null) {
      _monthController.text = widget.budget!.month;
      _limitController.text = widget.budget!.limit.toString();
    }
  }

  @override
  void dispose() {
    _monthController.dispose();
    _limitController.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final budget = Budget(
        id: widget.budget?.id ?? 0,
        month: _monthController.text,
        limit: double.tryParse(_limitController.text) ?? 0,
        ownerId: widget.budget?.ownerId ?? 0,
      );
      if (widget.budget == null) {
        await ApiService.createBudget(budget);
      } else {
        await ApiService.updateBudget(widget.budget!.id, budget);
      }
      if (!mounted) return;
      Navigator.pop(context, true);
    } catch (e) {
      setState(() => _error = e.toString());
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.budget == null ? 'Nuevo presupuesto' : 'Editar presupuesto',
            style: theme.textTheme.headline6),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Form(
            key: _formKey,
            child: Column(
              children: [
                TextFormField(
                  controller: _monthController,
                  decoration:
                      const InputDecoration(labelText: 'Mes (YYYY-MM)'),
                  style: theme.textTheme.bodyText2,
                  validator: (v) =>
                      v == null || v.isEmpty ? 'Campo obligatorio' : null,
                ),
                TextFormField(
                  controller: _limitController,
                  decoration: const InputDecoration(labelText: 'Límite'),
                  keyboardType: TextInputType.number,
                  style: theme.textTheme.bodyText2,
                  validator: (v) {
                    final val = double.tryParse(v ?? '');
                    if (val == null || val <= 0) {
                      return 'Debe ser mayor a 0';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 20),
                if (_error != null)
                  Text(_error!,
                      style: theme.textTheme.bodyText2
                          ?.copyWith(color: Colors.red)),
                ElevatedButton(
                  onPressed: _loading ? null : _save,
                  child: _loading
                      ? const CircularProgressIndicator()
                      : Text('Guardar', style: theme.textTheme.button),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
