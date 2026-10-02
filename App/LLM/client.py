from App.Config import keys, model_name, urls
from langchain_openrouter import ChatOpenRouter
from langchain_core.rate_limiters import InMemoryRateLimiter

rate_limiter = InMemoryRateLimiter(
    requests_per_second=1,  
    check_every_n_seconds=1, 
    max_bucket_size=10,  
)

def get_client_main(temperature = 0.3, max_tokens = 1024):

    client = ChatOpenRouter(
        base_url = urls.open_router_base_url,
        api_key = keys.open_router_key_main,
        model=model_name.qwen3,
        temperature = temperature,
        max_tokens = max_tokens,
        rate_limiter = rate_limiter
    )

    return client


def get_client_router(temperature = 0.3, max_tokens = 1024):

    client = ChatOpenRouter(
        base_url = urls.open_router_base_url,
        api_key = keys.open_router_key_router,
        model=model_name.qwen3,
        temperature = temperature,
        max_tokens = max_tokens,
        rate_limiter = rate_limiter
    )

    return client

def get_client_fallback(temperature = 0.3, max_tokens = 1024):

    client = ChatOpenRouter(
        base_url = urls.open_router_base_url,
        api_key = keys.open_router_key_fallback,
        model=model_name.qwen3,
        temperature = temperature,
        max_tokens = max_tokens,
        rate_limiter = rate_limiter
    )

    return client