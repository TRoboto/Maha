__all__ = ["Rule", "RuleCollection"]

from dataclasses import dataclass
from typing import List, Union

from maha.rexy import Expression, ExpressionGroup, ExpressionResult, non_capturing_group


@dataclass
class Rule:
    """
    Template representing a rule.

    Parameters
    ----------
    name : str
        The name of the rule.
    expression : Union[str, Expression]
        The expression to apply to the text.
    rule_type : DimensionType
        The type of the rule.

    Raises
    ------
    NameError
        If the name is already used.
    """

    __slots__ = ["name", "expression"]

    _rules = dict()
    name: str
    expression: Expression

    @property
    def pattern(self) -> str:
        """The regex pattern for the rule."""
        return self.expression.pattern

    def __init__(
        self, name: str, expression: Union[str, Expression, ExpressionGroup]
    ) -> None:
        if name in Rule._rules:
            raise NameError("Already used name '%s'." % name)
        Rule._rules[name] = self

        self.name = name
        if isinstance(expression, str):
            self.expression = Expression(expression)
        elif isinstance(expression, ExpressionGroup):
            self.expression = Expression(expression.join())
        else:
            self.expression = expression

    def __call__(self, text: str) -> List[ExpressionResult]:
        return self.apply(text)

    def apply(self, text: str) -> List[ExpressionResult]:
        """Applies the rule to the given text."""
        return list(self.expression(text))

    def compile(self):
        """Compiles the rule."""
        self.expression.compile()

    def __str__(self) -> str:
        return str(self.expression)

    def __add__(self, other: Union[str, Expression]) -> str:
        return self.pattern + other

    def __radd__(self, other: Union[str, Expression]) -> str:
        return other + self.pattern

    @classmethod
    def get(cls, name: str) -> "Rule":
        """Gets the rule with the given name."""
        return cls._rules[name]

    @classmethod
    def get_index_of_rule(cls, name: str) -> int:
        """
        Get the index of the rule with the given name.

        Parameters
        ----------
        name : str
            The name of the rule.

        Returns
        -------
        int
            The index of the rule with the given name.
        """
        for i, rule in enumerate(cls._rules):
            if cls._rules[rule].name == name:
                return i
        raise KeyError("No rule with name '%s'." % name)

    @classmethod
    def slice(cls, start: Union[str, int], stop: Union[str, int]) -> "RuleCollection":
        """
        Slice the rule collection.

        Parameters
        ----------
        start :
            The start index.
        stop :
            The stop index.

        Returns
        -------
        RuleCollection
            The sliced rule collection.
        """
        start_index = start
        end_index = stop
        if isinstance(start_index, str):
            start_index = cls.get_index_of_rule(start_index)
        if isinstance(end_index, str):
            end_index = cls.get_index_of_rule(end_index) + 1
        return RuleCollection(list(cls._rules.values())[start_index:end_index])

    @classmethod
    def combine_patterns(cls, *patterns: str) -> str:
        """
        Intelligently combine following input patterns.

        Parameters
        ----------
        patterns :
            The patterns to combine.

        Returns
        -------
        str
            The combined pattern.
        """
        from maha.parsers.expressions import WORD_SEPARATOR
        from maha.parsers.helper import wrap_pattern

        start_group = non_capturing_group(*[str(p) for p in patterns])
        pattern = wrap_pattern(
            start_group + non_capturing_group(WORD_SEPARATOR + start_group) + "*"
        )

        return pattern

    @classmethod
    def get_rules_with_name_startswith(cls, name_start: str) -> "RuleCollection":
        """
        Get rules with the given name start.

        Parameters
        ----------
        name_start : str
            The name start of the rule.

        Returns
        -------
        List[Rule]
            The rules with the given name start.
        """
        return RuleCollection(
            [rule for rule in cls._rules.values() if rule.name.startswith(name_start)]
        )

    @classmethod
    def get_rules_with_names(cls, *names: str) -> "RuleCollection":
        """
        Get rules with the given name start.

        Parameters
        ----------
        name_start : str
            The name start of the rule.

        Returns
        -------
        List[Rule]
            The rules with the given name start.
        """
        return RuleCollection(
            [rule for rule in cls._rules.values() if rule.name in names]
        )


@dataclass
class RuleCollection:
    """
    A collection of rules.

    Parameters
    ----------
    rules : List[Rule]
        The rules to combine.
    """

    __slots__ = ["rules"]
    rules: List[Rule]

    @property
    def expression_group(self) -> ExpressionGroup:
        """The expression group to use."""
        return ExpressionGroup(*[rule.expression for rule in self.rules])

    @property
    def patterns(self) -> List[str]:
        """The expression group to use."""
        return [str(rule.expression) for rule in self.rules]

    def __init__(
        self,
        rules: List[Rule],
    ) -> None:
        self.rules = rules

    def apply(self, text: str) -> List[ExpressionResult]:
        """Apply the rules to the given text."""
        return list(self.expression_group.parse(text))

    def join(self) -> str:
        """
        Joins the rules one after the other.

        Returns
        -------
        str
            The joined pattern.
        """
        return self.expression_group.join()

    def add_rule(self, rule: Union[Rule, "RuleCollection"]) -> "RuleCollection":
        """
        Adds a rule to the collection.

        Parameters
        ----------
        rule : Union[Rule, RuleCollection]
            The rule to add.
        """
        if isinstance(rule, RuleCollection):
            self.rules.extend(rule.rules)
        else:
            self.rules.append(rule)
        return self

    def get_rule_by_name(self, name: str) -> Rule:
        """
        Get a rule by its name.

        Parameters
        ----------
        name : str
            The name of the rule.

        Returns
        -------
        Rule
            The rule.
        """
        for rule in self.rules:
            if rule.name == name:
                return rule
        raise KeyError("No rule with name '%s'." % name)

    def __getitem__(self, key: Union[str, int]) -> Rule:
        """Get a rule by its name or index."""
        if isinstance(key, int):
            return self.rules[key]
        elif isinstance(key, str):
            return self.get_rule_by_name(key)

        raise TypeError("Index with {} is not supported".format(type(key).__name__))
