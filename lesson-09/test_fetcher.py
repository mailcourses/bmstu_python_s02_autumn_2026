import unittest
from unittest import mock

from fetcher import fetch_url, fetch_batch_urls


class TestFetcher(unittest.IsolatedAsyncioTestCase):

    async def test_fetch_url(self):
        with mock.patch("fetcher.aiohttp.ClientSession.get") as mget:
            text_mock = mock.AsyncMock(return_value="orig_text")
            resp_mock = mock.AsyncMock(text=text_mock)

            mget.return_value.__aenter__.return_value = resp_mock

            result = await fetch_url("url1")

            self.assertEqual("orig_text", result)

            expected_calls = [
                mock.call("url1"),
                mock.call().__aenter__(),
                mock.call().__aenter__().text(),
                mock.call().__aexit__(None, None, None),
            ]
            self.assertEqual(expected_calls, mget.mock_calls)

            self.assertTrue(text_mock.awaited)
            text_mock.assert_awaited_once_with()

            self.assertTrue(mget.awaited)

    async def test_fetch_url_error(self):
        with mock.patch("fetcher.aiohttp.ClientSession.get") as mget:
            mget.return_value.__aenter__.side_effect = ValueError("wrong connection")

            with self.assertRaises(ValueError) as err:
                await fetch_url("url1")

            expected_calls = [
                mock.call("url1"),
                mock.call().__aenter__(),
            ]
            self.assertEqual(expected_calls, mget.mock_calls)
            self.assertTrue(mget.awaited)

    async def test_fetch_batch_urls(self):
        resps = {f"url_{i}": f"resp_{i}" for i in range(3)}

        with mock.patch("fetcher.aiohttp.ClientSession.get") as mget:
            text_mock = mock.AsyncMock(side_effect=resps.values())
            resp_mock = mock.AsyncMock(text=text_mock)

            mget.return_value.__aenter__.return_value = resp_mock

            result = await fetch_batch_urls(resps.keys())

            self.assertEqual(["resp_0", "resp_1", "resp_2"], result)

            expected_calls = []
            for url in resps.keys():
                expected_calls.extend(
                    [
                        mock.call(url),
                        mock.call().__aenter__(),
                        mock.call().__aenter__().text(),
                        mock.call().__aexit__(None, None, None),
                    ]
                )
            self.assertEqual(expected_calls, mget.mock_calls)

            self.assertTrue(text_mock.awaited)
            self.assertEqual(3, text_mock.await_count)
            text_mock.assert_has_awaits([mock.call(), mock.call(), mock.call()])

            self.assertTrue(mget.awaited)


if __name__ == "__main__":
    unittest.main()
