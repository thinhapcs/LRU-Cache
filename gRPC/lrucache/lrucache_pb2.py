# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: lrucache.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0elrucache.proto\x12\x08lrucache\"\x1b\n\x0cImageRequest\x12\x0b\n\x03url\x18\x01 \x01(\t\"\x1e\n\rImageResponse\x12\r\n\x05image\x18\x01 \x01(\x0c\x32Z\n\rDownloadImage\x12I\n\x14RequestDownloadImage\x12\x16.lrucache.ImageRequest\x1a\x17.lrucache.ImageResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'lrucache_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _IMAGEREQUEST._serialized_start=28
  _IMAGEREQUEST._serialized_end=55
  _IMAGERESPONSE._serialized_start=57
  _IMAGERESPONSE._serialized_end=87
  _DOWNLOADIMAGE._serialized_start=89
  _DOWNLOADIMAGE._serialized_end=179
# @@protoc_insertion_point(module_scope)
