from typing import List

from ui.functions import COMMANDS, PROCESSES
from ui.utils import InterpreterFunctionWrapper as IFW, CommandParsingResult as CPS, UserContext, \
    reconstruct_delimited_arguments, TooFewArgumentsError, ArgumentValidationError


def command_not_found_error_function(context: UserContext, command: str, suggestion: str) -> str:
    return f"command '{command}' invalid, did you mean '`{suggestion}`'? Type '`help`' for a list of commands."


def parse_command(command: str) -> CPS:
    """ parses the given command and returns a CommandParsingResult object."""
    split_command: List[str] = reconstruct_delimited_arguments(command.split())
    parser = COMMANDS
    indentation_levels: int = 0
    full_command: str = ""
    for command_token in split_command:
        ctlw = command_token.lower()  # ctlw = command token lower
        if ctlw in parser:
            if isinstance(parser[ctlw], IFW):
                ifw: IFW = parser[ctlw]
                args: List[str] = split_command[indentation_levels+1:]
                if ifw.number_of_args > len(args):
                    raise TooFewArgumentsError(full_command + command_token, ifw.number_of_args, len(args))
                return CPS(ifw, args)
            full_command = f"{full_command}{command_token} "
            parser = parser[ctlw]
            indentation_levels += 1
    return CPS(command_not_found_error_function, [command, f"{full_command}{list(parser.keys())[0]}"])


def context_aware_execute(user: UserContext, user_input: str) -> str:
    """ parses and elaborates the given user input and returns the output. """
    if user.is_in_a_process():
        return PROCESSES[user.get_process_name()][user.get_process_step()](user, user_input)
    try:
        parsing_result = parse_command(user_input)
        return parsing_result.execute(user)
    except ArgumentValidationError as e:
        return str(e)
