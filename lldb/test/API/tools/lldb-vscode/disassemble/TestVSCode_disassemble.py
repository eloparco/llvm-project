"""
Test lldb-vscode disassemble request
"""


from lldbsuite.test.decorators import *
from lldbsuite.test.lldbtest import *
import lldbvscode_testcase


class TestVSCode_disassemble(lldbvscode_testcase.VSCodeTestCaseBase):
    def setUp(self):
        lldbvscode_testcase.VSCodeTestCaseBase.setUp(self)

        program = self.getBuildArtifact("a.out")
        self.build_and_launch(program)
        source = "main.cpp"

        breakpoint_line = line_number(source, "// breakpoint")
        breakpoint_ids = self.set_source_breakpoints(source, [breakpoint_line])
        self.continue_to_breakpoints(breakpoint_ids)

    @skipIfWindows
    @skipIfRemote
    def test_disassemble_negative_offset(self):
        # Retrieve program counter
        stackFrames, _ = self.get_stackFrames_and_totalFramesCount()
        pc = stackFrames[0]["instructionPointerReference"]

        # Get disassembled instructions
        num_instructions, offset = 8, -4
        response = self.vscode.request_disassemble(
            memoryReference=pc,
            instructionOffset=offset,
            instructionCount=num_instructions,
        )
        self.assertTrue(response["success"])

        disas_instructions = response["body"]["instructions"]
        self.assertEquals(len(disas_instructions), num_instructions)
        self.assertEquals(disas_instructions[num_instructions + offset]["address"], pc)
        for instr in disas_instructions:
            self.assertTrue("invalid" not in instr["instruction"])

    @skipIfWindows
    @skipIfRemote
    def test_disassemble_zero_offset(self):
        # Retrieve program counter
        stackFrames, _ = self.get_stackFrames_and_totalFramesCount()
        pc = stackFrames[0]["instructionPointerReference"]

        # Get disassembled instructions
        num_instructions, offset = 4, 0
        response = self.vscode.request_disassemble(
            memoryReference=pc,
            instructionOffset=offset,
            instructionCount=num_instructions,
        )
        self.assertTrue(response["success"])

        disas_instructions = response["body"]["instructions"]
        self.assertEquals(len(disas_instructions), num_instructions)
        self.assertEquals(disas_instructions[offset]["address"], pc)
        for instr in disas_instructions:
            self.assertTrue("invalid" not in instr["instruction"])

    @skipIfWindows
    @skipIfRemote
    def test_disassemble_positive_offset(self):
        # Retrieve program counter
        stackFrames, _ = self.get_stackFrames_and_totalFramesCount()
        pc = stackFrames[0]["instructionPointerReference"]

        # Get disassembled instructions
        num_instructions, offset = 4, 2
        response = self.vscode.request_disassemble(
            memoryReference=pc,
            instructionOffset=offset,
            instructionCount=num_instructions,
        )
        self.assertTrue(response["success"])

        disas_instructions = response["body"]["instructions"]
        self.assertEquals(len(disas_instructions), num_instructions)
        for instr in disas_instructions:
            self.assertTrue("invalid" not in instr["instruction"])

    @skipIfWindows
    @skipIfRemote
    def test_disassemble_invalid_address(self):
        response = self.vscode.request_disassemble(
            memoryReference="0x0",
            instructionOffset=-200,
            instructionCount=400,
        )
        self.assertFalse(response["success"])
