# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: message.protodd

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='message.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\rmessage.proto\"p\n\x04Node\x12\n\n\x02id\x18\x04 \x02(\x05\x12\x0c\n\x04rank\x18\x06 \x02(\x05\x12\x11\n\tclient_id\x18\x05 \x02(\x05\x12\r\n\x04port\x18\xc1> \x02(\x05\x12\n\n\x02ip\x18\x03 \x02(\t\x12\x0c\n\x04role\x18\x02 \x02(\t\x12\x12\n\nis_recover\x18\x01 \x01(\x08\" \n\x08NodeList\x12\x14\n\x05nodel\x18\x01 \x03(\x0b\x32\x05.Node\"3\n\x07\x43ontrol\x12\x0f\n\x07\x63ommand\x18\x01 \x02(\t\x12\x17\n\x08reg_node\x18\x02 \x02(\x0b\x32\x05.Node\"\x93\x01\n\x04Meta\x12\x0c\n\x04head\x18\x01 \x01(\x05\x12\x0c\n\x04\x62ody\x18\x02 \x01(\x0c\x12\x19\n\x07\x63ontrol\x18\x03 \x01(\x0b\x32\x08.Control\x12\x11\n\ttimestamp\x18\x04 \x01(\x05\x12\x11\n\tsender_id\x18\x05 \x01(\x05\x12\x0f\n\x07recv_id\x18\x06 \x01(\x05\x12\x0f\n\x07request\x18\x07 \x01(\x08\x12\x0c\n\x04push\x18\x08 \x01(\x08')
)




_NODE = _descriptor.Descriptor(
  name='Node',
  full_name='Node',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Node.id', index=0,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rank', full_name='Node.rank', index=1,
      number=6, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='client_id', full_name='Node.client_id', index=2,
      number=5, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='Node.port', index=3,
      number=8001, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ip', full_name='Node.ip', index=4,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='role', full_name='Node.role', index=5,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_recover', full_name='Node.is_recover', index=6,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=129,
)


_NODELIST = _descriptor.Descriptor(
  name='NodeList',
  full_name='NodeList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='nodel', full_name='NodeList.nodel', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=131,
  serialized_end=163,
)


_CONTROL = _descriptor.Descriptor(
  name='Control',
  full_name='Control',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='command', full_name='Control.command', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reg_node', full_name='Control.reg_node', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=165,
  serialized_end=216,
)


_META = _descriptor.Descriptor(
  name='Meta',
  full_name='Meta',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='head', full_name='Meta.head', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='body', full_name='Meta.body', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='control', full_name='Meta.control', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='Meta.timestamp', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sender_id', full_name='Meta.sender_id', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='recv_id', full_name='Meta.recv_id', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='request', full_name='Meta.request', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='push', full_name='Meta.push', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=219,
  serialized_end=366,
)

_NODELIST.fields_by_name['nodel'].message_type = _NODE
_CONTROL.fields_by_name['reg_node'].message_type = _NODE
_META.fields_by_name['control'].message_type = _CONTROL
DESCRIPTOR.message_types_by_name['Node'] = _NODE
DESCRIPTOR.message_types_by_name['NodeList'] = _NODELIST
DESCRIPTOR.message_types_by_name['Control'] = _CONTROL
DESCRIPTOR.message_types_by_name['Meta'] = _META
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Node = _reflection.GeneratedProtocolMessageType('Node', (_message.Message,), dict(
  DESCRIPTOR = _NODE,
  __module__ = 'message_pb2'
  # @@protoc_insertion_point(class_scope:Node)
  ))
_sym_db.RegisterMessage(Node)

NodeList = _reflection.GeneratedProtocolMessageType('NodeList', (_message.Message,), dict(
  DESCRIPTOR = _NODELIST,
  __module__ = 'message_pb2'
  # @@protoc_insertion_point(class_scope:NodeList)
  ))
_sym_db.RegisterMessage(NodeList)

Control = _reflection.GeneratedProtocolMessageType('Control', (_message.Message,), dict(
  DESCRIPTOR = _CONTROL,
  __module__ = 'message_pb2'
  # @@protoc_insertion_point(class_scope:Control)
  ))
_sym_db.RegisterMessage(Control)

Meta = _reflection.GeneratedProtocolMessageType('Meta', (_message.Message,), dict(
  DESCRIPTOR = _META,
  __module__ = 'message_pb2'
  # @@protoc_insertion_point(class_scope:Meta)
  ))
_sym_db.RegisterMessage(Meta)


# @@protoc_insertion_point(module_scope)
