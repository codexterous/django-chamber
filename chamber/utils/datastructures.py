from django.utils.datastructures import SortedDict


class AbstractEnum(object):

    def _has_attr(self, name):
        return name in self

    def _get_attr_val(self, name):
        return name

    def __getattr__(self, name):
        if self._has_attr(name):
            return self._get_attr_val(name)
        raise AttributeError('Missing attribute %s' % name)


class Enum(AbstractEnum, set):

    def __init__(self, *items):
        super(Enum, self).__init__(items)


class NumEnum(AbstractEnum, dict):

    def __init__(self, *items):
        super(NumEnum, self).__init__()
        i = 1
        for arg in items:
            if arg is not None:
                self[arg] = i
            i += 1

    def _get_attr_val(self, name):
        return self[name]


class AbstractChoicesEnum(object):

    def _get_labels_dict(self):
        return dict(self._get_choices())

    def _get_choices(self):
        raise NotImplementedError

    @property
    def choices(self):
        return self._get_choices()

    @property
    def all(self):
        return (key for key, _ in self._get_choices())

    def get_label(self, name):
        labels = dict(self._get_choices())
        if name in labels:
            return labels[name]
        raise AttributeError('Missing label with index %s' % name)


class ChoicesEnum(AbstractChoicesEnum, AbstractEnum, SortedDict):

    def __init__(self, *items):
        super(ChoicesEnum, self).__init__()
        for key, val in items:
            self[key] = val

    def _get_choices(self):
        return self.items()

    def _get_labels_dict(self):
        raise self

    def _get_attr_val(self, name):
        return self[name]


class ChoicesNumEnum(AbstractChoicesEnum, AbstractEnum, SortedDict):

    def __init__(self, *items):
        super(ChoicesNumEnum, self).__init__()
        i = 0
        for item in items:
            if len(item) == 3:
                key, val, i = item
                if not isinstance(i, int):
                    raise ValueError('Last value of item must by integer')
            elif len(item) == 2:
                key, val = item
                i += 1
            else:
                raise ValueError('Wrong input data format')

            if i in (j for j, _ in self.values()):
                raise ValueError('Index %s already exists, please renumber choices')
            self[key] = (i, val)

    def _get_attr_val(self, name):
        return self[name][0]

    def _get_choices(self):
        return self.values()
