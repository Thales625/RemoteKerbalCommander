# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: greet.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bgreet.proto\x12\x0c\x43\x61meraStream\"q\n\x17SendCameraStreamRequest\x12\x10\n\x08\x63\x61meraId\x18\x01 \x01(\t\x12\x12\n\ncameraName\x18\x02 \x01(\t\x12\r\n\x05speed\x18\x03 \x01(\t\x12\x10\n\x08\x61ltitude\x18\x04 \x01(\t\x12\x0f\n\x07texture\x18\x05 \x01(\x0c\"\x18\n\x16SendCameraStreamResult\"\x1b\n\x19GetActiveCameraIdsRequest\"+\n\x18GetActiveCameraIdsResult\x12\x0f\n\x07\x63\x61meras\x18\x01 \x03(\t\"+\n\x17GetCameraTextureRequest\x12\x10\n\x08\x63\x61meraId\x18\x01 \x01(\t\"p\n\x16GetCameraTextureResult\x12\x10\n\x08\x63\x61meraId\x18\x01 \x01(\t\x12\x12\n\ncameraName\x18\x02 \x01(\t\x12\r\n\x05speed\x18\x03 \x01(\t\x12\x10\n\x08\x61ltitude\x18\x04 \x01(\t\x12\x0f\n\x07texture\x18\x05 \x01(\x0c\"\x16\n\x14GetAverageFpsRequest\")\n\x13GetAverageFpsResult\x12\x12\n\naverageFps\x18\x01 \x01(\x05\x32\x8f\x03\n\x0c\x43\x61meraStream\x12_\n\x10SendCameraStream\x12%.CameraStream.SendCameraStreamRequest\x1a$.CameraStream.SendCameraStreamResult\x12\x65\n\x12GetActiveCameraIds\x12\'.CameraStream.GetActiveCameraIdsRequest\x1a&.CameraStream.GetActiveCameraIdsResult\x12_\n\x10GetCameraTexture\x12%.CameraStream.GetCameraTextureRequest\x1a$.CameraStream.GetCameraTextureResult\x12V\n\rGetAverageFps\x12\".CameraStream.GetAverageFpsRequest\x1a!.CameraStream.GetAverageFpsResultB&\xaa\x02#OfCourseIStillLoveYou.Communicationb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'greet_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\252\002#OfCourseIStillLoveYou.Communication'
  _globals['_SENDCAMERASTREAMREQUEST']._serialized_start=29
  _globals['_SENDCAMERASTREAMREQUEST']._serialized_end=142
  _globals['_SENDCAMERASTREAMRESULT']._serialized_start=144
  _globals['_SENDCAMERASTREAMRESULT']._serialized_end=168
  _globals['_GETACTIVECAMERAIDSREQUEST']._serialized_start=170
  _globals['_GETACTIVECAMERAIDSREQUEST']._serialized_end=197
  _globals['_GETACTIVECAMERAIDSRESULT']._serialized_start=199
  _globals['_GETACTIVECAMERAIDSRESULT']._serialized_end=242
  _globals['_GETCAMERATEXTUREREQUEST']._serialized_start=244
  _globals['_GETCAMERATEXTUREREQUEST']._serialized_end=287
  _globals['_GETCAMERATEXTURERESULT']._serialized_start=289
  _globals['_GETCAMERATEXTURERESULT']._serialized_end=401
  _globals['_GETAVERAGEFPSREQUEST']._serialized_start=403
  _globals['_GETAVERAGEFPSREQUEST']._serialized_end=425
  _globals['_GETAVERAGEFPSRESULT']._serialized_start=427
  _globals['_GETAVERAGEFPSRESULT']._serialized_end=468
  _globals['_CAMERASTREAM']._serialized_start=471
  _globals['_CAMERASTREAM']._serialized_end=870
# @@protoc_insertion_point(module_scope)