class CompressionFileError(Exception):
    pass


class ArchiveContentError(CompressionFileError):
    pass


class ArchiveCompressionRatioExceeded(ArchiveContentError):
    pass


class ArchiveInputSizeExceeded(ArchiveContentError):
    pass


class ArchiveMemberSizeExceeded(ArchiveContentError):
    pass


class NoMIMETypeMatch(CompressionFileError):
    pass
