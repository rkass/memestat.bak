project( Starter )
find_package( OpenCV REQUIRED )
add_executable( Starter starter.cpp )
target_link_libraries( Starter ${OpenCV_LIBS} )

