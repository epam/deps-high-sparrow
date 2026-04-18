## Rule Syntax

Custom rules use simple Python expressions to define validation logic.

- **Field References**: To reference the value of a field, use the format `F<fieldCode>`.
  Example: `F0457d9e633aa429cb9ba96be36eb45ff`

- **Expression Format**: The rule should be a valid Python boolean expression. Built-in functions can be used, refer to Built-in Functions page.

  Example:
```python
int(F<field_code>) > 100
```

  Array index access example:
```python
int(F<field_code>[0]) is True
```

  Each array item validation example:
```python
Fitem_of__<field_code> == 'test'
```

  Date in fieldA is before date in fieldB
```python
compare_dates(FfieldA, FfieldB, op="lt")
```

  Conditional rule example
```python
F<field_code> % 2 == 0 if F<field_code> > 0 else (F<field_code> > 0 and F<field_code> % 2 == 0)
```

  RegExp rule example, check that field contains only letters and spaces
```python
validate_field_content(F<field_code>, '^[a-zA-Z\-\'\s]+$')
```


  Key-value field validation example (check that key is equal to some value)
```python
F<field_code>__0 == "key"
```

  Key-value field validation example (check that value is equal to some value)
```python
F<field_code>__1 == "value"
```

  Table cells validation example
```python
F<field_code>[0][0] == F<field_code>[1][1]"
```

