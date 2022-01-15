#include <istream>
#include <ostream>

namespace cpp11embed {
void OutputEscapedCharacter(char c, std::ostream &out);

void OutputEscapedStringLiteral(std::istream &input_stream,
                                std::ostream &output_stream);

void OutputEscapedStringLiteralHeader(const std::string &identifier_name,
                                      std::istream &input_stream,
                                      std::ostream &output_stream);
}  // namespace cpp11embed