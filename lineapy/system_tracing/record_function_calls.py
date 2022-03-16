from __future__ import annotations

import operator
from contextlib import contextmanager
from dataclasses import InitVar, dataclass, field
from dis import Instruction, get_instructions
from sys import settrace
from types import CodeType
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Union

from lineapy.system_tracing._op_stack import OpStack
from lineapy.system_tracing.function_call import FunctionCall

# from rich.console import Console
# from rich.table import Table


@contextmanager
def record_function_calls(code: CodeType) -> Iterator[List[FunctionCall]]:
    """
    Use tracing to record all function calls that have frames defined in one of the code objects contained in the code object passed in.
    """

    try:
        trace_fn = TraceFunc(code)
        settrace(trace_fn)
        yield trace_fn.function_calls
    finally:
        settrace(None)
        # trace_fn.visualize()


# This callback is saved when we have an operator that had some function call. We need to defer some of the processing until the next bytecode instruction loads,
# So that at the point, the return value will be in the stack and we can look at it.
ReturnValueCallback = Optional[Callable[[OpStack], FunctionCall]]


@dataclass
class TraceFunc:

    code: InitVar[CodeType]
    function_calls: List[FunctionCall] = field(default_factory=list)

    # Mapping of each code object that was passed in to its instructions, by offset, so we can quicjly look up what instruction we are looking at
    code_to_offset_to_instruction: Dict[
        CodeType, Dict[int, Instruction]
    ] = field(init=False)

    # If set, then the previous bytecode instruction had a function call, and during the next call, we should call
    # this function with the current stack to get the FunctionCall result.
    return_value_callback: ReturnValueCallback = field(default=None)

    # Table of bytecode evaluations, for visualization.
    # table: Table = field(
    #     default_factory=lambda: Table(title="Bytecode Evaluations")
    # )

    def __post_init__(self, code):
        self.code_to_offset_to_instruction = {
            code: {i.offset: i for i in get_instructions(code)}
            for code in all_code_objects(code)
        }

        # self.table.add_column("Name", justify="right", no_wrap=True)
        # self.table.add_column(
        #     "Arg",
        #     justify="right",
        # )
        # self.table.add_column(
        #     "Stack",
        # )

    # def visualize(self):
    #     console = Console()
    #     console.print(self.table)

    def __call__(self, frame, event, arg):
        # Exit early if the code object for this frame is not one of the code objects we want to trace
        if frame.f_code not in self.code_to_offset_to_instruction:
            return self

        # If it is one we want to trace, enable opcode tracing on it
        frame.f_trace_opcodes = True
        # If this is not an opcode event, ignore it
        if event != "opcode":
            return self

        # Lookup the instruction we currently have based on the code object as well as the offset in that object
        instruction = self.code_to_offset_to_instruction[frame.f_code][
            frame.f_lasti
        ]

        # Create an op stack around the frame so we can access the stack
        op_stack = OpStack(frame)

        # If during last instruction we had some function call that needs a return value, trigger the callback with the current
        # stack, so it can get the return value.
        if self.return_value_callback:
            self.function_calls.append(self.return_value_callback(op_stack))
            self.return_value_callback = None

        # Check if the current operation is a function call
        possible_function_call = resolve_bytecode_execution(
            instruction.opname, instruction.argval, op_stack
        )
        # If resolving the function call needs to be deferred until after we have the return value, save teh callback
        if callable(possible_function_call):
            self.return_value_callback = possible_function_call
        # Otherwise, if we could resolve it fully now, add that to our function call
        elif possible_function_call:
            self.function_calls.append(possible_function_call)

        # self.table.add_row(
        #     instruction.opname,
        #     instruction.argrepr,
        # )
        return self


UNARY_OPERATORS = {"UNARY_POSITIVE": operator.pos}


def resolve_bytecode_execution(
    name: str, value: object, stack: OpStack
) -> Union[ReturnValueCallback, FunctionCall]:
    """
    Returns a function call corresponding to the bytecode executing on the current stack.
    """
    if name in UNARY_OPERATORS:
        return unary_operator(UNARY_OPERATORS[name], stack)
    return None


def unary_operator(fn: Callable, stack: OpStack) -> ReturnValueCallback:
    args = [stack[-1]]
    return lambda post_stack: FunctionCall(fn, args, {}, post_stack[-1])


def all_code_objects(code: CodeType) -> Iterable[CodeType]:
    """
    Return all code objects from a source code object. This will include those used within it, such as nested functions.
    """
    yield code
    for const in code.co_consts:
        if isinstance(const, CodeType):
            yield from all_code_objects(const)
