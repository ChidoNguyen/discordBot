import pytest , os
os.environ["TEST_MODE"] = '1'

from unittest.mock import patch
from scripts.auto_bot_setup import create_user_save_dir

'''
with patch -> better for block code testing ( context manager)
@patch -> better for entire test script (Decorator)
'''
def test_user_folder_creation(tmp_path):
    test_requester = "robboTest"
    fake_download_dir = str(tmp_path)
    with patch("scripts.auto_bot_setup.download_dir",fake_download_dir):
        user_folder = create_user_save_dir(test_requester)
        
        #Expectation : folder to be created
        expected_path = os.path.join(fake_download_dir,test_requester)

        #path creation string check
        #path exists
        #path is a folder and not file
        assert user_folder == expected_path
        assert os.path.exists(user_folder)
        assert os.path.isdir(user_folder)


