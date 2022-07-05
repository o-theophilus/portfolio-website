import unittest
import requests
import json

host = "http://127.0.0.1:5000"


class TeatAPI(unittest.TestCase):

    def test_status_code(self):
        resp = requests.post(
            f"{host}/entity",
            headers={
                'Content-type': 'application/json'
            },
            data=json.dumps({
                "type": "blog_post",
                "title": "How I met Svelte",
                "description": "The new reactive component based approach.",
                "photo": "how-i-met-svelte-01.jpg",
                "content": "<a href='{0}'> Click here </a>",
                "format": "markdown"
            })
        )

        status_code = resp.status_code
        resp = resp.json()

        self.assertEqual(status_code, 200, "Should be 200")
        self.assertEqual(resp["message"], "successful",
                         "Should be 'successful'")
        self.assertEqual(resp["status"], 200, "Should be 200")


if __name__ == '__main__':
    unittest.main()
