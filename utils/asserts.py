class Asserts:
    @staticmethod
    def assert_str(var):
        assert isinstance(var, str) or var is None, 'Parameter type must be str (with None)'

    @staticmethod
    def assert_str_strict(var):
        assert isinstance(var, str), 'Parameter type must be str'

    @staticmethod
    def assert_int(var):
        assert isinstance(var, int) or var is None, 'Parameter type must be int (with None)'

    @staticmethod
    def assert_int_strict(var):
        assert isinstance(var, int) or var is None, 'Parameter type must be int'

    @staticmethod
    def assert_int_non_negative(var, include_zero=True):
        assert isinstance(var, int), 'Parameter type must be int'
        if include_zero:
            assert var >= 0, 'Parameter type must be >= 0'
        else:
            assert var > 0, 'Parameter value must be > 0'

    @staticmethod
    def assert_bool(var):
        assert isinstance(var, bool) or var is None, 'Parameter type must be bool (with None)'

    @staticmethod
    def assert_bool_strict(var):
        assert isinstance(var, bool), 'Parameter type must be bool'
        