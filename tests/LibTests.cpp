#include <limits>
#include <sstream>

#include <catch2/catch.hpp>

#include "Lib.h"

namespace
{
    [[nodiscard]] std::string GetEscapedCharacterChar(const char c)
    {
        std::stringstream strm;
        cpp11embed::OutputEscapedCharacter(c, strm);
        return strm.str();
    }

    [[nodiscard]] bool CharShouldBeEscaped(const char c)
    {
        return (c == '\'') ||
               (c == '\"') ||
               (c == '\?') ||
               (c == '\\') ||
               (c == '\a') ||
               (c == '\b') ||
               (c == '\f') ||
               (c == '\n') ||
               (c == '\r') ||
               (c == '\t') ||
               (c == '\v');
    }
}

TEST_CASE("cpp11embed::OutputEscapedCharacter characters that shouldn't be escaped", "[cpp11embed][OutputEscapedCharacter]")
{
    const char c = GENERATE(std::numeric_limits<char>::min(), std::numeric_limits<char>::max() + 1);
    CAPTURE(c);
    if (!CharShouldBeEscaped(c))
    {
        const std::string escaped_char = GetEscapedCharacterChar(c);
        REQUIRE(escaped_char.size() == 1);
        REQUIRE(escaped_char[0] == c);
    }
}

TEST_CASE("cpp11embed::OutputEscapedCharacter character that should be escaped - '", "[cpp11embed][OutputEscapedCharacter]")
{
    REQUIRE(GetEscapedCharacterChar('\'') == "\\'");
}

TEST_CASE("cpp11embed::OutputEscapedCharacter character that should be escaped - \"", "[cpp11embed][OutputEscapedCharacter]")
{
    REQUIRE(GetEscapedCharacterChar('\"') == "\\\"");
}

TEST_CASE("cpp11embed::OutputEscapedCharacter character that should be escaped - \\?", "[cpp11embed][OutputEscapedCharacter]")
{
    REQUIRE(GetEscapedCharacterChar('\?') == "\\?");
}

TEST_CASE("cpp11embed::OutputEscapedCharacter character that should be escaped - \\", "[cpp11embed][OutputEscapedCharacter]")
{
    REQUIRE(GetEscapedCharacterChar('\\') == "\\\\");
}

TEST_CASE("cpp11embed::OutputEscapedCharacter character that should be escaped - \\a", "[cpp11embed][OutputEscapedCharacter]")
{
    REQUIRE(GetEscapedCharacterChar('\a') == "\\a");
}

TEST_CASE("cpp11embed::OutputEscapedCharacter character that should be escaped - \\b", "[cpp11embed][OutputEscapedCharacter]")
{
    REQUIRE(GetEscapedCharacterChar('\b') == "\\b");
}

TEST_CASE("cpp11embed::OutputEscapedCharacter character that should be escaped - \\f", "[cpp11embed][OutputEscapedCharacter]")
{
    REQUIRE(GetEscapedCharacterChar('\f') == "\\f");
}

TEST_CASE("cpp11embed::OutputEscapedCharacter character that should be escaped - \\n", "[cpp11embed][OutputEscapedCharacter]")
{
    REQUIRE(GetEscapedCharacterChar('\n') == "\\n");
}

TEST_CASE("cpp11embed::OutputEscapedCharacter character that should be escaped - \\r", "[cpp11embed][OutputEscapedCharacter]")
{
    REQUIRE(GetEscapedCharacterChar('\r') == "\\r");
}

TEST_CASE("cpp11embed::OutputEscapedCharacter character that should be escaped - \\t", "[cpp11embed][OutputEscapedCharacter]")
{
    REQUIRE(GetEscapedCharacterChar('\t') == "\\t");
}

TEST_CASE("cpp11embed::OutputEscapedCharacter character that should be escaped - \\v", "[cpp11embed][OutputEscapedCharacter]")
{
    REQUIRE(GetEscapedCharacterChar('\v') == "\\v");
}