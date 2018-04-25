class external_error(Exception):
    pass


class parser_syntax_error(external_error):
    pass


class net_definition_error(external_error):
    pass


class circuit_error(external_error):
    pass


class internal_error(Exception):
    pass
