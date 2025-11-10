"""
Custom middleware for enhanced HTTPS and security monitoring.
"""

import logging
from django.http import HttpResponsePermanentRedirect
from django.conf import settings

logger = logging.getLogger('django.security.https')

class HTTPSRedirectMiddleware:
    """
    Custom middleware to enforce HTTPS redirects and log security events.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log incoming request information for security monitoring
        self.log_request_info(request)
        
        # Check if HTTPS redirect is needed
        response = self.enforce_https(request)
        if response:
            return response
        
        # Process the request normally
        response = self.get_response(request)
        
        # Add security headers to response
        response = self.add_security_headers(response)
        
        return response

    def log_request_info(self, request):
        """Log request information for security monitoring."""
        secure = request.is_secure()
        protocol = 'HTTPS' if secure else 'HTTP'
        
        logger.info(
            f"{protocol} Request: {request.method} {request.path} "
            f"from {request.META.get('REMOTE_ADDR', 'Unknown IP')} "
            f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}"
        )

    def enforce_https(self, request):
        """
        Enforce HTTPS redirect if configured and request is not secure.
        """
        if (settings.SECURE_SSL_REDIRECT and 
            not request.is_secure() and 
            not any(header in request.path for header in ['/health/', '/ping/'])):
            
            # Build the secure URL
            secure_url = request.build_absolute_uri(request.get_full_path())
            secure_url = secure_url.replace('http://', 'https://', 1)
            
            logger.warning(
                f"HTTPS Redirect: Redirecting HTTP request to HTTPS - "
                f"From: {request.build_absolute_uri()} "
                f"To: {secure_url} "
                f"IP: {request.META.get('REMOTE_ADDR', 'Unknown')}"
            )
            
            return HttpResponsePermanentRedirect(secure_url)
        
        return None

    def add_security_headers(self, response):
        """
        Add additional security headers to the response.
        """
        # These headers complement Django's built-in security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'same-origin'
        
        # Add Strict-Transport-Security if using HTTPS
        if (hasattr(settings, 'SECURE_HSTS_SECONDS') and 
            settings.SECURE_HSTS_SECONDS > 0 and 
            'Strict-Transport-Security' not in response):
            
            hsts_value = f"max-age={settings.SECURE_HSTS_SECONDS}"
            if getattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS', False):
                hsts_value += "; includeSubDomains"
            if getattr(settings, 'SECURE_HSTS_PRELOAD', False):
                hsts_value += "; preload"
            
            response['Strict-Transport-Security'] = hsts_value
        
        return response


class SecurityHeadersMiddleware:
    """
    Middleware to add comprehensive security headers.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Security headers that should be on all responses
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
        }
        
        for header, value in security_headers.items():
            if header not in response:
                response[header] = value
        
        return response
