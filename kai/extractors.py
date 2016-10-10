"""A bunch of extractors go here"""
import os

import six
import rarfile
import tarfile
import zipfile


class ExtractorError(Exception):
    pass


class ExtractorRegistry(type):
    registry = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.register_extractor(new_cls)
        return new_cls

    @classmethod
    def register_extractor(cls, new_cls):
        cls.registry[new_cls] = new_cls.supported_extensions


class ExtractorFactory(object):
    @classmethod
    def create(cls, filename, destination='.'):
        for extractor in ExtractorRegistry.registry:
            if extractor.supports(filename):
                return extractor(filename, destination)
        else:
            raise ExtractorError('File extension not supported.')


@six.add_metaclass(ExtractorRegistry)
class Extractor(object):
    supported_extensions = []

    def __init__(self, filename, destination='.'):
        self.filename = filename
        self.destination = destination

    @classmethod
    def supports(cls, filename):
        """
        Returns True if the extractor supports the given file
        """
        for supported_extension in cls.supported_extensions:
            if filename.endswith(supported_extension):
                return True
        return False

    def extract(self):
        raise NotImplementedError()

    @staticmethod
    def strip_extension(full_path, extension):
        return os.path.basename(full_path[:-len(extension)])


class TarExtractor(Extractor):
    supported_extensions = ['tar', 'tar.gz', 'tgz', 'tar.bz2', 'tbz']

    def extract(self):
        mode_map = {
            '.tar.gz': 'r:gz',
            '.tgz': 'r:gz',
            '.tar.bz2': 'r:bz2',
            '.tbz': 'r:bz2',
            '.tar': 'r:'}
        for file_extension, mode in mode_map.items():
            if self.filename.endswith(file_extension):
                destination = '{}{}'.format(
                    self.destination,
                    self.strip_extension(self.filename, file_extension))
                with tarfile.open(self.filename, mode) as archive:
                    archive.extractall(path=destination)
                return destination
        raise ExtractorError(
            'Failed to extract {} as tar file.'.format(self.filename))


class ZipExtractor(Extractor):
    supported_extensions = ['.zip']

    def extract(self):
        destination = '{}{}'.format(
            self.destination, self.strip_extension(self.filename, '.zip'))
        with zipfile.ZipFile(self.filename, 'r') as archive:
            archive.extractall(path=destination)
        return destination


class RarExtractor(Extractor):
    """ Extracting RAR file """
    supported_extensions = ['.rar']

    def extract(self):
        destination = '{}{}'.format(
            self.destination, self.strip_extension(self.filename, '.rar'))
        with rarfile.RarFile(self.filename, 'r') as archive:
            archive.extractall(path=destination)
        return destination
