from itertools import chain

from django.db import models

class PrintableMixin:
    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            data[f.name] = f.value_from_object(self)
            if isinstance(
                f,
                (
                    models.DateTimeField,
                    models.DateField,
                    models.ImageField,
                    models.FileField,
                ),
            ):
                if f.value_from_object(self) is not None:
                    data[f.name] = str(f.value_from_object(self))
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(self)]
        return data