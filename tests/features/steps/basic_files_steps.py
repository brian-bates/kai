import hashlib
import os
import tarfile
import zipfile

from behave import given, when, then

from kai import extract


def compute_hash(filename):
    """Returns the MD5 hash of the specified file"""
    with open(filename, 'r') as f:
        contents = f.read().encode('utf-8')
        return hashlib.md5(contents).digest()


def create_dummy_file(filename='lorem-ipsum.txt', base_dir='.'):
    """Create a dummy text file with arbitrary contents"""
    path = os.path.join(base_dir, filename)
    with open(path, 'w') as f:
        f.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit, '
                'sed do eiusmod tempor incididunt ut labore et dolore magna'
                'aliqua.')
    return filename, path


def _create_zip_archive(path, contents):
    with zipfile.ZipFile(path, 'w') as archive:
        for inner_file in contents:
            archive.write(inner_file, arcname=os.path.basename(inner_file))


def _create_tar_archive(path, contents):
    with tarfile.open(path, 'w') as archive:
        for inner_file in contents:
            archive.add(inner_file, arcname=os.path.basename(inner_file))


def create_archive(file_type, base_dir, contents):
    """Create archive of the specified file type with the given contents

    Returns the path to the created archive.

    Args:
        file_type: The type of archive to create.
        base_dir:  The directory where the archive should be created.
        contents:  List of paths to files that should be inluded in the
                   archive.
    """
    archiver = {'tar': _create_tar_archive,
                'zip': _create_zip_archive}
    filename = 'test.{}'.format(file_type)
    path = os.path.join(base_dir, filename)
    archiver[file_type](path, contents)
    return path


@given(u'a file of type "{file_type}"')
def step_generate_test_archive(context, file_type):
    """Generate a dummy archive of the speficied type for testing

    Stores the path to a dummy archive and hash values of its contents in the
    current context.

    Args:
        context:   Behave's current testing context.
        file_type: The file extension for the type of archive to generate.
    """
    filename, path = create_dummy_file(base_dir=context.test_dir)
    context.expected_hash = {filename: compute_hash(path)}
    context.archive = create_archive(file_type, context.test_dir, [path])


@when(u'a user invokes kai on the file')
def step_invoke_kai(context):
    """Invokes kai on the archive provided in context"""
    context.extracted_dir = extract(context.archive, context.test_dir)


@then(u'the file is extracted into the specified directory')
def step_verify_contents(context):
    for filename, expected in context.expected_hash.items():
        path = os.path.join(context.extracted_dir, filename)
        actual = compute_hash(path)
        assert expected == actual, (
            'Failure: Extracted files are different:'
            '\nExpected {}\nReceived {}').format(expected, actual)
