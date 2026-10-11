"""
A versão 1.9.4 do Experta (e sua dependência frozendict 1.2) ainda usa
`collections.Mapping`, que foram removidos do módulo `collections`
no Python 3.10. Recria esses nomes a partir de `collections.abc`.
Deve ser importado ANTES de `experta`.
"""
import collections
import collections.abc

for _nome in ("Mapping", "MutableMapping", "Sequence", "Iterable", "Callable", "Hashable"):
    if not hasattr(collections, _nome):
        setattr(collections, _nome, getattr(collections.abc, _nome))
