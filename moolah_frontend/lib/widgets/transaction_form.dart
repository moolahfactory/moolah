import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/transaction.dart';
import '../models/category.dart';

class TransactionForm extends StatefulWidget {
  final Transaction? transaction;
  const TransactionForm({Key? key, this.transaction}) : super(key: key);

  @override
  State<TransactionForm> createState() => _TransactionFormState();
}

class _TransactionFormState extends State<TransactionForm> {
  final _formKey = GlobalKey<FormState>();
  final _amountController = TextEditingController();
  List<Category> _categories = [];
  int? _categoryId;
  bool _loading = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    if (widget.transaction != null) {
      _amountController.text = widget.transaction!.amount.toString();
      _categoryId = widget.transaction!.categoryId;
    }
    _loadCategories();
  }

  @override
  void dispose() {
    _amountController.dispose();
    super.dispose();
  }

  Future<void> _loadCategories() async {
    try {
      final data = await ApiService.getCategories();
      setState(() => _categories = data);
    } catch (_) {}
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final tx = Transaction(
        id: widget.transaction?.id ?? 0,
        amount: double.tryParse(_amountController.text) ?? 0,
        timestamp: widget.transaction?.timestamp ?? DateTime.now(),
        ownerId: widget.transaction?.ownerId ?? 0,
        categoryId: _categoryId,
        description: widget.transaction?.description,
      );
      if (widget.transaction == null) {
        await ApiService.createTransaction(tx);
      } else {
        await ApiService.updateTransaction(widget.transaction!.id, tx);
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
        title: Text(widget.transaction == null
            ? 'Nueva transacción'
            : 'Editar transacción',
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
                  controller: _amountController,
                  decoration: const InputDecoration(labelText: 'Monto'),
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
                DropdownButtonFormField<int?>(
                  value: _categoryId,
                  decoration: const InputDecoration(labelText: 'Categoría'),
                  items: [
                    const DropdownMenuItem<int?>(
                      value: null,
                  child: Text('Sin categoría'),
                ),
                ..._categories.map(
                  (c) => DropdownMenuItem<int?>(
                    value: c.id,
                    child: Text(c.name),
                  ),
                ),
              ],
              onChanged: (v) => setState(() => _categoryId = v),
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
