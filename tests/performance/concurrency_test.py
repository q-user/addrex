"""Performance test to verify concurrent user support."""

import concurrent.futures

from starlette.testclient import TestClient

from main import app


def test_concurrent_user_support():
    """Concurrent user testing to verify the application can handle multiple requests."""
    # This test simulates concurrent requests using threads to verify the application
    # can handle multiple requests without errors
    num_concurrent_requests = 50

    def make_request():
        """Make a single request and return the response."""
        try:
            client = TestClient(app)
            response = client.get("/health")
            return response.status_code
        except Exception:
            # Return an error status code if the request fails
            return 500

    # Execute all requests concurrently using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent_requests) as executor:
        # Create tasks for concurrent requests
        futures = [executor.submit(make_request) for _ in range(num_concurrent_requests)]

        # Collect results
        results = [future.result() for future in futures]

        # Count successful responses
        successful_responses = sum(1 for r in results if r == 200)
        failed_responses = num_concurrent_requests - successful_responses

        # For the test to pass, we expect most requests to succeed
        # In a real implementation with a full database and Redis, we'd expect all to pass
        assert successful_responses >= num_concurrent_requests * 0.95, (
            f"Only {successful_responses}/{num_concurrent_requests} requests succeeded, "
            f"which is less than the expected 95% success rate"
        )

        print(f"Successful responses: {successful_responses}/{num_concurrent_requests}")
        print(f"Failed responses: {failed_responses}")


def test_higher_concurrency_load():
    """Test with higher concurrency load to stress test the application."""
    # Test with 100 concurrent requests to simulate higher load
    num_concurrent_requests = 100

    def make_request():
        """Make a single request and return the response."""
        try:
            client = TestClient(app)
            response = client.get("/")
            return response.status_code
        except Exception:
            return 500

    # Execute all requests concurrently using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent_requests) as executor:
        # Create tasks for concurrent requests
        futures = [executor.submit(make_request) for _ in range(num_concurrent_requests)]

        # Collect results
        results = [future.result() for future in futures]

        # Count successful responses
        successful_responses = sum(1 for r in results if r == 200)
        failed_responses = num_concurrent_requests - successful_responses

        # Even under higher load, we expect a high success rate
        assert successful_responses >= num_concurrent_requests * 0.90, (
            f"Under high load, only {successful_responses}/{num_concurrent_requests} "
            f"requests succeeded, which is less than the expected 90% success rate"
        )

        print(f"High load test - Successful responses: {successful_responses}/{num_concurrent_requests}")
        print(f"High load test - Failed responses: {failed_responses}")
