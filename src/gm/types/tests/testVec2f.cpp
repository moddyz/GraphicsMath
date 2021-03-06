//
// This file is auto-generated, please do not modify directly!
//

#include <catch2/catch.hpp>

#include <gm/types/vec2f.h>

TEST_CASE( "Vec2f_DefaultConstructor" )
{
    gm::Vec2f vector;
    CHECK( vector == gm::Vec2f( 0.0f, 0.0f ) );
}

TEST_CASE( "Vec2f_CopyConstructor" )
{
    gm::Vec2f vectorA = gm::Vec2f( 0.0f, 2.0f );
    gm::Vec2f vectorB( vectorA );
    CHECK( vectorA == vectorB );
}

TEST_CASE( "Vec2f_CopyAssignmentConstructor" )
{
    gm::Vec2f vectorA = gm::Vec2f( 0.0f, 2.0f );
    gm::Vec2f vectorB = vectorA;
    CHECK( vectorA == vectorB );
}

TEST_CASE( "Vec2f_ElementReadAccess" )
{
    gm::Vec2f vector = gm::Vec2f( 0.0f, 2.0f );
    CHECK( vector[ 0 ] == 0.0f );
    CHECK( vector[ 1 ] == 2.0f );
}

TEST_CASE( "Vec2f_ElementWriteAccess" )
{
    gm::Vec2f vector;
    vector[ 0 ] = 0.0f;
    vector[ 1 ] = 5.0f;
    CHECK( vector[ 0 ] == 0.0f );
    CHECK( vector[ 1 ] == 5.0f );
}

TEST_CASE( "Vec2f_NamedElementReadAccessorX" )
{
    gm::Vec2f vector = gm::Vec2f( 0.0f, 1.0f );
    CHECK( vector.X() == 0.0f );
}

TEST_CASE( "Vec2f_NamedElementWriteAccessorX" )
{
    gm::Vec2f vector;
    vector.X() = 0.0f;
    CHECK( vector[ 0 ] == 0.0f );
}
TEST_CASE( "Vec2f_NamedElementReadAccessorY" )
{
    gm::Vec2f vector = gm::Vec2f( 0.0f, 1.0f );
    CHECK( vector.Y() == 1.0f );
}

TEST_CASE( "Vec2f_NamedElementWriteAccessorY" )
{
    gm::Vec2f vector;
    vector.Y() = 1.0f;
    CHECK( vector[ 1 ] == 1.0f );
}

TEST_CASE( "Vec2f_Addition" )
{
    gm::Vec2f vectorA = gm::Vec2f( 0.0f, 2.0f );
    gm::Vec2f vectorB = gm::Vec2f( 0.0f, 5.0f );
    gm::Vec2f vectorC = vectorA + vectorB;
    CHECK( vectorC == gm::Vec2f( 0.0f, 7.0f ) );
}

TEST_CASE( "Vec2f_AdditionAssignment" )
{
    gm::Vec2f vectorA = gm::Vec2f( 0.0f, 2.0f );
    gm::Vec2f vectorB = gm::Vec2f( 0.0f, 5.0f );
    vectorB += vectorA;
    CHECK( vectorB == gm::Vec2f( 0.0f, 7.0f ) );
}

TEST_CASE( "Vec2f_Subtraction" )
{
    gm::Vec2f vectorA = gm::Vec2f( 0.0f, 7.0f );
    gm::Vec2f vectorB = gm::Vec2f( 0.0f, 5.0f );
    gm::Vec2f vectorC = vectorA - vectorB;
    CHECK( vectorC == gm::Vec2f( 0.0f, 2.0f ) );
}

TEST_CASE( "Vec2f_SubtractionAssignment" )
{
    gm::Vec2f vectorA = gm::Vec2f( 0.0f, 5.0f );
    gm::Vec2f vectorB = gm::Vec2f( 0.0f, 7.0f );
    vectorB -= vectorA;
    CHECK( vectorB == gm::Vec2f( 0.0f, 2.0f ) );
}

TEST_CASE( "Vec2f_ScalarVectorMultiplication" )
{
    gm::Vec2f vectorA = gm::Vec2f( 0.0f, 2.0f );
    gm::Vec2f vectorB = 5.0f * vectorA;
    CHECK( vectorB == gm::Vec2f( 0.0f, 10.0f ) );
}

TEST_CASE( "Vec2f_VectorScalarMultiplication" )
{
    gm::Vec2f vectorA = gm::Vec2f( 0.0f, 2.0f );
    gm::Vec2f vectorB = vectorA * 5.0f;
    CHECK( vectorB == gm::Vec2f( 0.0f, 10.0f ) );
}

TEST_CASE( "Vec2f_ScalarMultiplicationAssignment" )
{
    gm::Vec2f vectorA = gm::Vec2f( 0.0f, 2.0f );
    vectorA *= 5;
    CHECK( vectorA == gm::Vec2f( 0.0f, 10.0f ) );
}

TEST_CASE( "Vec2f_VectorScalarDivision" )
{
    gm::Vec2f vectorA = gm::Vec2f( 0.0f, 10.0f );
    gm::Vec2f vectorB = vectorA / 5.0f;
    CHECK( vectorB == gm::Vec2f( 0.0f, 2.0f ) );
}

TEST_CASE( "Vec2f_ScalarDivisionAssignment" )
{
    gm::Vec2f vectorA = gm::Vec2f( 0.0f, 10.0f );
    vectorA /= 5;
    CHECK( vectorA == gm::Vec2f( 0.0f, 2.0f ) );
}

TEST_CASE( "Vec2f_Negation" )
{
    gm::Vec2f vector = gm::Vec2f( 0.0f, 2.0f );
    CHECK( -vector == gm::Vec2f( 0.0f, -2.0f ) );
}
