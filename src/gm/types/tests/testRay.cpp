//
// This file is auto-generated, please do not modify directly!
//

#include <catch2/catch.hpp>

#include <gm/types/ray.h>

TEST_CASE( "Ray_DefaultConstructor" )
{
    gm::Ray ray;
    CHECK( ray.Origin() == gm::Vec3f() );
    CHECK( ray.Direction() == gm::Vec3f() );
}