from unittest import TestCase
from classes.Tester import *


class SetUpRules(TestCase):

    def setUp(self):
        self.rule_candidate_correct1 = "a.**.f.**".split(".")
        self.rule_candidate_correct2 = "a.**.f.g.**".split(".")

        self.rule_candidate_correct3 = "a.**.f.**".split(".")
        self.rule_candidate_correct4 = "a.**.g.*".split(".")

        self.rule_candidate_incorrect = "a.b.*".split(".")

        self.rule_original = "a.b.c.d.e.f.g.h".split(".")
        self.rule_original2 = "a.**.f.g.h".split(".")

        self.rule_original3 = "a.b.c.d.e.f.g.*".split(".")
        self.rule_original4 = "a.**.f.g.*".split(".")

        self.rule_original_real = 'dontwarn org.joda.convert.FromString'
        self.rule_candidate_real = 'dontwarn org.joda.convert.**'


class TestEquivalentRules(SetUpRules):

    def test_is_equivalent_class_spec(self):
        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_correct1, self.rule_original), True)
        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_correct2, self.rule_original), True)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_correct3, self.rule_original), True)
        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_correct4, self.rule_original), True)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_incorrect, self.rule_original), False)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_original, self.rule_candidate_correct1), False)
        self.assertEqual(is_subgroup_of_class_spec(self.rule_original, self.rule_candidate_correct2), False)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_original, self.rule_candidate_correct3), False)
        self.assertEqual(is_subgroup_of_class_spec(self.rule_original, self.rule_candidate_correct4), False)

    def test_is_equivalent_class_spec_double_wildcard(self):
        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_correct1, self.rule_original2), True)
        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_correct2, self.rule_original2), True)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_correct3, self.rule_original2), True)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_incorrect, self.rule_original2), False)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_original2, self.rule_candidate_correct1), False)
        self.assertEqual(is_subgroup_of_class_spec(self.rule_original2, self.rule_candidate_correct2), False)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_original2, self.rule_candidate_correct3), False)

    def test_is_equivalent_class_spec_end_double_wildcards(self):
        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_correct1, self.rule_original3), True)
        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_correct2, self.rule_original3), True)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_correct3, self.rule_original3), True)
        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_correct4, self.rule_original3), True)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_incorrect, self.rule_original3), False)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_original3, self.rule_candidate_correct1), False)
        self.assertEqual(is_subgroup_of_class_spec(self.rule_original3, self.rule_candidate_correct2), False)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_original3, self.rule_candidate_correct3), False)
        self.assertEqual(is_subgroup_of_class_spec(self.rule_original3, self.rule_candidate_correct4), False)

    def test_is_equivalent_class_spec_end_single_wildcards(self):
        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_correct1, self.rule_original4), True)
        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_correct2, self.rule_original4), True)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_correct3, self.rule_original4), True)
        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_correct4, self.rule_original4), True)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_candidate_incorrect, self.rule_original4), False)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_original4, self.rule_candidate_correct1), False)
        self.assertEqual(is_subgroup_of_class_spec(self.rule_original4, self.rule_candidate_correct2), False)

        self.assertEqual(is_subgroup_of_class_spec(self.rule_original4, self.rule_candidate_correct3), False)
        self.assertEqual(is_subgroup_of_class_spec(self.rule_original4, self.rule_candidate_correct4), False)

    def test_is_equivalent_rule(self):
        self.assertEqual(is_equivalent_rule(self.rule_original_real, self.rule_candidate_real), True)
