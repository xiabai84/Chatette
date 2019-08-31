#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO shouldn't generate twice the same statement

from chatette.utils import print_DBG, remove_duplicates, UnitType
from chatette.units.ast import AST


class Generator(object):
    """
    Using the info parsed from the input file, this class will generate
    a Rasa NLU dataset and dump it in a JSON file.
    If there were inconsistencies in the input file, they are likely to be
    detected here.
    """
    def __init__(self):
        self.ast = AST.get_or_create()

    def generate_train(self):
        print_DBG("Generating training examples...")
        intent_definitions = self.ast[UnitType.intent]
        for intent_name in intent_definitions:
            intent = intent_definitions[intent_name]
            examples = intent.generate_train()
            for example in examples:
                yield example

    def generate_test(self, training_examples=None):
        should_generate_test_set = False

        intent_definitions = self.ast[UnitType.intent]
        for intent_name in intent_definitions:
            if (
                intent_definitions[intent_name].get_nb_testing_examples_asked \
                is not None
            ):
                should_generate_test_set = True
                break

        if should_generate_test_set:
            print_DBG("Generating testing examples...")
            for intent_name in intent_definitions:
                intent = intent_definitions[intent_name]
                examples = intent.generate_test(training_examples)
                for example in examples:
                    yield example

    def get_entities_synonyms(self):  # TODO move that into AST
        """
        Makes a dict of all the synonyms of entities
        based on the slot value they are assigned.
        """
        synonyms = dict()
        for slot_definition in self.ast[UnitType.slot]:
            current_synonyms_dict = \
                self.ast[UnitType.slot][slot_definition].get_synonyms_dict()
            for slot_value in current_synonyms_dict:
                if slot_value not in synonyms:
                    synonyms[slot_value] = current_synonyms_dict[slot_value]
                else:
                    synonyms[slot_value].extend(current_synonyms_dict[slot_value])
        return remove_duplicates(synonyms)


if __name__ == "__main__":
    # pylint: disable=wrong-import-position
    # pylint: disable=wrong-import-order
    import warnings

    warnings.warn("You are running the wrong file ('generator.py')." +
                  "The file that should be run is '__main__.py'.")
