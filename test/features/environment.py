import shutil
import tempfile


def before_all(context):
    """Create a temporary directory to house the test files"""
    context.test_dir = tempfile.mkdtemp()


def after_all(context):
    """Remove the directory after the tests are complete"""
    shutil.rmtree(context.test_dir)
