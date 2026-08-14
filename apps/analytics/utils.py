import re
from user_agents import parse


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_device_info(user_agent_string):
    """Parse user agent to get device information"""
    if not user_agent_string:
        return {
            'device_type': 'unknown',
            'browser': 'unknown',
            'os': 'unknown'
        }
    
    try:
        user_agent = parse(user_agent_string)
        
        if user_agent.is_mobile:
            device_type = 'mobile'
        elif user_agent.is_tablet:
            device_type = 'tablet'
        elif user_agent.is_pc:
            device_type = 'desktop'
        else:
            device_type = 'unknown'
        
        browser = user_agent.browser.family if user_agent.browser else 'unknown'
        os = user_agent.os.family if user_agent.os else 'unknown'
        
        return {
            'device_type': device_type,
            'browser': browser,
            'os': os,
        }
    except:
        return {
            'device_type': 'unknown',
            'browser': 'unknown',
            'os': 'unknown'
        }


def generate_session_id(request):
    """Generate or get session ID for tracking unique visitors"""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def get_browser_info(user_agent_string):
    """Get browser information from user agent"""
    if not user_agent_string:
        return {'browser': 'unknown', 'version': 'unknown'}
    
    try:
        user_agent = parse(user_agent_string)
        return {
            'browser': user_agent.browser.family if user_agent.browser else 'unknown',
            'version': user_agent.browser.version_string if user_agent.browser else 'unknown',
        }
    except:
        return {'browser': 'unknown', 'version': 'unknown'}


def get_os_info(user_agent_string):
    """Get operating system information from user agent"""
    if not user_agent_string:
        return {'os': 'unknown', 'version': 'unknown'}
    
    try:
        user_agent = parse(user_agent_string)
        return {
            'os': user_agent.os.family if user_agent.os else 'unknown',
            'version': user_agent.os.version_string if user_agent.os else 'unknown',
        }
    except:
        return {'os': 'unknown', 'version': 'unknown'}