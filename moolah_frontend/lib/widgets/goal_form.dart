import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/goal.dart';

class GoalForm extends StatefulWidget {
  final Goal? goal;
  const GoalForm({Key? key, this.goal}) : super(key: key);

  @override
  State<GoalForm> createState() => _GoalFormState();
}

class _GoalFormState extends State<GoalForm> {
  final _formKey = GlobalKey<FormState>();
  final _descController = TextEditingController();
  final _amountController = TextEditingController();
  bool _loading = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    if (widget.goal != null) {
      _descController.text = widget.goal!.description;
      _amountController.text = widget.goal!.targetAmount.toString();
    }
  }

  @override
  void dispose() {
    _descController.dispose();
    _amountController.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final goal = Goal(
        id: widget.goal?.id ?? 0,
        description: _descController.text,
        targetAmount: double.tryParse(_amountController.text) ?? 0,
        achieved: widget.goal?.achieved ?? false,
        ownerId: widget.goal?.ownerId ?? 0,
      );
      if (widget.goal == null) {
        await ApiService.createGoal(goal);
      } else {
        await ApiService.updateGoal(widget.goal!.id, goal);
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
        title: Text(widget.goal == null ? 'Nueva meta' : 'Editar meta',
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
                  controller: _descController,
                  decoration: const InputDecoration(labelText: 'Descripción'),
                  style: theme.textTheme.bodyText2,
                  validator: (v) =>
                      v == null || v.isEmpty ? 'Campo obligatorio' : null,
                ),
                TextFormField(
                  controller: _amountController,
                  decoration:
                      const InputDecoration(labelText: 'Monto objetivo'),
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
