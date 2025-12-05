"""
Test script for chatbot backend
Run this after setting up the backend to verify everything works
"""

import requests
import json
import time
from typing import Dict, Any

API_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)

    try:
        response = requests.get(f"{API_URL}/health")
        data = response.json()

        print(f"✓ Status: {response.status_code}")
        print(f"✓ Overall health: {data['status']}")
        print("\nComponents:")
        for component, status in data['components'].items():
            icon = "✓" if status == "healthy" else "⚠"
            print(f"  {icon} {component}: {status}")

        return response.status_code == 200
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False


def test_chat(question: str) -> Dict[str, Any]:
    """Test the chat endpoint with a question"""
    print("\n" + "=" * 60)
    print(f"TEST: Chat with question")
    print("=" * 60)
    print(f"Question: {question}")

    try:
        start_time = time.time()

        response = requests.post(
            f"{API_URL}/chat",
            json={
                "question": question,
                "conversation_history": [],
                "week_filter": None
            }
        )

        elapsed = (time.time() - start_time) * 1000

        if response.status_code != 200:
            print(f"✗ Request failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return {}

        data = response.json()

        print(f"\n✓ Response received in {elapsed:.0f}ms")
        print(f"\nAnswer:")
        print(f"{data['answer'][:300]}..." if len(data['answer']) > 300 else data['answer'])

        print(f"\n✓ Confidence: {data['confidence'] * 100:.1f}%")
        print(f"✓ Response time: {data['response_time_ms']}ms")

        if data.get('sources'):
            print(f"\n✓ Sources ({len(data['sources'])}):")
            for i, source in enumerate(data['sources'][:3], 1):
                print(f"  {i}. {source['title']}")
                print(f"     URL: {source['url']}")
                print(f"     Similarity: {source['similarity'] * 100:.1f}%")

        # Performance check
        if data['response_time_ms'] < 3000:
            print(f"\n✓ Performance: EXCELLENT (< 3 seconds)")
        elif data['response_time_ms'] < 5000:
            print(f"\n⚠ Performance: GOOD (< 5 seconds)")
        else:
            print(f"\n⚠ Performance: SLOW (> 5 seconds)")

        return data

    except Exception as e:
        print(f"✗ Chat test failed: {e}")
        return {}


def test_feedback():
    """Test the feedback endpoint"""
    print("\n" + "=" * 60)
    print("TEST: Feedback Submission")
    print("=" * 60)

    try:
        response = requests.post(
            f"{API_URL}/feedback",
            json={
                "question": "Test question",
                "answer": "Test answer",
                "rating": 5,
                "comment": "Automated test feedback"
            }
        )

        data = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Message: {data.get('message', 'No message')}")

        return response.status_code == 200
    except Exception as e:
        print(f"✗ Feedback test failed: {e}")
        return False


def test_stats():
    """Test the stats endpoint"""
    print("\n" + "=" * 60)
    print("TEST: Statistics")
    print("=" * 60)

    try:
        response = requests.get(f"{API_URL}/stats")
        data = response.json()

        print(f"✓ Status: {response.status_code}")
        print(f"\nStatistics:")
        print(f"  Total questions: {data.get('total_questions', 0)}")
        print(f"  Avg response time: {data.get('avg_response_time_ms', 0)}ms")
        print(f"  Avg confidence: {data.get('avg_confidence', 0) * 100:.1f}%")
        print(f"  Database status: {data.get('database_status', 'unknown')}")

        return response.status_code == 200
    except Exception as e:
        print(f"✗ Stats test failed: {e}")
        return False


def run_comprehensive_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("PHYSICAL AI CHATBOT - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print(f"API URL: {API_URL}")

    results = {
        "health_check": False,
        "chat_tests": [],
        "feedback": False,
        "stats": False
    }

    # Test 1: Health check
    results["health_check"] = test_health_check()

    if not results["health_check"]:
        print("\n✗ CRITICAL: Health check failed. Make sure the backend is running.")
        print(f"  Start the backend with: uvicorn main:app --reload")
        return

    # Test 2: Chat with different questions
    test_questions = [
        "What is physical AI?",
        "Explain embodied intelligence",
        "What sensors do humanoid robots use?",
        "What is the sim-to-real gap?",
    ]

    for question in test_questions:
        result = test_chat(question)
        if result:
            results["chat_tests"].append({
                "question": question,
                "passed": True,
                "confidence": result.get("confidence", 0),
                "response_time": result.get("response_time_ms", 0)
            })
        else:
            results["chat_tests"].append({
                "question": question,
                "passed": False
            })

    # Test 3: Feedback
    results["feedback"] = test_feedback()

    # Test 4: Stats
    results["stats"] = test_stats()

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    total_tests = 1 + len(test_questions) + 2
    passed_tests = sum([
        results["health_check"],
        sum(1 for test in results["chat_tests"] if test["passed"]),
        results["feedback"],
        results["stats"]
    ])

    print(f"\nPassed: {passed_tests}/{total_tests} tests")

    if results["chat_tests"]:
        avg_confidence = sum(t.get("confidence", 0) for t in results["chat_tests"]) / len(results["chat_tests"])
        avg_response_time = sum(t.get("response_time", 0) for t in results["chat_tests"]) / len(results["chat_tests"])

        print(f"\nAverage confidence: {avg_confidence * 100:.1f}%")
        print(f"Average response time: {avg_response_time:.0f}ms")

    if passed_tests == total_tests:
        print("\n✓ ALL TESTS PASSED!")
        print("\n🎉 Your chatbot is working correctly!")
        print("\nNext steps:")
        print("1. Integrate the ChatBot component into your Docusaurus site")
        print("2. Test with real users and collect feedback")
        print("3. Deploy the backend to production (Railway/Render)")
    else:
        print(f"\n⚠ Some tests failed ({total_tests - passed_tests} failures)")
        print("\nTroubleshooting:")
        print("- Make sure the backend is running: uvicorn main:app --reload")
        print("- Check that Qdrant is accessible")
        print("- Verify your OpenAI API key is valid")
        print("- Ensure the collection has been created: python ingest.py")


if __name__ == "__main__":
    run_comprehensive_tests()
