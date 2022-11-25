# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: template.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import proto.minutia_pb2 as minutia__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='template.proto',
  package='',
  syntax='proto3',
  serialized_options=b'H\003',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0etemplate.proto\x1a\rminutia.proto\"\x1a\n\tVectorMCC\x12\r\n\x05value\x18\x01 \x03(\x08\"\x96\x01\n\x08Template\x12\r\n\x05width\x18\x01 \x01(\x05\x12\x0e\n\x06height\x18\x02 \x01(\x05\x12\x15\n\rnfiq1_quality\x18\x03 \x01(\x02\x12\x15\n\rnfiq2_quality\x18\x04 \x01(\x02\x12\x1e\n\nminutiaepb\x18\x05 \x03(\x0b\x32\n.Minutiapb\x12\x1d\n\tvectorMCC\x18\x06 \x03(\x0b\x32\n.VectorMCCB\x02H\x03\x62\x06proto3'
  ,
  dependencies=[minutia__pb2.DESCRIPTOR,])




_VECTORMCC = _descriptor.Descriptor(
  name='VectorMCC',
  full_name='VectorMCC',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='VectorMCC.value', index=0,
      number=1, type=8, cpp_type=7, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=33,
  serialized_end=59,
)


_TEMPLATE = _descriptor.Descriptor(
  name='Template',
  full_name='Template',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='width', full_name='Template.width', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='height', full_name='Template.height', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nfiq1_quality', full_name='Template.nfiq1_quality', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nfiq2_quality', full_name='Template.nfiq2_quality', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='minutiaepb', full_name='Template.minutiaepb', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='vectorMCC', full_name='Template.vectorMCC', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=62,
  serialized_end=212,
)

_TEMPLATE.fields_by_name['minutiaepb'].message_type = minutia__pb2._MINUTIAPB
_TEMPLATE.fields_by_name['vectorMCC'].message_type = _VECTORMCC
DESCRIPTOR.message_types_by_name['VectorMCC'] = _VECTORMCC
DESCRIPTOR.message_types_by_name['Template'] = _TEMPLATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

VectorMCC = _reflection.GeneratedProtocolMessageType('VectorMCC', (_message.Message,), {
  'DESCRIPTOR' : _VECTORMCC,
  '__module__' : 'template_pb2'
  # @@protoc_insertion_point(class_scope:VectorMCC)
  })
_sym_db.RegisterMessage(VectorMCC)

Template = _reflection.GeneratedProtocolMessageType('Template', (_message.Message,), {
  'DESCRIPTOR' : _TEMPLATE,
  '__module__' : 'template_pb2'
  # @@protoc_insertion_point(class_scope:Template)
  })
_sym_db.RegisterMessage(Template)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
