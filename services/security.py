def get_security_info(response):
    if "Strict-Transport-Security" in response.headers:
        hsts = True
    else:
        hsts = False
    if "Content-Security-Policy" in response.headers:
        csp = True
    else:
        csp = False
    if "X-Frame-Options" in response.headers:
        x_frame_options = True
    else:
        x_frame_options = False

    return hsts, csp, x_frame_options
