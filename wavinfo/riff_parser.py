
import struct
from collections import namedtuple
from .rf64_parser import parse_rf64


class WavInfoEOFError(EOFError):
    def __init__(self, identifier, chunk_start):
        self.identifier = identifier
        self.chunk_start = chunk_start


class ListChunkDescriptor(namedtuple('ListChunkDescriptor', 'signature children')):
    def find(self, chunk_path):
        if len(chunk_path) > 1:
            for chunk in self.children:
                if type(chunk) is ListChunkDescriptor and \
                        chunk.signature is chunk_path[0]:
                    return chunk.find(chunk_path[1:])
        else:
            for chunk in self.children:
                if type(chunk) is ChunkDescriptor and \
                        chunk.ident is chunk_path[0]:
                    return chunk


class ChunkDescriptor(namedtuple('ChunkDescriptor', 'ident start length rf64_context')):
    def read_data(self, from_stream):
        from_stream.seek(self.start)
        return from_stream.read(self.length)


def parse_list_chunk(stream, length, rf64_context=None):
    start = stream.tell()

    signature = stream.read(4)

    children = []
    while (stream.tell() - start) < length:
        child_chunk = parse_chunk(stream, rf64_context=rf64_context)
        if child_chunk:
            children.append(child_chunk)
        else: 
            break

    return ListChunkDescriptor(signature=signature, children=children)


def parse_chunk(stream, rf64_context=None):
    ident = stream.read(4)
    size_bytes = stream.read(4)

    if len(ident) != 4 or len(size_bytes) < 4:
        raise WavInfoEOFError(identifier=ident, chunk_start=stream.tell() - 4)

    size_bytes = stream.read(4)
    size = struct.unpack('<I', size_bytes)[0]
    
    if size == 0xFFFFFFFF:
        if rf64_context is None and ident == b'RF64':
            rf64_context = parse_rf64(stream=stream)
        
        size = rf64_context.bigchunk_table[ident] 
            
    displacement = size
    if displacement % 2 is not 0:
        displacement = displacement + 1

    if ident in [b'RIFF', b'LIST', b'RF64']:
        return parse_list_chunk(stream=stream, length=size, rf64_context=rf64_context)
    else:
        start = stream.tell()
        stream.seek(displacement, 1)
        return ChunkDescriptor(ident=ident, start=start, length=size, rf64_context=rf64_context)
