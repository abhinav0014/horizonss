class SubdomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __process_request(self, request):
        domain_parts = request.get_host().split('.')
        if len(domain_parts) > 2:
            subdomain = domain_parts[0]
            if subdomain == 'admin':
                request.subdomain = 'admin'
            elif subdomain == 'dashboard':
                request.subdomain = 'dashboard'
            else:
                request.subdomain = None
        else:
            request.subdomain = None

    def __call__(self, request):
        self.__process_request(request)
        return self.get_response(request)