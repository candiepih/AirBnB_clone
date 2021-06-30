from console import HBNBCommand
import unittest
from unittest.mock import create_autospec, patch
import sys
from io import StringIO
import os


class TestConsole(unittest.TestCase):

    classes = ["BaseModel", "User", "State", "City",
               "Amenity", "Place", "Review"]

    @classmethod
    def teardown(cls):
        """ final statement """
        try:
            os.remove("file.json")
        except Exception:
            pass

    def setUp(self):
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)

    def create_session(self, server=None):
        return HBNBCommand(stdin=self.mock_stdin, stdout=self.mock_stdout)

    def test_destroy(self):
        cli = self.create_session()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('destroy'))
        self.assertEqual('** class name missing **',
                         f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('destroy obj'))
        self.assertEqual("** class doesn't exist **",
                         f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('destroy {}'.format(cls)))
            self.assertEqual("** instance id missing **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('destroy {} 123456'.format(cls)))
            self.assertEqual("** no instance found **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('all'))
            self.assertTrue(ids in f.getvalue().strip())
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('destroy {} {}'.format(cls, ids)))
            self.assertFalse(ids in f.getvalue().strip())
            self.assertEqual("", f.getvalue().strip())
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('all'))
            self.assertFalse(ids in f.getvalue().strip())

        """ <class>.destroy(<id>) method """

        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.destroy("123456")'
                                 .format(cls)))
            self.assertEqual("** no instance found **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('all'))
            self.assertTrue(ids in f.getvalue().strip())
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.destroy("{}")'
                                 .format(cls, ids)))
            self.assertFalse(ids in f.getvalue().strip())
            self.assertEqual("", f.getvalue().strip())
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('all'))
            self.assertFalse(ids in f.getvalue().strip())

    def test_all(self):
        cli = self.create_session()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('all'))
        self.assertEqual('[', f.getvalue().strip()[0])
        self.assertEqual(']', f.getvalue().strip()[-1])
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('all obj'))
        self.assertEqual("** class doesn't exist **",
                         f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('all {}'.format(cls)))
                self.assertEqual('[', f.getvalue().strip()[0])
                self.assertEqual(']', f.getvalue().strip()[-1])
            self.assertTrue(ids in f.getvalue().strip())

        """ <class>.all mode """

        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.all()'.format(cls)))
            self.assertEqual('[', f.getvalue().strip()[0])
            self.assertEqual(']', f.getvalue().strip()[-1])
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.all()'.format(cls)))
            self.assertTrue(ids in f.getvalue().strip())

    def test_update(self):
        cli = self.create_session()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('update'))
        self.assertEqual('** class name missing **',
                         f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(cli.onecmd('update obj'))
        self.assertEqual("** class doesn't exist **",
                         f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('update {}'.format(cls)))
            self.assertEqual("** instance id missing **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('update {} 123456'.format(cls)))
            self.assertEqual("** no instance found **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('update {} {}'.format(cls, ids)))
            self.assertEqual("** attribute name missing **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('update {} {} attribute'
                                 .format(cls, ids)))
            self.assertEqual("** value missing **", f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('update {} {} attribute "test"'
                                 .format(cls, ids)))
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('show {} {}'.format(cls, ids)))
            self.assertTrue("attribute" in f.getvalue().strip())
            self.assertTrue("test" in f.getvalue().strip())

        """
        <class name>.update(<id>, <attribute name>, <attribute value>)
        method
        """

        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.update()'.format(cls)))
            self.assertEqual("** instance id missing **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.update("123456")'.format(cls)))
            self.assertEqual("** no instance found **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.update("{}")'
                                 .format(cls, ids)))
            self.assertEqual("** attribute name missing **",
                             f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.update("{}", "attribute")'
                                 .format(cls, ids)))
            self.assertEqual("** value missing **", f.getvalue().strip())
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.update("{}", "attr", "test")'
                                 .format(cls, ids)))
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('show {} {}'.format(cls, ids)))
            self.assertTrue("attr" in f.getvalue().strip())
            self.assertTrue("test" in f.getvalue().strip())

        """ <class name>.update(<id>, <dictionary representation>) method """

        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
                ids = f.getvalue().strip()
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.update("{}", {{"num": 89}})'
                                 .format(cls, ids)))
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('show {} {}'.format(cls, ids)))
            self.assertTrue("num" in f.getvalue().strip())
            self.assertTrue("89" in f.getvalue().strip())

    def test_count(self):
        cli = self.create_session()
        for cls in TestConsole.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.count()'.format(cls)))
                number1 = int(f.getvalue().strip())
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('create {}'.format(cls)))
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(cli.onecmd('{}.count()'.format(cls)))
                number2 = int(f.getvalue().strip())
            self.assertTrue(number2 == number1 + 1)

    def test_quit(self):
        """exit command"""
        cli = self.create_session()
        self.assertTrue(cli.onecmd("quit"))
