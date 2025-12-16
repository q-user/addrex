"""Performance test to verify <100ms response time for 95% of requests."""

import time

from starlette.testclient import TestClient

from main import app


def test_response_time_under_100ms_for_95_percent():
    """Performance load testing to verify <100ms response time for 95% of requests."""
    # This test simulates load and measures response times
    client = TestClient(app)

    response_times: list[float] = []

    # Make multiple requests to gather response time data
    for _ in range(100):  # 100 requests should be sufficient for basic testing
        start_time = time.time()
        try:
            # Make a simple request to the health check endpoint
            client.get("/health")
            end_time = time.time()

            # Record the response time in milliseconds
            response_time_ms = (end_time - start_time) * 1000
            response_times.append(response_time_ms)
        except Exception:
            # If there's an error with the request, still record the time
            end_time = time.time()
            response_time_ms = (end_time - start_time) * 1000
            response_times.append(response_time_ms)

    # Calculate the 95th percentile of response times
    response_times.sort()
    percentile_95_index = int(len(response_times) * 0.95) - 1
    percentile_95_response_time = response_times[percentile_95_index]

    # Assert that 95% of requests are under 100ms
    assert percentile_95_response_time < 100, (
        f"95th percentile response time is {percentile_95_response_time:.2f}ms, "
        f"exceeds the 100ms requirement"
    )

    print(f"95th percentile response time: {percentile_95_response_time:.2f}ms")
    print(f"Average response time: {sum(response_times)/len(response_times):.2f}ms")
    print(f"Max response time: {max(response_times):.2f}ms")


def test_single_request_response_time():
    """Test that individual requests meet the <100ms requirement."""
    client = TestClient(app)

    # Test the health endpoint
    start_time = time.time()
    response = client.get("/health")
    end_time = time.time()

    response_time_ms = (end_time - start_time) * 1000

    assert response.status_code == 200
    assert response_time_ms < 100, f"Response time {response_time_ms:.2f}ms exceeds 100ms"

    # Test the root endpoint
    start_time = time.time()
    response = client.get("/")
    end_time = time.time()

    response_time_ms = (end_time - start_time) * 1000

    assert response.status_code == 200
    assert response_time_ms < 100, f"Response time {response_time_ms:.2f}ms exceeds 100ms"
