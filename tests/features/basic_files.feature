Feature: Extract common file types

Scenario Outline: Kai common file types
        Given a file of type "<file type>"
        When a user invokes kai on the file
        Then the file is extracted into the specified directory

        Examples: common files types
            | file type |
            | tar       |
            | zip       |
