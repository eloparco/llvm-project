#include "DisassembledInstruction.h"

#include "LLDBUtils.h"
#include "VSCode.h"
#include "lldb/API/SBInstruction.h"

namespace lldb_vscode {

DisassembledInstruction::DisassembledInstruction()
    : m_address("0x0000000000000000"), m_instruction("   <invalid>") {}

DisassembledInstruction::DisassembledInstruction(lldb::SBInstruction &inst) {
  const auto inst_addr = inst.GetAddress().GetLoadAddress(g_vsc.target);
  const char *m = inst.GetMnemonic(g_vsc.target);
  const char *o = inst.GetOperands(g_vsc.target);
  const char *c = inst.GetComment(g_vsc.target);

  std::string line;
  llvm::raw_string_ostream line_strm(line);
  const auto comment_sep = (c == nullptr || std::string(c) == "") ? "" : "  ; ";
  line_strm << llvm::formatv("{0,12} {1}{2}{3}", m, o, comment_sep, c);

  m_address = addr_to_hex_string(inst_addr);
  m_instruction = line_strm.str();
}

} // namespace lldb_vscode