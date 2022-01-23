#include <catch2/catch.hpp>
#include <limits>
#include <sstream>

#include "Lib.h"

namespace {
std::string GetEscapedCharacterChar(const char c) {
  std::ostringstream strm;
  cpp11embed::OutputEscapedCharacter(c, strm);
  return strm.str();
}

std::string GetEscapedStringLiteral(const std::string& to_escape) {
  std::istringstream input_stream{to_escape};
  std::ostringstream output_stream;
  cpp11embed::OutputEscapedStringLiteral(input_stream, output_stream);
  return output_stream.str();
}

std::string GetEscapedStringLiteralHeader(const std::string& identifier,
                                          const bool use_header_guard,
                                          const std::string& literal_value) {
  std::istringstream input_stream{literal_value};
  std::ostringstream output_stream;
  cpp11embed::OutputEscapedStringLiteralHeader(identifier, use_header_guard,
                                               input_stream, output_stream);
  return output_stream.str();
}

bool CharShouldBeEscaped(const char c) {
  return (c == '\'') || (c == '\"') || (c == '\?') || (c == '\\') ||
         (c == '\a') || (c == '\b') || (c == '\f') || (c == '\n') ||
         (c == '\r') || (c == '\t') || (c == '\v');
}

std::string GetBinaryHeader(const std::string& identifier,
                            const bool use_header_guard, const char* const data,
                            const size_t data_size) {
  std::istringstream input_stream{std::string{data, data_size}};
  std::ostringstream output_stream;
  cpp11embed::OutputBinaryDataHeader(identifier, use_header_guard, input_stream,
                                     output_stream);
  return output_stream.str();
}
}  // namespace

TEST_CASE(
    "cpp11embed::OutputEscapedCharacter characters that shouldn't be escaped",
    "[cpp11embed][OutputEscapedCharacter]") {
  const char c = GENERATE(std::numeric_limits<char>::min(),
                          std::numeric_limits<char>::max() + 1);
  CAPTURE(c);
  if (!CharShouldBeEscaped(c)) {
    const std::string escaped_char = GetEscapedCharacterChar(c);
    REQUIRE(escaped_char.size() == 1);
    REQUIRE(escaped_char[0] == c);
  }
}

TEST_CASE(
    "cpp11embed::OutputEscapedCharacter character that should be escaped - '",
    "[cpp11embed][OutputEscapedCharacter]") {
  REQUIRE(GetEscapedCharacterChar('\'') == "\\'");
}

TEST_CASE(
    "cpp11embed::OutputEscapedCharacter character that should be escaped - \"",
    "[cpp11embed][OutputEscapedCharacter]") {
  REQUIRE(GetEscapedCharacterChar('\"') == "\\\"");
}

TEST_CASE(
    "cpp11embed::OutputEscapedCharacter character that should be escaped - \\?",
    "[cpp11embed][OutputEscapedCharacter]") {
  REQUIRE(GetEscapedCharacterChar('\?') == "\\?");
}

TEST_CASE(
    "cpp11embed::OutputEscapedCharacter character that should be escaped - \\",
    "[cpp11embed][OutputEscapedCharacter]") {
  REQUIRE(GetEscapedCharacterChar('\\') == "\\\\");
}

TEST_CASE(
    "cpp11embed::OutputEscapedCharacter character that should be escaped - \\a",
    "[cpp11embed][OutputEscapedCharacter]") {
  REQUIRE(GetEscapedCharacterChar('\a') == "\\a");
}

TEST_CASE(
    "cpp11embed::OutputEscapedCharacter character that should be escaped - \\b",
    "[cpp11embed][OutputEscapedCharacter]") {
  REQUIRE(GetEscapedCharacterChar('\b') == "\\b");
}

TEST_CASE(
    "cpp11embed::OutputEscapedCharacter character that should be escaped - \\f",
    "[cpp11embed][OutputEscapedCharacter]") {
  REQUIRE(GetEscapedCharacterChar('\f') == "\\f");
}

TEST_CASE(
    "cpp11embed::OutputEscapedCharacter character that should be escaped - \\n",
    "[cpp11embed][OutputEscapedCharacter]") {
  REQUIRE(GetEscapedCharacterChar('\n') == "\\n");
}

TEST_CASE(
    "cpp11embed::OutputEscapedCharacter character that should be escaped - \\r",
    "[cpp11embed][OutputEscapedCharacter]") {
  REQUIRE(GetEscapedCharacterChar('\r') == "\\r");
}

TEST_CASE(
    "cpp11embed::OutputEscapedCharacter character that should be escaped - \\t",
    "[cpp11embed][OutputEscapedCharacter]") {
  REQUIRE(GetEscapedCharacterChar('\t') == "\\t");
}

TEST_CASE(
    "cpp11embed::OutputEscapedCharacter character that should be escaped - \\v",
    "[cpp11embed][OutputEscapedCharacter]") {
  REQUIRE(GetEscapedCharacterChar('\v') == "\\v");
}

TEST_CASE("cpp11embed::OutputEscapedStringLiteral no characters need escaping",
          "[cpp11embed][OutputEscapedStringLiteral]") {
  const std::string to_escape =
      GENERATE("", "abcdefghijklmnopqrstuvwxyz", " ", "ASDNCA caascfd ~ACDCDA",
               ".!// / ;:@#)()*&^%", "");
  CAPTURE(to_escape);
  REQUIRE(GetEscapedStringLiteral(to_escape) == "\"" + to_escape + "\"");
}

TEST_CASE("cpp11embed::OutputEscapedStringLiteral all characters need escaping",
          "[cpp11embed][OutputEscapedStringLiteral]") {
  const std::string to_escape = "\n\r\t";
  REQUIRE(GetEscapedStringLiteral(to_escape) == R"("\n\r\t")");
}

TEST_CASE(
    "cpp11embed::OutputEscapedStringLiteral some characters need escaping",
    "[cpp11embed][OutputEscapedStringLiteral]") {
  const std::string to_escape = "\na\rbb\tccc";
  REQUIRE(GetEscapedStringLiteral(to_escape) == R"("\na\rbb\tccc")");
}

TEST_CASE("cpp11embed::OutputStringLiteralHeader",
          "[cpp11embed][OutputStringLiteralHeader]") {
  const std::string identifier = "an_identifier";
  const std::string literal_value = "abcdefg\n";
  REQUIRE(GetEscapedStringLiteralHeader(identifier, false, literal_value) ==
          "#pragma once\n\nconstexpr char an_identifier[] = \"abcdefg\\n\";\n");
  REQUIRE(GetEscapedStringLiteralHeader(identifier, true, literal_value) ==
          "#ifndef AN_IDENTIFIER\n#define AN_IDENTIFIER\n\nconstexpr char "
          "an_identifier[] = \"abcdefg\\n\";\n\n#endif\n");
}

TEST_CASE("cpp11embed::GetBinaryInitialiser {1, 2, 3, 4}",
          "[cpp11embed][GetBinaryInitialiser]") {
  constexpr char input[]{1, 2, 3, 4};
  std::istringstream input_stream{std::string{input, sizeof(input)}};
  const cpp11embed::InitialiserAndNumberOfElements initialiser =
      cpp11embed::GetBinaryInitialiser(input_stream);
  REQUIRE(initialiser.initialiser == "{1, 2, 3, 4}");
  REQUIRE(initialiser.number_of_elements == 4);
}

TEST_CASE("cpp11embed::GetBinaryInitialiser {9, 12, '\n' 3}",
          "[cpp11embed][GetBinaryInitialiser]") {
  // New line should not be escaped
  constexpr char input[]{9, 12, '\n', 3};
  std::istringstream input_stream{std::string{input, sizeof(input)}};
  const cpp11embed::InitialiserAndNumberOfElements initialiser =
      cpp11embed::GetBinaryInitialiser(input_stream);
  std::string expected_output =
      "{9, 12, " + std::to_string(static_cast<int>('\n')) + ", 3}";
  REQUIRE(initialiser.initialiser == "{9, 12, 3}");
  REQUIRE(initialiser.number_of_elements == 3);
}

TEST_CASE("cpp11embed::OutputBinaryDataHeader {1, 2, 3, 4}",
          "[cpp11embed][OutputBinaryDataHeader]") {
  constexpr char input[]{1, 2, 3, 4};
  REQUIRE(GetBinaryHeader("identifier", false, input, sizeof(input)) ==
          "#pragma once\n\n#include <array>\n#include <cstdint>\n\n"
          "constexpr std::array<uint8_t, 4> identifier{1, 2, 3, 4};\n");
  REQUIRE(
      GetBinaryHeader("identifier", true, input, sizeof(input)) ==
      "#ifndef IDENTIFIER\n#define IDENTIFIER\n\n#include "
      "<array>\n#include <cstdint>\n\n"
      "constexpr std::array<uint8_t, 4> identifier{1, 2, 3, 4};\n\n#endif\n");
}

TEST_CASE("cpp11embed::OutputBinaryDataHeader {9, 12, 3}",
          "[cpp11embed][OutputBinaryDataHeader]") {
  constexpr char input[]{9, 12, 3};
  REQUIRE(GetBinaryHeader("another_identifier", false, input, sizeof(input)) ==
          "#pragma once\n\n#include <array>\n#include <cstdint>\n\n"
          "constexpr std::array<uint8_t, 3> another_identifier{9, 12, 3};\n");
  REQUIRE(GetBinaryHeader("another_identifier", true, input, sizeof(input)) ==
          "#ifndef ANOTHER_IDENTIFIER\n#define ANOTHER_IDENTIFIER\n\n#include "
          "<array>\n#include <cstdint>\n\n"
          "constexpr std::array<uint8_t, 3> another_identifier{9, 12, "
          "3};\n\n#endif\n");
}
