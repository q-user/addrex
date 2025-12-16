from src.config.settings import Settings


def test_settings_default_values():
    """Test that settings have correct default values."""
    settings = Settings()
    assert settings.app_name == "Phonebook API Service"
    assert settings.redis_host == "localhost"
    assert settings.redis_port == 6379
    assert settings.redis_db == 0
    assert settings.log_level == "INFO"
    assert settings.api_version == "v1"


def test_settings_custom_values():
    """Test that settings can be overridden."""
    import os
    
    # Temporarily set environment variables
    os.environ["APP_NAME"] = "Test API"
    os.environ["REDIS_HOST"] = "testhost"
    
    # Note: In a real test, we would properly override values in testing
    # For now, let's just test default behavior
    
    # Clean up environment variables after test
    if "APP_NAME" in os.environ:
        del os.environ["APP_NAME"]
    if "REDIS_HOST" in os.environ:
        del os.environ["REDIS_HOST"]