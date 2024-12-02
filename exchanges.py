import ccxt

corretoras = {
    "binance": ccxt.binance({
        'apiKey': 'hI60zeaef7qf7pa3Geas40YftFBzxwujPuCEt2oZH6F6KqXvOXXVDOYbkOUgkLH3',
        'secret': 'h4POcGR3hyU51KtwKudX3uNuAiQNeB1jCMpK8KKA04PR7jFORcUU0hPbWJCSSFp4',
        'enableRateLimit': True,
        'options': {
            'sandbox': True,  # Ativa o modo sandbox
        },
        'timeout': 60000
    })
}