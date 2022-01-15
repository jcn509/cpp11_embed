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
  std::istringstream in_strm{to_escape};
  std::ostringstream out_strm;
  cpp11embed::OutputEscapedStringLiteral(in_strm, out_strm);
  return out_strm.str();
}

std::string GetEscapedStringLiteralHeader(const std::string& identifier,
                                          const std::string& literal_value) {
  std::istringstream input_stream{literal_value};
  std::ostringstream output_strm;
  cpp11embed::OutputEscapedStringLiteralHeader(identifier, input_stream,
                                               output_strm);
  return output_strm.str();
}

bool CharShouldBeEscaped(const char c) {
  return (c == '\'') || (c == '\"') || (c == '\?') || (c == '\\') ||
         (c == '\a') || (c == '\b') || (c == '\f') || (c == '\n') ||
         (c == '\r') || (c == '\t') || (c == '\v');
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
  REQUIRE(GetEscapedStringLiteralHeader(identifier, literal_value) ==
          "#pragma once\n\nconstexpr char* an_identifier = \"abcdefg\\n\";\n");
}
