import os
import re
import requests
from typing import Optional
from urllib.parse import urlparse, parse_qs
from pyaxm.models import OrgDeviceActivity


def download_activity_csv(activity: OrgDeviceActivity, save_path: str = None) -> Optional[str]:
    """
    Download CSV file from activity if download URL is available.
    
    :param activity: OrgDeviceActivity object with attributes.downloadUrl property
    :param save_path: Optional path to save file (defaults to current directory)
    :return: Path to saved file or None if no download URL
    """
    if not save_path:
        save_path = os.getcwd()

    if not (activity.attributes and activity.attributes.downloadUrl):
        return None

    url = activity.attributes.downloadUrl
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    disposition = query_params['response-content-disposition'][0]
    match = re.search(r'filename="([^"]+)"', disposition)
    filename = match.group(1)
    
    file_path = os.path.join(save_path, filename)
    
    response = requests.get(url)
    response.raise_for_status()
    
    with open(file_path, 'wb') as f:
        f.write(response.content)
    
    return file_path
