import pytest
from unittest.mock import MagicMock, patch
from myapp.services.mistral_service import ask_mistral

# Mock response for the Mistral API
mock_response = {
    "choices": [
        {
            "message": {
                "content": "The best French cheese is Camembert.",
            }
        }
    ]
}

@patch("myapp.services.mistral_service.Mistral")  # Mock the Mistral client
def test_ask_mistral_success(mock_mistral_class):
    """
    Test ask_mistral returns the expected response when the API call is successful.
    """
    # Mock the Mistral instance and its methods
    mock_client = MagicMock()
    mock_client.chat.complete.return_value = mock_response
    mock_mistral_class.return_value = mock_client

    question = "What is the best French cheese?"
    response = ask_mistral(question)

    # Assertions
    assert response == "The best French cheese is Camembert."
    mock_mistral_class.assert_called_once()  # Ensure Mistral was instantiated
    mock_client.chat.complete.assert_called_once_with(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": question}],
    )


@patch("myapp.services.mistral_service.Mistral")  # Mock the Mistral client
def test_ask_mistral_no_api_key(mock_mistral_class, monkeypatch):
    """
    Test ask_mistral raises an error if the API key is not set.
    """
    # Remove the API key from the environment
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)

    question = "What is the best French cheese?"

    with pytest.raises(ValueError, match="MISTRAL_API_KEY is not set"):
        ask_mistral(question)

    # Ensure Mistral was never instantiated
    mock_mistral_class.assert_not_called()


@patch("myapp.services.mistral_service.Mistral")  # Mock the Mistral client
def test_ask_mistral_api_error(mock_mistral_class):
    """
    Test ask_mistral handles API errors gracefully.
    """
    # Mock the Mistral instance to raise an exception
    mock_client = MagicMock()
    mock_client.chat.complete.side_effect = Exception("API Error")
    mock_mistral_class.return_value = mock_client

    question = "What is the best French cheese?"

    with pytest.raises(Exception, match="API Error"):
        ask_mistral(question)

    # Ensure the Mistral client was called
    mock_mistral_class.assert_called_once()
    mock_client.chat.complete.assert_called_once_with(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": question}],
    )
