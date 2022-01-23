// Standard library
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <memory>

// 3rd party
#include <args.hxx>

// Project
#include "Lib.h"

namespace {
bool OutputHeader(args::Positional<std::string> &input_file,
                  args::Positional<std::string> &identifier_name,
                  args::ValueFlag<std::string> &output_filename,
                  args::Flag &binary_mode, args::Flag &use_header_guard) {
  const std::string &input_filename = args::get(input_file);
  // Use std::optional? Would require C++17?
  // Read in binary mode so that we embed the file contents
  // exactly as they are
  const std::unique_ptr<std::ifstream> in_file_stream =
      (input_filename == "-") ? nullptr
                              : std::make_unique<std::ifstream>(
                                    input_filename, std::ifstream::binary);
  if (in_file_stream != nullptr && !in_file_stream) {
    std::cerr << "Unable to read input\n";
    return false;
  }

  const std::unique_ptr<std::ofstream> out_file_stream =
      (output_filename)
          ? std::make_unique<std::ofstream>(args::get(output_filename))
          : nullptr;
  if (out_file_stream != nullptr && !out_file_stream) {
    std::cerr << "Unable to open output file\n";
    return false;
  }

  std::istream &input_stream =
      (in_file_stream == nullptr) ? std::cin : *in_file_stream;
  std::ostream &output_stream =
      (out_file_stream == nullptr) ? std::cout : *out_file_stream;

  if (binary_mode) {
    cpp11embed::OutputBinaryDataHeader(args::get(identifier_name),
                                       args::get(use_header_guard),
                                       input_stream, output_stream);
  } else {
    cpp11embed::OutputEscapedStringLiteralHeader(args::get(identifier_name),
                                                 args::get(use_header_guard),
                                                 input_stream, output_stream);
  }
  return true;
}
}  // namespace

int main(const int argc, char *argv[]) {
  args::ArgumentParser parser("CPP11 Embed", "Embed files in C++11 programs");
  args::HelpFlag help(parser, "help", "Display this help menu", {'h', "help"});

  // Required arguments
  args::Positional<std::string> input_file(
      parser, "input_file",
      "Input file (use - to read from stdin). Note: input is read exactly and "
      "line-endings are left unchanged",
      args::Options::Required);
  args::Positional<std::string> identifier_name(
      parser, "identifier_name",
      "The name of constant/variable you want to store the data in",
      args::Options::Required);

  // Optional flags
  args::ValueFlag<std::string> output_filename(
      parser, "output",
      "Redirect the output to a file instead of standard output",
      {'o', "output"});
  args::Flag binary_mode(parser, "binary_mode",
                         "The input is binary data and not text",
                         {'b', "binary-mode"});
  args::Flag use_header_guard(parser, "use_header_guard",
                              "Use a header guard rather than #pragma once",
                              {'g', "use-header-guard"});

  try {
    parser.ParseCLI(argc, argv);
  } catch (args::Help &) {
    std::cout << parser;
    return EXIT_SUCCESS;
  } catch (args::ParseError &e) {
    std::cerr << e.what() << std::endl;
    std::cerr << parser;
    return EXIT_FAILURE;
  } catch (args::ValidationError &e) {
    std::cerr << e.what() << std::endl;
    std::cerr << parser;
    return EXIT_FAILURE;
  }

  return OutputHeader(input_file, identifier_name, output_filename, binary_mode,
                      use_header_guard)
             ? EXIT_SUCCESS
             : EXIT_FAILURE;
}