cmake_minimum_required(VERSION 3.8)
project(self_test_robot_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

# Install directory named urdf to the pkg share destination
install(
  DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
