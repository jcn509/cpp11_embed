#include "Lib.h"

#include <algorithm>
#include <iterator>
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
}  // namespace cpp11embed