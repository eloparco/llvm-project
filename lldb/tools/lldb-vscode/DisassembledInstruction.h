#ifndef LLDB_TOOLS_LLDB_VSCODE_DISASSEMBLED_INSTRUCTION_H
#define LLDB_TOOLS_LLDB_VSCODE_DISASSEMBLED_INSTRUCTION_H

#include "VSCodeForward.h"
#include <string>

namespace lldb_vscode {

struct DisassembledInstruction {
  std::string m_address;
  std::string m_instruction;

  DisassembledInstruction();
  DisassembledInstruction(lldb::SBInstruction &inst);
};

} // namespace lldb_vscode

#endif // LLDB_TOOLS_LLDB_VSCODE_DISASSEMBLED_INSTRUCTION_H