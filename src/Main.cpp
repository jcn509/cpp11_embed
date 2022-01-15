#include <cstdlib>
#include <fstream>
#include <iostream>
#include <memory>

#include "Lib.h"

int main(const int argc, char *argv[]) {
  if (argc != 4) {
    std::cerr << "Usage:\n ";
    return EXIT_FAILURE;
  }
  const char *input_filename = argv[1];
  const char *identifier_name = argv[2];
  const char *output_filename = argv[3];
  // Use std::optional? Would require C++17?
  // Read in binary mode so that we embed the file contents
  // exactly as they are
  const std::unique_ptr<std::ifstream> in_file_stream =
      (std::string{input_filename} == "-")
          ? nullptr
          : std::make_unique<std::ifstream>(input_filename,
                                            std::ifstream::binary);
  const std::unique_ptr<std::ofstream> out_file_stream =
      (std::string{output_filename} == "-")
          ? nullptr
          : std::make_unique<std::ofstream>(output_filename);
  // const bool binary_mode = false;
  std::istream &input_stream =
      (in_file_stream == nullptr) ? std::cin : *in_file_stream;
  std::ostream &output_stream =
      (out_file_stream == nullptr) ? std::cout : *out_file_stream;
  if (input_stream) {
    cpp11embed::OutputEscapedStringLiteralHeader(identifier_name, input_stream,
                                                 output_stream);
  } else {
    // couldn't open the file
  }

  return EXIT_SUCCESS;
}