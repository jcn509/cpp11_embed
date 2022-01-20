#include <istream>
#include <ostream>

namespace cpp11embed {
std::string GetSafeHeaderGuardIdentifier(const std::string &unsafe);

void OutputEscapedCharacter(char c, std::ostream &out);

void OutputEscapedStringLiteral(std::istream &input_stream,
                                std::ostream &output_stream);

void OutputEscapedStringLiteralHeader(const std::string &identifier_name,
                                      bool use_header_guard,
                                      std::istream &input_stream,
                                      std::ostream &output_stream);

struct InitialiserAndNumberOfElements {
  std::string initialiser;
  size_t number_of_elements;
};
/**
 * @returns the number of elements in the initialiser
 */
InitialiserAndNumberOfElements GetBinaryInitialiser(std::istream &input_stream);

void OutputBinaryDataHeader(const std::string &identifier_name,
                            bool use_header_guard, std::istream &input_stream,
                            std::ostream &output_stream);
}  // namespace cpp11embed