// C++
#include <cstring>

// 3rd party
#include <catch2/catch.hpp>

// Project
#include "BinaryHeader.h"
#include "BinaryHeaderWithHeaderGuard.h"
#include "InASubDirectory/TextHeader2.h"
#include "TextHeader.h"
#include "TextHeaderWithHeaderGuard.h"

// Include the headers twice to make sure that header guards and pragmas are
// done correctly. If they aren't compilation will fail due to multiple
// definitions of the same constants
#include "BinaryHeader.h"
#include "BinaryHeaderWithHeaderGuard.h"
#include "TextHeader.h"
#include "TextHeaderWithHeaderGuard.h"

TEST_CASE("cpp11embedtest auto-generated text header",
          "[cpp11embed][SelfTest]") {
  REQUIRE(std::strcmp(k_text_header, "one line\ntwo lines") == 0);
}

TEST_CASE("cpp11embedtest auto-generated text header with header guard",
          "[cpp11embed][SelfTest]") {
  REQUIRE(std::strcmp(k_text_header_with_header_guard, "one line\ntwo lines") ==
          0);
}

TEST_CASE("cpp11embedtest auto-generated binary header",
          "[cpp11embed][SelfTest]") {
  REQUIRE(k_binary_header ==
          std::array<uint8_t, 18>{111, 110, 101, 32, 108, 105, 110, 101, 10,
                                  116, 119, 111, 32, 108, 105, 110, 101, 115});
}

TEST_CASE("cpp11embedtest auto-generated binary header with header guard",
          "[cpp11embed][SelfTest]") {
  REQUIRE(k_binary_header_with_header_guard ==
          std::array<uint8_t, 18>{111, 110, 101, 32, 108, 105, 110, 101, 10,
                                  116, 119, 111, 32, 108, 105, 110, 101, 115});
}

TEST_CASE("cpp11embedtest auto-generated text header in a subdirectory",
          "[cpp11embed][SelfTest]") {
  REQUIRE(std::strcmp(k_text_header_in_a_subdirectory, "one line\ntwo lines") ==
          0);
}
