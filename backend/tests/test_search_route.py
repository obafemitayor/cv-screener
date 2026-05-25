import asyncio
import json
import unittest
from unittest.mock import AsyncMock, patch

from app.main import app
from app.api.routes import search as search_route


async def asgi_json_request(method: str, path: str, payload: dict) -> dict[str, object]:
    body = json.dumps(payload).encode("utf-8")
    response: dict[str, object] = {"status": None, "body": bytearray()}
    request_sent = False

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method,
        "scheme": "http",
        "path": path,
        "raw_path": path.encode("utf-8"),
        "query_string": b"",
        "headers": [
            (b"host", b"testserver"),
            (b"content-type", b"application/json"),
            (b"content-length", str(len(body)).encode("utf-8")),
        ],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
        "root_path": "",
    }

    async def receive() -> dict[str, object]:
        nonlocal request_sent
        if request_sent:
            return {"type": "http.disconnect"}
        request_sent = True
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(message: dict[str, object]) -> None:
        if message["type"] == "http.response.start":
            response["status"] = message["status"]
        elif message["type"] == "http.response.body":
            response["body"].extend(message.get("body", b""))

    await app(scope, receive, send)
    response["body"] = bytes(response["body"])
    return response


def request_json(method: str, path: str, payload: dict) -> dict[str, object]:
    return asyncio.run(asgi_json_request(method, path, payload))


class SearchRouteTests(unittest.TestCase):
    def test_search_when_request_is_invalid(self) -> None:
        result = request_json("POST", "/search", {})

        self.assertEqual(result["status"], 422)

        body = json.loads(result["body"])
        self.assertIn("detail", body)

    def test_search_when_query_is_valid_but_there_is_no_matching_resume_context(self) -> None:
        payload = {
            "query": "Who has Python experience?",
            "chat_history": [],
        }

        with patch.object(search_route, "get_question", AsyncMock(return_value=payload["query"])), patch.object(
            search_route, "get_relevant_cvs_for_question", AsyncMock(return_value=[])
        ) as get_relevant_cvs_mock, patch.object(
            search_route, "generate_response_from_cvs", AsyncMock()
        ) as generate_response_mock:
            result = request_json("POST", "/search", payload)

        self.assertEqual(result["status"], 200)
        self.assertEqual(
            json.loads(result["body"]),
            {
                "response": "I could not find any indexed CV content to answer the question.",
            },
        )
        get_relevant_cvs_mock.assert_awaited_once_with(payload["query"])
        generate_response_mock.assert_not_called()

    def test_search_when_query_is_valid_and_there_is_matching_resume_context(self) -> None:
        payload = {
            "query": "Who has Python experience?",
            "chat_history": [],
        }
        matching_cvs = [
            {
                "text": "Jane Doe has Python experience.",
                "metadata": {"filename": "jane_doe.pdf"},
                "distance": 0.12,
            }
        ]

        with patch.object(search_route, "get_question", AsyncMock(return_value=payload["query"])), patch.object(
            search_route, "get_relevant_cvs_for_question", AsyncMock(return_value=matching_cvs)
        ), patch.object(
            search_route,
            "generate_response_from_cvs",
            AsyncMock(return_value={"response": "Jane Doe has Python experience."}),
        ) as generate_response_mock:
            result = request_json("POST", "/search", payload)

        self.assertEqual(result["status"], 200)
        self.assertEqual(json.loads(result["body"]), {"response": "Jane Doe has Python experience."})
        generate_response_mock.assert_awaited_once_with(payload["query"], matching_cvs)

    def test_search_query_should_be_rewritten_when_conversation_history_exists(self) -> None:
        payload = {
            "query": "What about Java?",
            "chat_history": [
                {"role": "user", "content": "Who has Python experience?"},
                {"role": "assistant", "content": "Jane Doe has Python experience."},
            ],
        }

        with patch.object(
            search_route,
            "get_question",
            AsyncMock(return_value="Which candidates have Java experience?"),
        ) as get_question_mock, patch.object(
            search_route,
            "get_relevant_cvs_for_question",
            AsyncMock(return_value=[
                {
                    "text": "John Smith has Java experience.",
                    "metadata": {"filename": "john_smith.pdf"},
                    "distance": 0.1,
                }
            ]),
        ), patch.object(
            search_route,
            "generate_response_from_cvs",
            AsyncMock(return_value={"response": "John Smith has Java experience."}),
        ):
            result = request_json("POST", "/search", payload)

        self.assertEqual(result["status"], 200)
        self.assertEqual(json.loads(result["body"]), {"response": "John Smith has Java experience."})

        forwarded_payload = get_question_mock.await_args.args[0]
        self.assertEqual(forwarded_payload.query, payload["query"])
        self.assertEqual(len(forwarded_payload.chat_history), 2)


if __name__ == "__main__":
    unittest.main()
