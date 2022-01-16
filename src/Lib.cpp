#include "Lib.h"

#include <algorithm>
#include <iterator>
#include <sstream>
#include <string>

namespace cpp11embed {
void OutputEscapedCharacter(const char c, std::ostream &out) {
  switch (c) {
    case '\'':
      out << "\\'";
      break;
    case '\"':
      out << "\\\"";
      break;
    // Escaping questions marks may be necessary before C++17?:
    // https://en.cppreference.com/w/cpp/language/escape#Notes
    // https://en.cppreference.com/w/cpp/language/operator_alternative
    case '\?':
      out << "\\?";
      break;
    case '\\':
      out << "\\\\";
      break;
    case '\a':
      out << "\\a";
      break;
    case '\b':
      out << "\\b";
      break;
    case '\f':
      out << "\\f";
      break;
    case '\n':
#include <algorithm>
#include <string>
      out << "\\n";
      break;
    case '\r':
      out << "\\r";
      break;
    case '\t':
      out << "\\t";
      break;
    case '\v':
      out << "\\v";
      break;
    default:
      out << c;
  }
}

void OutputEscapedStringLiteral(std::istream &input_stream,
                                std::ostream &output_stream) {
  output_stream << '"';
  std::for_each(std::istreambuf_iterator<char>(input_stream),
                std::istreambuf_iterator<char>(),
                [&output_stream](const char c) {
                  OutputEscapedCharacter(c, output_stream);
                });
  output_stream << '"';
}

void OutputEscapedStringLiteralHeader(const std::string &identifier_name,
                                      std::istream &input_stream,
                                      std::ostream &output_stream) {
  // TODO: Allow using header guard instead of pragma once
  output_stream << "#pragma once\n\n"
                << "constexpr char* " << identifier_name << " = ";
  OutputEscapedStringLiteral(input_stream, output_stream);
  output_stream << ";\n";
}

InitialiserAndNumberOfElements GetBinaryInitialiser(
    std::istream &input_stream) {
  std::ostringstream output_stream;
  output_stream << "{";
  size_t num_elements = 0;
  if (input_stream) {
    while (1) {
      uint8_t c;
      input_stream.read(reinterpret_cast<char *>(&c), sizeof(uint8_t));
      output_stream << std::to_string(c);
      num_elements++;
      // Check to see if there is another byte
      input_stream.peek();
      if (input_stream.eof()) {
        break;
      } else {
        // Not yet at the last element
        output_stream << ", ";
      }
    }
  }
  output_stream << "}";
  return {output_stream.str(), num_elements};
}

void OutputBinaryDataHeader(const std::string &identifier_name,
                            std::istream &input_stream,
                            std::ostream &output_stream) {
  // TODO: Allow using header guard instead of pragma once

  const InitialiserAndNumberOfElements binary_initialiser_details =
      GetBinaryInitialiser(input_stream);
  output_stream << "#pragma once\n\n"
                << "#include <array>\n"
                << "#include <cstdint>\n\n"
                << "constexpr std::array<uint8_t, "
                << binary_initialiser_details.number_of_elements << "> "
                << identifier_name << binary_initialiser_details.initialiser
                << ";\n";
}
}  // namespace cpp11embed