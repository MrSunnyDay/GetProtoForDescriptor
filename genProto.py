from google.protobuf import descriptor_pb2
import os

field_list = [
    "",
    "optional",
    "required",
    "repeated",
]

data_type_list = [
    "",
    "double",
    "float",
    "int64",
    "uint64",
    "int32",
    "fixed64",
    "fixed32",
    "bool",
    "string",
    "group",
    "message",
    "bytes",
    "uint32",
    "enum",
    "sfixed32",
    "sfixed64",
    "sint32",
    "sint64",
]
pbbin_file_path = "./test_dump_pb_buff.bin"
file = open(pbbin_file_path, "rb")
descriptor = descriptor_pb2.FileDescriptorProto()
data = file.read()
file.close()
descriptor.ParseFromString(data)
output_file = open("./"+(descriptor.name), "w")

message_type_list = descriptor.message_type
lines = []
if descriptor.syntax == "":
    lines.append("syntax = \"proto2\";")
else:
    lines.append("syntax = \"proto3\";")
if descriptor.package:
    package = descriptor.package
    lines.append("package %s;" % descriptor.package)
for dependency in descriptor.dependency:
    lines.append("import %s;" % dependency)
for enum_type in descriptor.enum_type:
    lines.append("enum %s {" % enum_type.name)
    for val in enum_type.value:
        path = (' '*2 + "{0} = {1};").format(val.name, val.number)
        lines.append(path)
        print(path)
    lines.append("}")
def gen_message_recursion(message_type_list, indent):
    for message in message_type_list:
        lines.append(' '*2*indent + "message %s {" % message.name)
        for enum in message.enum_type:
            lines.append(' '*2*(indent+1) + "enum %s {" % (enum.name))
            for enum_fied in enum.value:
                lines.append(' '*2*(indent+2) + "{0} = {1};".format(enum_fied.name, enum_fied.number))
            lines.append(' '*2*(indent+1) + "}")
        if message.nested_type:
            gen_message_recursion(message.nested_type, indent+1)
        for field in message.field:
            label_name = field_list[field.label]
            field_type = data_type_list[field.type]
            if field_type == "message" or field_type == "enum":
                field_type = field.type_name.replace(".{0}.".format(descriptor.package), "", 1)
                prefix = "{0}.".format(message.name)
                if prefix in field_type:
                    field_type = field_type[field_type.find(prefix) + len(prefix):]
                if field_type[0] == '.':
                    field_type = field_type[1:]
            lines.append(' '*2*(indent+1) + "{0} {1} {2} = {3};".format(label_name, field_type, field.name, field.number))
        lines.append(' '*2*indent + "}")
indent = 0;
for message in message_type_list:
    lines.append("message %s {" % message.name)
    for enum in message.enum_type:
        lines.append(' '*2 + "enum %s {" % (enum.name))
        for enum_fied in enum.value:
            lines.append(' '*4 + "{0} = {1};".format(enum_fied.name, enum_fied.number))
        lines.append(' '*2 + "}")
    if message.nested_type:
        gen_message_recursion(message.nested_type, indent+1)
    for field in message.field:
        label_name = field_list[field.label]
        field_type = data_type_list[field.type]
        if field_type == "message" or field_type == "enum":
            field_type = field.type_name.replace(".{0}.".format(descriptor.package), "", 1)
            prefix = "{0}.".format(message.name)
            if prefix in field_type:
                field_type = field_type[field_type.find(prefix)+len(prefix):]
            if field_type[0] == '.':
                field_type = field_type[1:]
        lines.append(' '*2 + "{0} {1} {2} = {3};".format(label_name, field_type, field.name, field.number))
    lines.append("}")
for line in lines:
    output_file.write(line+'\n')
output_file.close()

