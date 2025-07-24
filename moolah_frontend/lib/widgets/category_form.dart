import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/category.dart';

class CategoryForm extends StatefulWidget {
  final Category? category;
  const CategoryForm({Key? key, this.category}) : super(key: key);

  @override
  State<CategoryForm> createState() => _CategoryFormState();
}

class _CategoryFormState extends State<CategoryForm> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  bool _loading = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    if (widget.category != null) {
      _nameController.text = widget.category!.name;
    }
  }

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final category = Category(
        id: widget.category?.id ?? 0,
        name: _nameController.text,
      );
      if (widget.category == null) {
        await ApiService.createCategory(category);
      } else {
        await ApiService.updateCategory(widget.category!.id, category);
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
        title: Text(widget.category == null ? 'Nueva categoría' : 'Editar categoría',
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
                  controller: _nameController,
                  decoration: const InputDecoration(labelText: 'Nombre'),
                  style: theme.textTheme.bodyText2,
                  validator: (v) =>
                      v == null || v.isEmpty ? 'Campo obligatorio' : null,
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
