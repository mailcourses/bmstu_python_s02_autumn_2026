from unittest import TestCase, mock

from user import User


class TestUser(TestCase):

    def test_init(self):
        steve = User("steve", 99)
        self.assertEqual(steve.name, "steve")
        self.assertEqual(steve.age, 99)

    def test_greetings(self):
        steve = User("steve", 99)

        self.assertEqual(steve.name, "steve")
        self.assertEqual("Hello, steve!", steve.greetings())

    def test_birthday(self):
        steve = User("steve", 99)

        self.assertEqual(steve.age, 99)
        self.assertEqual(100, steve.birthday())
        self.assertEqual(steve.age, 100)

    def test_get_friends_current_impl(self):
        steve = User("steve", 99)

        with self.assertRaises(NotImplementedError):
            steve.get_friends()

    def test_get_friends_empty(self):
        steve = User("steve", 99)

        with mock.patch("user.fetch_vk_api") as fetch_mock:
            self.assertEqual([], steve.get_friends(name_part="neo"))

            calls = [
                mock.call("/friends", "steve", part="NEO"),
                mock.call().__iter__(),
            ]
            self.assertEqual(calls, fetch_mock.mock_calls)

    def test_get_friends_single(self):
        steve = User("steve", 99)

        with mock.patch("user.fetch_vk_api") as fetch_mock:
            fetch_mock.return_value = ["neo", "morf"]

            self.assertEqual(["neo", "morf"], steve.get_friends())
            calls = [
                mock.call("/friends", "steve", part=None),
            ]
            self.assertEqual(calls, fetch_mock.mock_calls)

            self.assertEqual(["neo"], steve.get_friends(name_part="n"))
            calls = [
                mock.call("/friends", "steve", part=None),
                mock.call("/friends", "steve", part="N"),
            ]
            self.assertEqual(calls, fetch_mock.mock_calls)

            fetch_mock.reset_mock()
            self.assertEqual(["neo"], steve.get_friends(name_part="n"))
            calls = [
                mock.call("/friends", "steve", part="N"),
            ]
            self.assertEqual(calls, fetch_mock.mock_calls)

    def test_get_friends_error(self):
        steve = User("steve", 99)

        with mock.patch("user.fetch_vk_api") as fetch_mock:
            fetch_mock.side_effect = ValueError("wrong")

            with self.assertRaises(ValueError) as err:
                steve.get_friends()

            self.assertEqual("wrong", str(err.exception))

            calls = [
                mock.call("/friends", "steve", part=None),
            ]
            self.assertEqual(calls, fetch_mock.mock_calls)

    def test_get_friends_many(self):
        steve = User("steve", 99)

        with mock.patch("user.fetch_vk_api") as fetch_mock:
            fetch_mock.side_effect = [["neo", "morf"], [], ["neo"]]

            self.assertEqual(["neo", "morf"], steve.get_friends())
            calls = [
                mock.call("/friends", "steve", part=None),
            ]
            self.assertEqual(calls, fetch_mock.mock_calls)

            fetch_mock.reset_mock()
            self.assertEqual([], steve.get_friends(name_part="n"))
            calls = [
                mock.call("/friends", "steve", part="N"),
            ]
            self.assertEqual(calls, fetch_mock.mock_calls)

            fetch_mock.reset_mock()
            self.assertEqual(["neo"], steve.get_friends(name_part="neo"))
            calls = [
                mock.call("/friends", "steve", part="NEO"),
            ]
            self.assertEqual(calls, fetch_mock.mock_calls)

    def test_get_friends_lambda(self):
        steve = User("steve", 99)

        with mock.patch("user.fetch_vk_api") as fetch_mock:
            fetch_mock.side_effect = lambda *a, **kw: ["neo"]

            self.assertEqual(["neo"], steve.get_friends())
            calls = [
                mock.call("/friends", "steve", part=None),
            ]
            self.assertEqual(calls, fetch_mock.mock_calls)

            self.assertEqual([], steve.get_friends(name_part="qwerty"))
            calls = [
                mock.call("/friends", "steve", part=None),
                mock.call("/friends", "steve", part="QWERTY"),
            ]
            self.assertEqual(calls, fetch_mock.mock_calls)

    def test_get_friends_count(self):
        steve = User("steve", 99)
        lst = []
        def count_calls(*args, **kwargs):
            lst.append(1)
            return ["neo"]

        with mock.patch("user.fetch_vk_api") as fetch_mock:
            fetch_mock.side_effect = count_calls

            self.assertEqual(["neo"], steve.get_friends())
            calls = [
                mock.call("/friends", "steve", part=None),
            ]
            self.assertEqual(calls, fetch_mock.mock_calls)
            self.assertEqual(lst, [1])

            self.assertEqual([], steve.get_friends(name_part="qwerty"))
            calls = [
                mock.call("/friends", "steve", part=None),
                mock.call("/friends", "steve", part="QWERTY"),
            ]
            self.assertEqual(calls, fetch_mock.mock_calls)
            self.assertEqual(lst, [1, 1])

