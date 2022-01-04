#include "Lib.h"

#include <algorithm>
#include <iterator>

//remove
#include <iostream>

namespace cpp11embed
{
    void OutputEscapedCharacter(const char c, std::ostream &out)
    {
        switch (c)
        {
        case '\'':
            out << "\\'";
            break;
        case '\"':
            out << "\\\"";
            break;
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

    void OutputEscapedStringLiteral(std::istream &input_stream, std::ostream &output_stream)
    {
        output_stream << '"';
        std::for_each(std::istreambuf_iterator<char>(input_stream),
                      std::istreambuf_iterator<char>(),
                      [&output_stream](const char c)
                      {
                          OutputEscapedCharacter(c, output_stream);
                      });
        output_stream << '"';
    }
}