import datetime
from lineapy.data.types import *
from lineapy.utils import get_new_id

session = SessionContext(
    id=get_new_id(),
    environment_type=SessionType.SCRIPT,
    creation_time=datetime.datetime(1, 1, 1, 0, 0),
    file_name="[source file path]",
    code='bs = [1,2]\nif len(bs) > 4:\n    print("True")\nelse:\n    bs.append(3)\n    print("False")\n',
    working_directory="dummy_linea_repo/",
    libraries=[],
)
literal_1 = LiteralNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=1,
    col_offset=6,
    end_lineno=1,
    end_col_offset=7,
    value=1,
)
literal_2 = LiteralNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=1,
    col_offset=8,
    end_lineno=1,
    end_col_offset=9,
    value=2,
)
lookup_1 = LookupNode(
    id=get_new_id(),
    session_id=session.id,
    name="__build_list__",
)
lookup_2 = LookupNode(
    id=get_new_id(),
    session_id=session.id,
    name="len",
)
literal_3 = LiteralNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=2,
    col_offset=13,
    end_lineno=2,
    end_col_offset=14,
    value=4,
)
lookup_3 = LookupNode(
    id=get_new_id(),
    session_id=session.id,
    name="gt",
)
literal_4 = LiteralNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=3,
    col_offset=10,
    end_lineno=3,
    end_col_offset=16,
    value="True",
)
lookup_4 = LookupNode(
    id=get_new_id(),
    session_id=session.id,
    name="print",
)
literal_5 = LiteralNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=5,
    col_offset=14,
    end_lineno=5,
    end_col_offset=15,
    value=3,
)
lookup_5 = LookupNode(
    id=get_new_id(),
    session_id=session.id,
    name="getattr",
)
literal_6 = LiteralNode(
    id=get_new_id(),
    session_id=session.id,
    value="append",
)
literal_7 = LiteralNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=6,
    col_offset=10,
    end_lineno=6,
    end_col_offset=17,
    value="False",
)
lookup_6 = LookupNode(
    id=get_new_id(),
    session_id=session.id,
    name="print",
)
argument_1 = ArgumentNode(
    id=get_new_id(),
    session_id=session.id,
    positional_order=0,
    value_node_id=literal_1.id,
)
argument_2 = ArgumentNode(
    id=get_new_id(),
    session_id=session.id,
    positional_order=1,
    value_node_id=literal_2.id,
)
argument_3 = ArgumentNode(
    id=get_new_id(),
    session_id=session.id,
    positional_order=1,
    value_node_id=literal_3.id,
)
argument_4 = ArgumentNode(
    id=get_new_id(),
    session_id=session.id,
    positional_order=0,
    value_node_id=literal_4.id,
)
argument_5 = ArgumentNode(
    id=get_new_id(),
    session_id=session.id,
    positional_order=0,
    value_node_id=literal_5.id,
)
argument_6 = ArgumentNode(
    id=get_new_id(),
    session_id=session.id,
    positional_order=1,
    value_node_id=literal_6.id,
)
argument_7 = ArgumentNode(
    id=get_new_id(),
    session_id=session.id,
    positional_order=0,
    value_node_id=literal_7.id,
)
call_1 = CallNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=1,
    col_offset=0,
    end_lineno=1,
    end_col_offset=10,
    arguments=[argument_1.id, argument_2.id],
    function_id=lookup_1.id,
)
call_2 = CallNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=3,
    col_offset=4,
    end_lineno=3,
    end_col_offset=17,
    arguments=[argument_4.id],
    function_id=lookup_4.id,
)
call_3 = CallNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=6,
    col_offset=4,
    end_lineno=6,
    end_col_offset=18,
    arguments=[argument_7.id],
    function_id=lookup_6.id,
)
variable_1 = VariableNode(
    id=get_new_id(),
    session_id=session.id,
    source_node_id=call_1.id,
    assigned_variable_name="bs",
)
argument_8 = ArgumentNode(
    id=get_new_id(),
    session_id=session.id,
    positional_order=0,
    value_node_id=variable_1.id,
)
argument_9 = ArgumentNode(
    id=get_new_id(),
    session_id=session.id,
    positional_order=0,
    value_node_id=variable_1.id,
)
call_4 = CallNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=2,
    col_offset=3,
    end_lineno=2,
    end_col_offset=10,
    arguments=[argument_8.id],
    function_id=lookup_2.id,
)
call_5 = CallNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=5,
    col_offset=4,
    end_lineno=5,
    end_col_offset=13,
    arguments=[argument_6.id, argument_9.id],
    function_id=lookup_5.id,
)
argument_10 = ArgumentNode(
    id=get_new_id(),
    session_id=session.id,
    positional_order=0,
    value_node_id=call_4.id,
)
call_6 = CallNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=5,
    col_offset=4,
    end_lineno=5,
    end_col_offset=16,
    arguments=[argument_5.id],
    function_id=call_5.id,
)
call_7 = CallNode(
    id=get_new_id(),
    session_id=session.id,
    lineno=2,
    col_offset=3,
    end_lineno=2,
    end_col_offset=14,
    arguments=[argument_10.id, argument_3.id],
    function_id=lookup_3.id,
)
