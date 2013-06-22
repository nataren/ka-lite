"""
For functions mucking with internet access
"""
import logging
import requests

def am_i_online(url, expected_val=None, search_string=None, timeout=5, allow_redirects=True):
    """Test whether we are online or not.
    returns True or False.  
    Eats all exceptions!
    """
    assert not (search_string and expected_val is not None), "Search string and expected value cannot both be set"

    try:
        if not search_string and expected_val is None:
            response = requests.head(url)
        else:
            response = requests.get(url, timeout=timeout, allow_redirects=allow_redirects)

        # Validate that response came from the requested url
        if response.status_code != 200:
            return False
        elif not allow_redirects and response.url != url:
            return False
        
        # Check the output, if expected values are specified
        if expected_val is not None:
            return expected_val == response.text
        elif search_string:
            return search_string in response.text
        
        return True
        
    except Exception as e:
        logging.getLogger("kalite").debug("am_i_online: %s" % e)
        return False



def generate_all_paths(path, base_path="/"):

    if not base_path.endswith("/"):   # Must have trailing slash to work.
        base_path += "/"
        
    if not path.endswith("/"):        # Must NOT have trailing slash to work.
        path = path[0:-1]
        
    all_paths = []
    cur_path = base_path[0:-1]
    for dirname in path[len(base_path)-1:].split("/"): # start AFTER the base path
        cur_path += dirname + "/"
        all_paths.append(cur_path)
    return all_paths


if __name__ == "__main__":
    print generate_all_paths("/test/me/out")
    print generate_all_paths("/test/me/out/")
    print generate_all_paths("/test/me/out", base_path="/test")
    
    print am_i_online()